import contextlib, copy, datetime as dt, importlib.util, io, json, os, re, subprocess, sys, tempfile, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
spec = importlib.util.spec_from_file_location("source_impact", os.path.join(ROOT, "scripts", "source_impact.py"))
si = importlib.util.module_from_spec(spec)
spec.loader.exec_module(si)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


SOURCES = si.load(si.SOURCES)
MAPPINGS = si.load(si.MAPPINGS)
CONTROLS = si.load(si.CONTROLS)["controls"]
TODAY = dt.date(2026, 10, 12)


def errs(sources=None, mappings=None, today=TODAY):
    return si.validate(sources or SOURCES, mappings or MAPPINGS, ROOT, today)


def run_main(argv, **patches):
    old = {k: getattr(si, k) for k in patches}
    for k, v in patches.items():
        setattr(si, k, v)
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = si.main(argv)
    finally:
        for k, v in old.items():
            setattr(si, k, v)
    return rc, out.getvalue(), err.getvalue()


class Validation(unittest.TestCase):
    def test_committed_watch_list_is_valid(self):
        self.assertEqual(errs(), [])

    def test_each_required_field_is_enforced(self):
        for f in si.REQUIRED:
            s = copy.deepcopy(SOURCES)
            del s["sources"][0][f]
            self.assertTrue(any(f"missing field '{f}'" in e for e in errs(s)), f)

    def test_duplicate_ids_bad_types_and_frameworks(self):
        s = copy.deepcopy(SOURCES); s["sources"][1]["id"] = s["sources"][0]["id"]
        self.assertTrue(any("duplicate id" in e for e in errs(s)))
        s = copy.deepcopy(SOURCES); s["sources"][0]["type"] = "blog"
        self.assertTrue(any("type must be one of" in e for e in errs(s)))
        s = copy.deepcopy(SOURCES); s["sources"][0]["framework"] = "HIPAA"
        self.assertTrue(any("framework must be null or one of" in e for e in errs(s)))
        s = copy.deepcopy(SOURCES); s["sources"][0]["id"] = "Bad Id"
        self.assertTrue(any("id must be lowercase" in e for e in errs(s)))

    def test_empty_text_fields_owner_address_and_url(self):
        for f in ("name", "edition_mapped", "url_status", "owner", "review_cadence", "checked_what", "notes"):
            s = copy.deepcopy(SOURCES); s["sources"][0][f] = " "
            self.assertTrue(any(f"{f} must not be empty" in e for e in errs(s)), f)
        s = copy.deepcopy(SOURCES); s["sources"][0]["owner"] = "someone@example.org"
        self.assertTrue(any("owner must be a role" in e for e in errs(s)))
        s = copy.deepcopy(SOURCES); s["sources"][0]["official_url"] = "http://plain.example.org"
        self.assertTrue(any("official_url must be null or an https URL" in e for e in errs(s)))

    def test_dates_cadence_and_documents(self):
        s = copy.deepcopy(SOURCES); s["sources"][0]["last_checked"] = "2026-13-45"
        self.assertTrue(any("not a real date" in e for e in errs(s)))
        s = copy.deepcopy(SOURCES); s["sources"][0]["last_checked"] = "2026-10-13"
        self.assertTrue(any("is in the future" in e for e in errs(s)))
        for bad in (0, -1, "yearly", True):
            s = copy.deepcopy(SOURCES); s["sources"][0]["review_cadence_days"] = bad
            self.assertTrue(any("review_cadence_days" in e for e in errs(s)), bad)
        s = copy.deepcopy(SOURCES); s["sources"][0]["documents"] = ["no/such/file.md"]
        self.assertTrue(any("document not found" in e for e in errs(s)))

    def test_a_mapping_edition_the_watch_list_does_not_name_is_an_error(self):
        m = copy.deepcopy(MAPPINGS)
        for r in m["records"]:
            if r["framework"] == "SOC 2":
                r["edition"] = "2027 Trust Services Criteria (fictional)"
        e = [x for x in errs(mappings=m) if x.startswith("SOC 2")]
        self.assertEqual(len(e), 1)
        self.assertIn("mapping records use edition(s) ['2027 Trust Services Criteria (fictional)'] but the watch list says", e[0])

    def test_a_watch_list_edition_no_record_uses_is_an_error(self):
        s = copy.deepcopy(SOURCES)
        for x in s["sources"]:
            if x["framework"] == "GDPR":
                x["edition_mapped"] = "Regulation (EU) 2016/679, consolidated 2099"
        self.assertTrue(any(e.startswith("GDPR: mapping records use edition") for e in errs(s)))

    def test_a_mapped_framework_with_no_source_is_an_error(self):
        s = copy.deepcopy(SOURCES)
        s["sources"] = [x for x in s["sources"] if x["framework"] != "DORA"]
        self.assertTrue(any("DORA: the mappings use this framework but no source" in e for e in errs(s)))

    def test_every_mapped_framework_has_a_source_and_all_documents_exist(self):
        mapped = {r["framework"] for r in MAPPINGS["records"]}
        self.assertEqual(mapped, {s["framework"] for s in SOURCES["sources"] if s["framework"]})
        for s in SOURCES["sources"]:
            for p in s["documents"]:
                self.assertTrue(os.path.exists(os.path.join(ROOT, p)), p)

    def test_owners_are_roles_and_unchecked_sources_say_so(self):
        for s in SOURCES["sources"]:
            self.assertNotIn("@", s["owner"])
            if s["last_checked"] is None:
                self.assertTrue(s["checked_what"].lower().startswith("nothing"), s["id"])
            else:
                self.assertNotIn("nothing", s["checked_what"].lower().split(".")[0], s["id"])


class Impact(unittest.TestCase):
    def test_soc2_lists_all_twelve_records_the_control_files_and_documents(self):
        r = si.impact(SOURCES, MAPPINGS, CONTROLS, "SOC 2")
        self.assertEqual(len(r["records"]), 12)
        self.assertEqual(len(r["control_files"]), 12)
        self.assertEqual(r["documents"], ["guide/paths/soc2.md"])

    def test_counts_per_framework_match_the_mappings(self):
        for fw in ("SOC 2", "ISO/IEC 27001", "GDPR", "DORA"):
            r = si.impact(SOURCES, MAPPINGS, CONTROLS, fw)
            self.assertEqual(len(r["records"]), sum(1 for x in MAPPINGS["records"] if x["framework"] == fw), fw)

    def test_lookup_is_case_insensitive_and_accepts_a_source_id(self):
        self.assertEqual(len(si.impact(SOURCES, MAPPINGS, CONTROLS, "dora")["records"]), len(si.impact(SOURCES, MAPPINGS, CONTROLS, "DORA")["records"]))
        self.assertIsNotNone(si.impact(SOURCES, MAPPINGS, CONTROLS, "gdpr"))

    def test_edition_filter_narrows_and_can_return_nothing(self):
        self.assertEqual(len(si.impact(SOURCES, MAPPINGS, CONTROLS, "DORA", "2022/2554")["records"]), 16)
        self.assertEqual(si.impact(SOURCES, MAPPINGS, CONTROLS, "DORA", "2030")["records"], [])

    def test_gdpr_impact_includes_the_documents_that_rely_on_it(self):
        docs = si.impact(SOURCES, MAPPINGS, CONTROLS, "GDPR")["documents"]
        for p in ("scoping/gdpr-territorial-scope.md", "privacy/dpia-screening.md", "runbooks/incident-response.md"):
            self.assertIn(p, docs)

    def test_a_cited_but_unmapped_source_has_documents_and_no_records(self):
        r = si.impact(SOURCES, MAPPINGS, CONTROLS, "wp248")
        self.assertEqual(r["records"], [])
        self.assertEqual(r["documents"], ["privacy/dpia-screening.md"])

    def test_unknown_framework_exits_2_with_the_known_names(self):
        self.assertIsNone(si.impact(SOURCES, MAPPINGS, CONTROLS, "HIPAA"))
        rc, _, err = run_main(["list", "--framework", "HIPAA"])
        self.assertEqual(rc, 2)
        self.assertIn("Known:", err)

    def test_json_output_parses(self):
        rc, out, _ = run_main(["list", "--framework", "GDPR", "--json"])
        self.assertEqual(rc, 0)
        self.assertEqual(len(json.loads(out)["records"]), 19)


class ReleaseNotes(unittest.TestCase):
    def test_status_current_stale_never_and_not_tracked(self):
        by = {s["id"]: s for s in SOURCES["sources"]}
        self.assertEqual(si.status(by["gdpr"], dt.date(2026, 10, 12)), "current")
        self.assertEqual(si.status(by["gdpr"], dt.date(2027, 10, 10)), "stale")
        self.assertEqual(si.status(by["iso-27001"], dt.date(2026, 10, 12)), "never checked")
        self.assertEqual(si.status(by["authority-lists"], dt.date(2030, 1, 1)), "not tracked")

    def test_release_notes_report_unreviewed_mappings_and_ask_for_the_two_lines(self):
        t = si.release_notes(SOURCES, MAPPINGS, TODAY)
        self.assertIn("Community drafts (no maintainer or specialist review recorded): 60 of 60 records.", t)
        self.assertIn("Sources and editions changed by this release:", t)
        self.assertIn("Mappings this release leaves stale, unreviewed or incomplete:", t)
        self.assertIn("never checked", t)

    def test_a_year_later_sources_show_as_stale(self):
        t = si.release_notes(SOURCES, MAPPINGS, dt.date(2027, 12, 1))
        self.assertIn("(stale)", t)

    def test_bad_today_exits_2(self):
        rc, _, _ = run_main(["release-notes", "--today", "soon"])
        self.assertEqual(rc, 2)


class PageAndCi(unittest.TestCase):
    def test_committed_page_is_current(self):
        rc, out, err = run_main(["check"])
        self.assertEqual(rc, 0, err)

    def test_a_stale_or_missing_page_fails(self):
        with tempfile.TemporaryDirectory() as d:
            stale = os.path.join(d, "p.md")
            with open(stale, "w") as fh:
                fh.write("old")
            self.assertEqual(run_main(["check"], PAGE=stale)[0], 1)
            self.assertEqual(run_main(["check"], PAGE=os.path.join(d, "none.md"))[0], 1)

    def test_invalid_data_blocks_build_and_check(self):
        with tempfile.TemporaryDirectory() as d:
            bad = copy.deepcopy(SOURCES); bad["sources"][0]["type"] = "blog"
            p = os.path.join(d, "s.json")
            with open(p, "w") as fh:
                json.dump(bad, fh)
            page = os.path.join(d, "page.md")
            self.assertEqual(run_main(["build"], SOURCES=p, PAGE=page)[0], 1)
            self.assertFalse(os.path.exists(page))
            self.assertEqual(run_main(["check"], SOURCES=p, PAGE=page)[0], 1)

    def test_unreadable_input_exits_2(self):
        rc, _, _ = run_main(["check"], SOURCES=os.path.join(tempfile.gettempdir(), "kit-no-such-sources.json"))
        self.assertEqual(rc, 2)

    def test_ci_runs_the_check(self):
        self.assertIn("scripts/source_impact.py check", read(".github/workflows/sanitise.yml"))


class TheProcess(unittest.TestCase):
    """The acceptance criterion: a maintainer can trace a framework update from a source change to a reviewed release."""

    def test_an_edition_change_is_traced_end_to_end_with_the_tools(self):
        # 1. the records change edition but the watch list does not: the check refuses
        m = copy.deepcopy(MAPPINGS)
        for r in m["records"]:
            if r["framework"] == "SOC 2":
                r["edition"] = "2027 Trust Services Criteria (fictional)"
        self.assertTrue(any(e.startswith("SOC 2") for e in si.validate(SOURCES, m, ROOT, TODAY)))
        # 2. the watch list is updated to agree: the check passes
        s = copy.deepcopy(SOURCES)
        for x in s["sources"]:
            if x["framework"] == "SOC 2":
                x["edition_mapped"] = "2027 Trust Services Criteria (fictional)"
                x["last_checked"] = "2026-10-12"
        self.assertEqual(si.validate(s, m, ROOT, TODAY), [])
        # 3. the impact list for the new edition finds every record to review
        r = si.impact(s, m, CONTROLS, "SOC 2", "2027")
        self.assertEqual(len(r["records"]), 12)
        # 4. a record that changed is back to community draft with no reviewer
        for rec in m["records"]:
            if rec["framework"] == "SOC 2":
                self.assertEqual(rec["review"]["label"], "community draft")
                self.assertIsNone(rec["review"]["reviewer_role"])
        # 5. the release notes name the new edition and the unreviewed records
        t = si.release_notes(s, m, TODAY)
        self.assertIn("2027 Trust Services Criteria (fictional)", t)
        self.assertIn("Community drafts", t)

    def test_maintenance_describes_roles_nine_steps_and_the_fallback(self):
        t = read("MAINTENANCE.md")
        for role in ("Source watcher", "Impact analyst", "Reviewer", "Release manager"):
            self.assertIn(f"| **{role}**", t)
        steps = re.findall(r"(?m)^(\d)\. \*\*", t)
        self.assertEqual(steps, [str(i) for i in range(1, 10)])
        for needle in ("scripts/source_impact.py list", "scripts/source_impact.py release-notes", "scripts/validate_mappings.py --build",
                       "scripts/coverage_reports.py --build", "If nobody can review in time", "needs expert review", "If no maintainer is available at all",
                       "Never record a reviewer, date or decision that did not happen", "worked-example.md", "Framework, law or guidance update"):
            self.assertIn(needle, t, needle)

    def test_maintenance_no_longer_points_at_the_removed_last_reviewed_column(self):
        t = read("MAINTENANCE.md") + read("VERSIONING.md")
        self.assertNotIn('"last reviewed" dates in', t)
        self.assertNotIn('a "last reviewed" date ([`controls/framework-mappings.md`]', t)

    def test_issue_template_has_the_impact_checklist(self):
        t = read(".github/ISSUE_TEMPLATE/framework_update.md")
        for needle in ("Impact analysis checklist", "source_impact.py list", "community draft", "null reviewer fields", "data_date", "release-notes",
                       "needs expert review"):
            self.assertIn(needle, t, needle)

    def test_versioning_and_release_require_sources_to_be_named(self):
        v, r = read("VERSIONING.md"), read("RELEASE.md")
        self.assertIn("A release that changes compliance content names its sources", v)
        self.assertIn("A change of framework edition", v)
        self.assertIn("scripts/source_impact.py release-notes", v + r)
        self.assertIn("Sources and editions are named", r)
        self.assertIn("scripts/source_impact.py check", r)

    def test_the_worked_example_is_fictional_and_its_output_is_real(self):
        t = read("docs/maintenance/worked-example.md")
        self.assertIn("**This example is fictional.**", t)
        self.assertEqual(len(re.findall(r"(?m)^## \d\. ", t)), 9)
        real = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts", "source_impact.py"), "list", "--framework", "SOC 2"],
                              capture_output=True, text=True, cwd=ROOT).stdout.splitlines()
        for line in real[:6]:
            self.assertIn(line, t, line)
        m = copy.deepcopy(MAPPINGS)
        for r in m["records"]:
            if r["framework"] == "SOC 2":
                r["edition"] = "2027 Trust Services Criteria (fictional)"
        self.assertIn([e for e in si.validate(SOURCES, m, ROOT, TODAY) if e.startswith("SOC 2")][0], t)
        notes = si.release_notes(SOURCES, MAPPINGS, TODAY).splitlines()
        for line in [l for l in notes if l.startswith("| AICPA") or l.startswith("- Community drafts")]:
            self.assertIn(line, t, line)
        self.assertNotIn("reviewer_role\": \"", t)

    def test_nothing_in_the_process_documents_invents_a_review(self):
        for f in ("MAINTENANCE.md", "docs/maintenance/worked-example.md", ".github/ISSUE_TEMPLATE/framework_update.md"):
            t = read(f)
            self.assertNotIn("specialist reviewed 1", t)
            self.assertIn("community draft", t, f)


if __name__ == "__main__":
    unittest.main()
