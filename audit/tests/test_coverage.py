import copy, importlib.util, json, os, re, tempfile, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def load_module(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


cov = load_module("coverage_reports", "scripts/coverage_reports.py")
vm = load_module("validate_mappings", "scripts/validate_mappings.py")


def read_json(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


DATA = read_json("controls/mappings.json")
SCHEMA = read_json("controls/mapping.schema.json")
CONTROLS = read_json("controls/controls.json")["controls"]
CONTROL_IDS = {c["id"] for c in CONTROLS}

BANNED = ("%", "score", "ready", "readiness", "certified", "compliant", "passed", "pass rate", "progress", "percent")


def fixture():
    """A small dataset that has one record of every status, so the reports can be checked by hand."""
    base = DATA["records"]
    pick = lambda fw: [r for r in base if r["framework"] == fw and r["control_id"] == "KIT-ACC-01"][0]
    gdpr = copy.deepcopy([r for r in base if r["framework"] == "GDPR" and r["control_id"] == "KIT-ACC-01"][0])
    dora = copy.deepcopy(pick("DORA"))
    soc = copy.deepcopy(pick("SOC 2"))
    iso = copy.deepcopy(pick("ISO/IEC 27001"))
    gdpr["coverage_status"] = "covered in part"
    dora2 = copy.deepcopy(dora); dora2["id"] = "KIT-ACC-01.DORA.2"; dora2["coverage_status"] = "not covered"
    dora3 = copy.deepcopy(dora); dora3["id"] = "KIT-ACC-01.DORA.3"; dora3["coverage_status"] = "not applicable"
    dora4 = copy.deepcopy(dora); dora4["id"] = "KIT-ACC-01.DORA.4"; dora4["coverage_status"] = "not assessed"
    soc["coverage_status"] = "needs expert review"
    iso["coverage_status"] = "needs expert review"
    for r in (dora2, dora3):
        r["mapping_rationale"] = "A substantive written rationale that is long enough to count."
        for k in vm.FIELDS_WITH_PLACEHOLDERS:
            if vm.is_placeholder(r.get(k)):
                r[k] = r[k] if k not in ("requirements_covered", "dependencies", "exclusions") else ["Stated"]
                if isinstance(r[k], str):
                    r[k] = "Stated"
    return {"data_date": "2026-10-09", "records": [gdpr, dora, dora2, dora3, dora4, soc, iso]}


def build(data):
    errors, incomplete = vm.validate(data, SCHEMA, {"KIT-ACC-01"})
    return cov.build_reports(data, CONTROLS, incomplete)


def sections(text):
    parts = re.split(r"(?m)^## ", text)
    return {p.split("\n", 1)[0].strip(): p for p in parts[1:]}


class Content(unittest.TestCase):
    def setUp(self):
        self.files = build(fixture())

    def test_counts_match_the_fixture(self):
        dora = self.files["dora.md"]
        for status, n in (("covered", 0), ("covered in part", 1), ("not covered", 1), ("not applicable", 1), ("not assessed", 1), ("needs expert review", 0)):
            self.assertIn(f"| {status} | {n} |", dora, status)
        self.assertIn("| **Total** | 4 |", dora)
        self.assertIn("| covered in part | 1 |", self.files["gdpr.md"])
        self.assertIn("| needs expert review | 1 |", self.files["soc2.md"])
        self.assertIn("Records: 4.", dora)

    def test_index_totals_are_the_sum_of_the_frameworks(self):
        idx = self.files["README.md"]
        self.assertIn("| **Total** | **0** | **2** | **1** | **1** | **1** | **2** | **7** |", idx)

    def test_not_assessed_is_never_shown_as_a_gap_or_a_pass(self):
        sec = sections(self.files["dora.md"])
        self.assertIn("KIT-ACC-01.DORA.4", sec["Not assessed"])
        for heading in ("Not covered", "Not applicable", "Covered in part", "Needs expert review"):
            self.assertNotIn("KIT-ACC-01.DORA.4", sec[heading], heading)
        self.assertIn("Not assessed is neither a gap nor a pass", sec["Not assessed"])

    def test_each_status_sits_only_in_its_own_section(self):
        sec = sections(self.files["dora.md"])
        self.assertIn("KIT-ACC-01.DORA.2", sec["Not covered"])
        self.assertNotIn("KIT-ACC-01.DORA.2", sec["Not applicable"])
        self.assertIn("KIT-ACC-01.DORA.3", sec["Not applicable"])
        self.assertIn("actual gaps", sec["Not covered"])
        self.assertIn("deliberate, documented exclusion", sec["Not applicable"])
        self.assertIn("KIT-ACC-01.SOC2.1", sections(self.files["soc2.md"])["Needs expert review"])

    def test_needs_expert_review_lists_the_reason_and_a_readable_first_sentence(self):
        line = [l for l in sections(self.files["soc2.md"])["Needs expert review"].splitlines() if "KIT-ACC-01.SOC2.1" in l][0]
        self.assertIn("free AICPA account", line)
        self.assertNotIn("<pending", line)

    def test_sentence_splitter_does_not_cut_at_abbreviations(self):
        got = cov._first_sentence("<pending: only the titles of Arts. 15 to 22 were checked; more. Next sentence.>")
        self.assertEqual(got, "Only the titles of Arts. 15 to 22 were checked; more.")

    def test_incomplete_records_are_listed_with_their_pending_fields(self):
        sec = sections(self.files["soc2.md"])["Incomplete records"]
        self.assertIn("KIT-ACC-01.SOC2.1", sec)
        self.assertIn("pending", sec)

    def test_label_distribution_and_edition_are_reported(self):
        gdpr = self.files["gdpr.md"]
        self.assertIn("**Review labels: community draft 1, maintainer reviewed 0, specialist reviewed 0.**", gdpr)
        self.assertIn("Edition mapped: Regulation (EU) 2016/679.", gdpr)
        self.assertIn("Data as of 2026-10-09", gdpr)


class Wording(unittest.TestCase):
    def all_texts(self):
        out = list(build(fixture()).values())
        for name in ("README.md", "soc2.md", "iso27001.md", "gdpr.md", "dora.md"):
            out.append(read(f"docs/coverage/{name}"))
        return out

    def test_every_report_opens_with_the_label_summary_and_the_notice(self):
        for t in self.all_texts():
            head = t.split("\n## ")[0] if "\n## " in t else t[:900]
            lines = [l for l in head.splitlines() if l.strip()]
            self.assertTrue(lines[0].startswith("# "), lines[0])
            self.assertTrue(lines[1].startswith("**Review labels:"), lines[1])
            self.assertEqual(lines[2], "> " + cov.NOTICE)

    def test_notice_text_is_exactly_the_agreed_wording(self):
        self.assertEqual(cov.NOTICE, "These reports describe the state of the kit's mappings. They are not a measure of anyone's compliance and the mappings have "
                                     "not been verified by a specialist unless the review label says so.")

    def test_no_percentages_scores_or_readiness_wording(self):
        for t in self.all_texts():
            body = t.replace("> " + cov.NOTICE, "").lower()
            for word in BANNED:
                self.assertNotIn(word, body, word)

    def test_no_report_uses_a_stronger_label_than_exists(self):
        for t in self.all_texts():
            self.assertNotIn("maintainer reviewed 1", t)
            self.assertNotIn("specialist reviewed 1", t)

    def test_the_only_date_is_the_recorded_data_date(self):
        data = fixture()
        data["data_date"] = "2001-02-03"
        for t in build(data).values():
            self.assertEqual(set(re.findall(r"\d{4}-\d{2}-\d{2}", t)), {"2001-02-03"})

    def test_a_build_is_reproducible(self):
        self.assertEqual(build(fixture()), build(fixture()))


class CommittedReports(unittest.TestCase):
    def test_committed_reports_are_current(self):
        self.assertEqual(cov.main(["--check"]), 0)

    def test_committed_counts_match_the_committed_mappings(self):
        recs = DATA["records"]
        idx = read("docs/coverage/README.md")
        self.assertIn(f"**{len(recs)}**", idx)
        for fw, slug in cov.FRAMEWORKS:
            n = sum(1 for r in recs if r["framework"] == fw)
            self.assertIn(f"Records: {n}.", read(f"docs/coverage/{slug}.md"))

    def test_readme_and_label_document_link_the_reports(self):
        self.assertIn("docs/coverage/README.md", read("README.md"))
        self.assertIn("coverage/README.md", read("docs/review-labels.md"))
        self.assertIn("coverage/README.md", read("controls/framework-mappings.md"))

    def test_ci_checks_the_reports(self):
        self.assertIn("scripts/coverage_reports.py --check", read(".github/workflows/sanitise.yml"))


class StaleDetection(unittest.TestCase):
    def run_check(self, mutate, **kw):
        old = cov.OUT_DIR
        with tempfile.TemporaryDirectory() as d:
            for name in os.listdir(os.path.join(ROOT, "docs", "coverage")):
                with open(os.path.join(ROOT, "docs", "coverage", name), encoding="utf-8") as src, open(os.path.join(d, name), "w", encoding="utf-8") as dst:
                    dst.write(src.read())
            mutate(d)
            cov.OUT_DIR = d
            try:
                import contextlib, io
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    rc = cov.main(["--check"])
                return rc, err.getvalue()
            finally:
                cov.OUT_DIR = old

    def test_unchanged_copy_passes(self):
        self.assertEqual(self.run_check(lambda d: None)[0], 0)

    def test_an_edited_report_fails(self):
        def edit(d):
            p = os.path.join(d, "gdpr.md")
            with open(p, encoding="utf-8") as fh:
                t = fh.read()
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(t.replace("| covered in part | 18 |", "| covered in part | 19 |"))
        rc, err = self.run_check(edit)
        self.assertEqual(rc, 1)
        self.assertIn("gdpr.md", err)

    def test_a_missing_report_fails(self):
        rc, err = self.run_check(lambda d: os.remove(os.path.join(d, "dora.md")))
        self.assertEqual(rc, 1)
        self.assertIn("dora.md", err)

    def test_an_unexpected_extra_file_fails(self):
        def add(d):
            with open(os.path.join(d, "old-report.md"), "w") as fh:
                fh.write("stale")
        rc, err = self.run_check(add)
        self.assertEqual(rc, 1)
        self.assertIn("old-report.md", err)

    def test_invalid_mappings_block_generation(self):
        real = cov._vm
        with tempfile.TemporaryDirectory() as d:
            bad = copy.deepcopy(DATA)
            bad["records"][0]["coverage_status"] = "fully covered"
            p = os.path.join(d, "m.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(bad, fh)

            def fake():
                m = real()
                m.MAPPINGS = p
                return m
            cov._vm = fake
            old = cov.OUT_DIR
            cov.OUT_DIR = os.path.join(d, "out")
            try:
                import contextlib, io
                with contextlib.redirect_stderr(io.StringIO()):
                    rc = cov.main(["--build"])
                self.assertEqual(rc, 1)
                self.assertFalse(os.path.exists(cov.OUT_DIR))
            finally:
                cov._vm = real
                cov.OUT_DIR = old

    def test_missing_input_exits_2(self):
        real = cov._vm
        def fake():
            m = real()
            m.MAPPINGS = os.path.join(tempfile.gettempdir(), "kit-no-such-mappings.json")
            return m
        cov._vm = fake
        try:
            import contextlib, io
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(cov.main(["--check"]), 2)
        finally:
            cov._vm = real


if __name__ == "__main__":
    unittest.main()
