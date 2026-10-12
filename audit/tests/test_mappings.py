import copy, datetime as dt, importlib.util, json, os, tempfile, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
spec = importlib.util.spec_from_file_location("validate_mappings", os.path.join(ROOT, "scripts", "validate_mappings.py"))
vm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vm)

TODAY = dt.date(2026, 10, 9)


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


SCHEMA = load("controls/mapping.schema.json")
CONTROLS = load("controls/controls.json")["controls"]
CONTROL_IDS = {c["id"] for c in CONTROLS}


def good(**kw):
    """A complete, valid community-draft record for one control and framework."""
    r = {"id": "KIT-ACC-01.SOC2.1", "control_id": "KIT-ACC-01", "framework": "SOC 2", "edition": "2017 Trust Services Criteria",
         "source_reference": ["CC6.1"], "source_url": "https://example.org/source", "mapping_rationale": "Logical access restrictions are the subject of this criterion",
         "requirements_covered": ["Restricting access to named people"], "exclusions": ["Access request and approval records"],
         "dependencies": ["An access policy"], "coverage_status": "covered in part", "limitations": "Covers technical access only",
         "review": {"label": "community draft", "reviewer_role": None, "review_date": None, "decision": None, "rationale": None,
                    "next_review_trigger": "On maintainer review, or when the source edition changes"},
         "change_reference": "CHANGELOG.md [Unreleased]"}
    for k, v in kw.items():
        if k == "review":
            r["review"].update(v)
        else:
            r[k] = v
    return r


def check(*records, controls=("KIT-ACC-01",), fill=True):
    """Validate records; by default add a placeholder-free 'not assessed' record for every other control and framework so only the case under test fails."""
    recs = list(records)
    if fill:
        present = {(r.get("control_id"), r.get("framework")) for r in recs}
        for cid in controls:
            for fw in vm.FRAMEWORKS:
                if (cid, fw) not in present:
                    extra = good(id=f"{cid}.{ {'SOC 2':'SOC2','ISO/IEC 27001':'ISO27001','GDPR':'GDPR','DORA':'DORA'}[fw] }.9", control_id=cid, framework=fw, coverage_status="not assessed")
                    if fw == "DORA":
                        extra["obligation_type"] = ["direct statutory duty"]
                    recs.append(extra)
    return vm.validate({"data_date": "2026-10-09", "records": recs}, SCHEMA, set(controls), TODAY)


def messages(*records, **kw):
    return " | ".join(check(*records, **kw)[0])


class SchemaChecker(unittest.TestCase):
    def test_valid_record_passes(self):
        errors, incomplete = check(good())
        self.assertEqual(errors, [])
        self.assertEqual(incomplete, [])

    def test_missing_required_fields_are_each_reported(self):
        for field in SCHEMA["required"]:
            r = good()
            del r[field]
            self.assertIn(f"missing required field '{field}'", messages(r), field)

    def test_missing_review_subfields_are_reported(self):
        for f in SCHEMA["properties"]["review"]["required"]:
            r = good()
            del r["review"][f]
            self.assertIn(f"missing required field '{f}'", messages(r), f)

    def test_unknown_fields_are_rejected(self):
        self.assertIn("unknown field 'invented'", messages(good(invented="x")))

    def test_wrong_types_and_empty_values_are_rejected(self):
        self.assertIn("expected array", messages(good(source_reference="CC6.1")))
        self.assertIn("needs at least 1 item", messages(good(exclusions=[])))
        self.assertIn("must not be empty", messages(good(edition="")))
        self.assertIn("does not match", messages(good(source_url="http://plain")))
        self.assertIn("does not match", messages(good(id="bad id")))

    def test_invalid_coverage_status_is_rejected(self):
        for bad in ("fully covered", "Covered", "n/a", "Not assessed", "partially"):
            self.assertIn("is not one of", messages(good(coverage_status=bad)), bad)

    def test_blank_coverage_status_is_rejected_with_a_clear_message(self):
        self.assertIn("coverage_status is blank", messages(good(coverage_status="")))
        self.assertIn("coverage_status is blank", messages(good(coverage_status="   ")))

    def test_all_six_statuses_are_accepted_when_otherwise_valid(self):
        for s in ("covered in part", "not covered", "not applicable", "not assessed", "needs expert review"):
            self.assertEqual(check(good(coverage_status=s))[0], [], s)
        reviewed = {"label": "maintainer reviewed", "reviewer_role": "Maintainer", "review_date": "2026-10-01",
                    "decision": "Accepted", "rationale": "Checked against the source"}
        self.assertEqual(check(good(coverage_status="covered", review=reviewed))[0], [])

    def test_covered_is_rejected_on_a_community_draft(self):
        self.assertIn("'covered' needs a maintainer reviewed or specialist reviewed label", messages(good(coverage_status="covered")))

    def test_covered_is_accepted_on_a_specialist_reviewed_record_and_rejected_without_reviewer_data(self):
        spec = {"label": "specialist reviewed", "reviewer_role": "External specialist", "review_date": "2026-10-01",
                "decision": "Accepted", "rationale": "Checked"}
        self.assertEqual(check(good(coverage_status="covered", review=spec))[0], [])
        self.assertIn("review.reviewer_role is required", messages(good(coverage_status="covered", review={"label": "maintainer reviewed"})))

    def test_no_shipped_record_claims_covered_while_all_are_community_drafts(self):
        recs = json.load(open(os.path.join(ROOT, "controls", "mappings.json")))["records"]
        self.assertFalse([r["id"] for r in recs if r["coverage_status"] == "covered" and r["review"]["label"] == "community draft"])


class DataDate(unittest.TestCase):
    def test_data_date_is_required_and_must_be_a_real_past_date(self):
        recs = [good()]
        for bad, msg in ((None, "data_date is required"), ("2026-13-45", "data_date is required"), ("soon", "data_date is required"), ("2026-10-10", "is in the future")):
            d = {"records": recs}
            if bad is not None:
                d["data_date"] = bad
            errors, _ = vm.validate(d, SCHEMA, {"KIT-ACC-01"}, TODAY)
            self.assertTrue(any(msg in e for e in errors), (bad, errors[:2]))
        errors, _ = vm.validate({"data_date": "2026-10-09", "records": recs}, SCHEMA, {"KIT-ACC-01"}, TODAY)
        self.assertFalse(any("data_date" in e for e in errors))

    def test_committed_data_has_a_data_date(self):
        self.assertEqual(vm.valid_date(load("controls/mappings.json")["data_date"]), dt.date(2026, 10, 9))


class CrossFieldRules(unittest.TestCase):
    def test_not_covered_and_not_applicable_need_a_substantive_rationale(self):
        for s in ("not covered", "not applicable"):
            self.assertEqual(check(good(coverage_status=s))[0], [], s)
            self.assertIn("needs a substantive written rationale", messages(good(coverage_status=s, mapping_rationale="n/a")), s)
            self.assertIn("needs a substantive written rationale", messages(good(coverage_status=s, mapping_rationale="<pending: why>")), s)

    def test_covered_in_part_must_say_what_is_not_covered(self):
        self.assertIn("must say what is not covered", messages(good(coverage_status="covered in part", exclusions=["<pending: what is left out>"])))

    def test_reviewer_data_on_a_community_draft_is_rejected(self):
        for f, v in (("reviewer_role", "privacy lead"), ("review_date", "2026-10-01"), ("decision", "accepted"), ("rationale", "checked")):
            self.assertIn(f"review.{f} must be null for a community draft", messages(good(review={f: v})), f)

    def test_reviewed_labels_need_role_date_and_decision(self):
        for label in ("maintainer reviewed", "specialist reviewed"):
            for missing in ("reviewer_role", "review_date", "decision"):
                rev = {"label": label, "reviewer_role": "maintainer", "review_date": "2026-10-01", "decision": "accepted", missing: None}
                self.assertIn(f"review.{missing} is required when the label is '{label}'", messages(good(review=rev)), (label, missing))
            ok = {"label": label, "reviewer_role": "maintainer", "review_date": "2026-10-01", "decision": "accepted"}
            self.assertEqual(check(good(review=ok))[0], [], label)

    def test_future_review_date_is_rejected(self):
        rev = {"label": "maintainer reviewed", "reviewer_role": "maintainer", "review_date": "2026-10-10", "decision": "accepted"}
        self.assertIn("is in the future", messages(good(review=rev)))
        rev["review_date"] = "2026-13-45"
        self.assertTrue("does not match" in messages(good(review=rev)) or "not a real date" in messages(good(review=rev)))
        rev["review_date"] = "2026-02-31"
        self.assertIn("not a real date", messages(good(review=rev)))

    def test_placeholders_make_a_record_incomplete_and_are_limited(self):
        r = good(coverage_status="not assessed", limitations="<pending: limits>")
        errors, incomplete = check(r)
        self.assertEqual(errors, [])
        self.assertEqual(incomplete, [(r["id"], ["limitations"])])
        r2 = good(coverage_status="covered in part", limitations="<pending: limits>")
        self.assertIn("placeholders (limitations) are only allowed", messages(r2))
        rev = {"label": "maintainer reviewed", "reviewer_role": "maintainer", "review_date": "2026-10-01", "decision": "accepted"}
        r3 = good(coverage_status="not assessed", limitations="<pending: limits>", review=rev)
        self.assertIn("only allowed on a community draft", messages(r3))

    def test_needs_expert_review_may_stay_incomplete(self):
        errors, incomplete = check(good(coverage_status="needs expert review", dependencies=["<pending>"]))
        self.assertEqual(errors, [])
        self.assertEqual(len(incomplete), 1)

    def test_unknown_control_duplicate_id_and_prefix(self):
        self.assertIn("is not a control", messages(good(control_id="KIT-ZZZ-99", id="KIT-ZZZ-99.SOC2.1"), fill=False))
        self.assertIn("duplicate id", messages(good(), good(), fill=False))
        self.assertIn("id must start with the control id", messages(good(id="KIT-SEC-01.SOC2.1")))

    def test_every_control_needs_a_record_for_every_framework(self):
        errors, _ = check(good(), fill=False)
        for fw in ("ISO/IEC 27001", "GDPR", "DORA"):
            self.assertTrue(any(f"no mapping record for {fw}" in e for e in errors), fw)

    def test_dora_obligation_rules(self):
        d = good(id="KIT-ACC-01.DORA.1", framework="DORA", edition="Regulation (EU) 2022/2554", source_reference=["Art. 9"])
        self.assertIn("DORA records need obligation_type", messages(d))
        d["obligation_type"] = ["direct statutory duty"]
        self.assertEqual(check(d)[0], [])
        d30 = good(id="KIT-ACC-01.DORA.2", framework="DORA", edition="Regulation (EU) 2022/2554", source_reference=["Art. 30(2)(d)"], obligation_type=["direct statutory duty"])
        self.assertIn("Art. 30 reference must include", messages(d30))
        self.assertIn("only for DORA records", messages(good(obligation_type=["direct statutory duty"])))


class CommittedData(unittest.TestCase):
    def setUp(self):
        self.data = load("controls/mappings.json")

    def test_committed_mappings_are_valid(self):
        errors, incomplete = vm.validate(self.data, SCHEMA, CONTROL_IDS)
        self.assertEqual(errors, [])
        self.assertGreater(len(incomplete), 0)

    def test_records_are_community_drafts_with_no_invented_reviews(self):
        recs = self.data["records"]
        self.assertGreaterEqual(len(recs), 48)
        for r in recs:
            self.assertEqual(r["review"]["label"], "community draft", r["id"])
            for f in ("reviewer_role", "review_date", "decision", "rationale"):
                self.assertIsNone(r["review"][f], (r["id"], f))

    UNVERIFIED = ("ISO/IEC 27001", "SOC 2")   # frameworks whose source text could not be read

    def test_unverified_sources_are_needs_expert_review_and_incomplete(self):
        _, incomplete = vm.validate(self.data, SCHEMA, CONTROL_IDS)
        inc = {rid for rid, _ in incomplete}
        for r in self.data["records"]:
            if r["framework"] in self.UNVERIFIED:
                self.assertEqual(r["coverage_status"], "needs expert review", r["id"])
                self.assertIn(r["id"], inc, r["id"])
                self.assertIn("source verification pending", r["limitations"], r["id"])

    def test_iso_separates_annex_a_controls_from_management_system_clauses(self):
        iso = [r for r in self.data["records"] if r["framework"] == "ISO/IEC 27001"]
        for r in iso:
            for ref in r["source_reference"]:
                self.assertTrue(ref.startswith("Annex A control ") or ref.startswith("Clauses "), (r["id"], ref))
            self.assertTrue(any("not a complete ISMS" in x or "Statement of Applicability" in x for x in r["dependencies"] + r["exclusions"]), r["id"])
        clauses = [r for r in iso if any(x.startswith("Clauses ") for x in r["source_reference"])]
        self.assertEqual(len(clauses), 1)
        self.assertEqual(clauses[0]["control_id"], "KIT-GOV-01")

    def test_no_data_was_invented_for_unverified_sources(self):
        for r in self.data["records"]:
            if r["framework"] == "ISO/IEC 27001":
                self.assertTrue(vm.is_placeholder(r["source_url"]), r["id"])
            elif r["framework"] == "SOC 2":
                self.assertTrue(vm.is_placeholder(r["source_url"]) or r["source_url"].startswith("https://www.aicpa-cima.com/"), r["id"])
            else:
                self.assertTrue(r["source_url"].startswith("https://publications.europa.eu/resource/celex/"), r["id"])

    def test_dora_records_keep_their_obligation_types(self):
        dora = [r for r in self.data["records"] if r["framework"] == "DORA"]
        self.assertGreaterEqual(len(dora), 12)
        for r in dora:
            self.assertTrue(set(r["obligation_type"]) <= set(vm.OBLIGATION))
        art30 = [r for r in dora if any("Art. 30" in x for x in r["source_reference"])]
        self.assertTrue(art30)
        for r in art30:
            self.assertIn("contractual flow-down", r["obligation_type"])

    def test_every_control_has_all_four_frameworks(self):
        have = {(r["control_id"], r["framework"]) for r in self.data["records"]}
        self.assertEqual(have, {(c, f) for c in CONTROL_IDS for f in vm.FRAMEWORKS})


class GdprBackfill(unittest.TestCase):
    def setUp(self):
        self.recs = [r for r in load("controls/mappings.json")["records"] if r["framework"] == "GDPR"]

    def test_references_are_well_formed_article_pointers(self):
        import re
        for r in self.recs:
            for ref in r["source_reference"]:
                self.assertRegex(ref, r"^Art\. \d+(\(\d+\))?(\([a-z]\))?$", (r["id"], ref))

    def test_complete_records_are_covered_in_part_and_state_what_is_excluded(self):
        _, incomplete = vm.validate(load("controls/mappings.json"), SCHEMA, CONTROL_IDS)
        inc = {rid for rid, _ in incomplete}
        for r in self.recs:
            if r["id"] not in inc:
                self.assertEqual(r["coverage_status"], "covered in part", r["id"])
                self.assertTrue(r["exclusions"], r["id"])
                self.assertGreater(len(r["mapping_rationale"]), 100, r["id"])

    def test_records_whose_text_was_not_read_are_needs_expert_review_with_a_pending_marker(self):
        for r in self.recs:
            if vm.is_placeholder(r["limitations"]):
                self.assertEqual(r["coverage_status"], "needs expert review", r["id"])
                self.assertIn("source verification pending", r["limitations"], r["id"])
        pending = [r for r in self.recs if vm.is_placeholder(r["limitations"])]
        self.assertEqual({r["source_reference"][0] for r in pending}, {"Art. 15"})

    def test_every_gdpr_control_has_at_least_one_record_and_breach_duties_sit_under_incident_response(self):
        self.assertEqual({r["control_id"] for r in self.recs}, CONTROL_IDS)
        breach = [r for r in self.recs if any(x in ("Art. 33", "Art. 34") for x in r["source_reference"])]
        self.assertEqual({r["control_id"] for r in breach}, {"KIT-INC-01"})

    def test_the_privacy_control_is_split_by_requirement_not_one_catch_all_record(self):
        prv = [r for r in self.recs if r["control_id"] == "KIT-PRV-01"]
        self.assertGreaterEqual(len(prv), 6)

    def test_nothing_claims_the_kit_meets_a_gdpr_requirement(self):
        for r in self.recs:
            blob = " ".join([r["mapping_rationale"], r["limitations"]] + r["requirements_covered"]).lower()
            for banned in ("fully compl", "satisfies art", "meets art", "is compliant"):
                self.assertNotIn(banned, blob, (r["id"], banned))
            self.assertNotEqual(r["coverage_status"], "covered", r["id"])


class DoraBackfill(unittest.TestCase):
    def setUp(self):
        self.recs = [r for r in load("controls/mappings.json")["records"] if r["framework"] == "DORA"]

    def test_references_are_well_formed_article_pointers(self):
        import re
        for r in self.recs:
            for ref in r["source_reference"]:
                self.assertRegex(ref, r"^Art\. \d+(\(\d+\))?(\([a-z]\))?$", (r["id"], ref))

    def test_art_30_is_always_contractual_flow_down_and_nothing_else_is(self):
        for r in self.recs:
            has30 = any(x.startswith("Art. 30") for x in r["source_reference"])
            if has30:
                self.assertEqual(r["obligation_type"], ["contractual flow-down"], r["id"])
                self.assertTrue(all(x.startswith("Art. 30") for x in r["source_reference"]), r["id"])
            else:
                self.assertEqual(r["obligation_type"], ["direct statutory duty"], r["id"])

    def test_no_dora_record_maps_the_oversight_framework(self):
        for r in self.recs:
            self.assertNotIn("oversight obligation", r["obligation_type"], r["id"])
            for x in r["source_reference"]:
                n = int(x.split()[1].split("(")[0])
                self.assertLess(n, 31, (r["id"], x))   # Arts. 31 onwards are the oversight framework

    def test_direct_duty_records_say_they_are_a_financial_entitys_and_a_supplier_is_not_bound(self):
        for r in self.recs:
            if r["obligation_type"] == ["direct statutory duty"] and r["coverage_status"] == "covered in part":
                self.assertIn("This duty is owed by a financial entity", r["limitations"], r["id"])
                self.assertIn("contractual flow-down", r["limitations"], r["id"])

    def test_flow_down_records_say_they_are_contract_terms_not_direct_duties(self):
        for r in self.recs:
            if r["obligation_type"] == ["contractual flow-down"]:
                self.assertIn("contract", (r["limitations"] + r["mapping_rationale"]).lower(), r["id"])

    def test_the_data_return_term_is_an_honest_gap(self):
        r = [x for x in self.recs if x["source_reference"] == ["Art. 30(2)(d)"]][0]
        self.assertEqual(r["coverage_status"], "not covered")
        self.assertGreater(len(r["mapping_rationale"]), 100)

    def test_records_whose_judgement_is_open_are_needs_expert_review_with_a_pending_marker(self):
        pend = [r for r in self.recs if vm.is_placeholder(r["limitations"])]
        self.assertEqual([r["control_id"] for r in pend], ["KIT-PRV-01"])
        self.assertEqual(pend[0]["coverage_status"], "needs expert review")

    def test_controls_with_both_duty_types_are_split(self):
        by = {}
        for r in self.recs:
            by.setdefault(r["control_id"], set()).update(r["obligation_type"])
        for cid in ("KIT-BKP-01", "KIT-VND-01", "KIT-INC-01"):
            self.assertEqual(by[cid], {"direct statutory duty", "contractual flow-down"}, cid)


class GeneratedDocAndCi(unittest.TestCase):
    def run_main(self, argv, mappings=None, doc=None):
        old = (vm.MAPPINGS, vm.DOC)
        try:
            if mappings is not None:
                vm.MAPPINGS = mappings
            if doc is not None:
                vm.DOC = doc
            import contextlib, io
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = vm.main(argv)
            return rc, out.getvalue(), err.getvalue()
        finally:
            vm.MAPPINGS, vm.DOC = old

    def test_committed_markdown_is_current(self):
        rc, out, err = self.run_main(["--check"])
        self.assertEqual(rc, 0, out + err)
        self.assertIn("framework-mappings.md is up to date", out)

    def test_a_stale_generated_markdown_fails_the_check(self):
        with tempfile.TemporaryDirectory() as d:
            stale = os.path.join(d, "framework-mappings.md")
            with open(os.path.join(ROOT, "controls", "framework-mappings.md"), encoding="utf-8") as fh:
                text = fh.read()
            with open(stale, "w", encoding="utf-8") as fh:
                fh.write(text.replace("not assessed", "covered in part", 1))
            rc, out, err = self.run_main(["--check"], doc=stale)
            self.assertEqual(rc, 1)
            self.assertIn("out of date", err)

    def test_missing_markdown_fails_the_check(self):
        with tempfile.TemporaryDirectory() as d:
            rc, _, err = self.run_main(["--check"], doc=os.path.join(d, "missing.md"))
            self.assertEqual(rc, 1)

    def test_invalid_data_fails_the_check_and_blocks_a_build(self):
        data = copy.deepcopy(load("controls/mappings.json"))
        data["records"][0]["coverage_status"] = "fully covered"
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "m.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(data, fh)
            rc, out, _ = self.run_main(["--check"], mappings=p)
            self.assertEqual(rc, 1)
            self.assertIn("INVALID", out)
            target = os.path.join(d, "out.md")
            rc, _, err = self.run_main(["--build"], mappings=p, doc=target)
            self.assertEqual(rc, 1)
            self.assertFalse(os.path.exists(target))

    def test_missing_or_unreadable_inputs_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            rc, _, err = self.run_main([], mappings=os.path.join(d, "nope.json"))
            self.assertEqual(rc, 2)
            bad = os.path.join(d, "bad.json")
            with open(bad, "w") as fh:
                fh.write("not json")
            rc, _, _ = self.run_main([], mappings=bad)
            self.assertEqual(rc, 2)

    def test_a_missing_required_field_in_the_data_fails(self):
        data = copy.deepcopy(load("controls/mappings.json"))
        del data["records"][3]["limitations"]
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "m.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(data, fh)
            rc, out, _ = self.run_main([], mappings=p)
            self.assertEqual(rc, 1)
            self.assertIn("missing required field 'limitations'", out)

    def test_ci_runs_the_mapping_check_and_the_index_check(self):
        with open(os.path.join(ROOT, ".github", "workflows", "sanitise.yml"), encoding="utf-8") as fh:
            ci = fh.read()
        self.assertIn("scripts/validate_mappings.py --check", ci)
        self.assertIn("scripts/controls_index.py --check", ci)

    def test_controls_index_stays_current(self):
        spec2 = importlib.util.spec_from_file_location("controls_index", os.path.join(ROOT, "scripts", "controls_index.py"))
        ci = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(ci)
        self.assertEqual(ci.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
