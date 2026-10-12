import importlib.util, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "..", "kit-audit.py")
EX = os.path.join(HERE, "..", "examples")
spec = importlib.util.spec_from_file_location("kit_audit", AUDIT)
ka = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ka)


def _w(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def run(*args):
    r = subprocess.run([sys.executable, "-I", AUDIT, *args], capture_output=True, text=True)
    return r.returncode, r.stdout


class AuditTests(unittest.TestCase):
    def test_empty_repo_everything_missing(self):
        rc, out = run("--evidence", os.path.join(EX, "empty"), "--today", "2026-10-09")
        self.assertEqual(rc, 1)
        self.assertEqual(out.count("**MISSING**"), 12)
        self.assertIn("evidence check, not a compliance assessment", out)

    def test_filled_example_passes(self):
        rc, out = run("--evidence", os.path.join(EX, "filled", "evidence"), "--risks", os.path.join(EX, "filled", "risks.md"),
                      "--incidents", os.path.join(EX, "filled", "incidents.md"), "--today", "2026-10-09")
        self.assertEqual(rc, 0, out)
        self.assertEqual(out.count("**PRESENT**"), 12)
        self.assertIn("INTERNAL EVIDENCE CHECK COMPLETE", out)
        self.assertIn("It is not an examination, certification or audit", out)

    def test_stale_evidence_is_flagged(self):
        rc, out = run("--evidence", os.path.join(EX, "filled", "evidence"), "--risks", os.path.join(EX, "filled", "risks.md"),
                      "--today", "2027-09-01")
        self.assertEqual(rc, 1)
        self.assertIn("**STALE**", out)

    def test_failing_result_is_not_passing(self):
        with tempfile.TemporaryDirectory() as d:
            _w(os.path.join(d, "x.md"), "<!-- kit-evidence: control=05 date=2026-10-01 result=fail -->\n")
            rows = ka.judge(ka.load_evidence(d), ka.parse_date("2026-10-09"))
            self.assertEqual(dict((r[0], r[2]) for r in rows)["05"], "NOT PASSING")

    def test_future_date_is_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            _w(os.path.join(d, "x.md"), "<!-- kit-evidence: control=01 date=2030-01-01 result=pass -->\n")
            rows = ka.judge(ka.load_evidence(d), ka.parse_date("2026-10-09"))
            self.assertEqual(dict((r[0], r[2]) for r in rows)["01"], "INVALID")

    def test_template_placeholders_do_not_count_as_evidence(self):
        for folder in ("evidence", "scoping", "policies", "privacy"):
            rows = ka.judge(ka.load_evidence(os.path.join(HERE, "..", "..", folder)), ka.parse_date("2026-10-09"))
            self.assertTrue(all(r[2] == "MISSING" for r in rows), (folder, rows))

    def test_incident_rules(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "i.md")
            _w(p, 
                "| INC-001 | 2026-01-01 08:00 | SEV2 | leak | Yes |  | <link> | Lead | Closed |\n"
                "| INC-002 | 2026-09-01 08:00 | SEV3 | bad deploy | No | n/a |  | Lead | Open |\n"
                "| INC-003 | 2026-10-08 08:00 | SEV4 | near miss | No | n/a | r.md | Lead | Closed |\n")
            problems, total = ka.check_incidents(p, ka.parse_date("2026-10-09"))
            self.assertEqual(total, 3)
            joined = " | ".join(problems)
            self.assertIn("INC-001: personal data", joined)
            self.assertIn("INC-001: closed without a linked report", joined)
            self.assertIn("INC-002: still Open after", joined)
            self.assertNotIn("INC-003", joined)

    def test_missing_incident_register_is_reported(self):
        problems, total = ka.check_incidents(None, ka.parse_date("2026-10-09"))
        self.assertEqual(total, 0)
        self.assertTrue(problems)

    def test_unticked_boxes_counted(self):
        out = ka.unticked(os.path.join(HERE, "..", "..", "controls"))
        self.assertEqual(len(out), 12)


def risk_row(**kw):
    d = dict(id="R-001", date="2026-09-01", asset="Cloud", threat="x", lk="2", im="4", rating="Medium", safe="MFA", treat="Mitigate",
             acc="n/a", owner="Engineer", target="2026-12-01", review="2027-01-01", status="Open", ev="")
    d.update(kw)
    return "| " + " | ".join(d[k] for k in ("id", "date", "asset", "threat", "lk", "im", "rating", "safe", "treat", "acc", "owner", "target", "review", "status", "ev")) + " |\n"


def risks(*rows, today="2026-10-09"):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "r.md")
        with open(p, "w") as fh:
            fh.write("".join(rows))
        return ka.check_risks(p, ka.parse_date(today))


class EvidenceTypeTests(unittest.TestCase):
    def write(self, d, name, control, date, result, typ=None):
        with open(os.path.join(d, name), "w") as fh:
            fh.write(f"<!-- kit-evidence: control={control} date={date} result={result}" + (f" type={typ}" if typ else "") + " -->\n")

    def test_types_are_read_and_unknown_types_are_unspecified(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(d, "a.md", "05", "2026-10-01", "pass", "effectiveness")
            self.write(d, "b.md", "05", "2026-10-02", "pass", "bogus")
            self.write(d, "c.md", "05", "2026-10-03", "pass")
            kinds = {i[3] for i in ka.load_evidence(d)["05"]}
            self.assertEqual(kinds, {"effectiveness", "unspecified"})

    def test_current_passing_types_per_control(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(d, "a.md", "05", "2026-10-01", "pass", "config")
            self.write(d, "b.md", "05", "2026-10-02", "pass", "effectiveness")
            self.write(d, "c.md", "05", "2026-10-03", "fail", "assurance")      # failing: does not count
            rows = ka.judge(ka.load_evidence(d), ka.parse_date("2026-10-09"))
            self.assertEqual(dict((r[0], r[5]) for r in rows)["05"], ["config", "effectiveness"])

    def test_old_evidence_of_a_kind_does_not_count_as_current(self):
        with tempfile.TemporaryDirectory() as d:
            self.write(d, "a.md", "05", "2026-10-01", "pass", "config")
            self.write(d, "b.md", "05", "2025-01-01", "pass", "effectiveness")   # older than the 100 day limit
            rows = ka.judge(ka.load_evidence(d), ka.parse_date("2026-10-09"))
            self.assertEqual(dict((r[0], r[5]) for r in rows)["05"], ["config"])

    def test_report_lists_controls_lacking_effectiveness_evidence_without_failing(self):
        rc, out = run("--evidence", os.path.join(EX, "filled", "evidence"), "--risks", os.path.join(EX, "filled", "risks.md"),
                      "--incidents", os.path.join(EX, "filled", "incidents.md"), "--today", "2026-10-09")
        self.assertEqual(rc, 0, out)
        self.assertIn("Controls with no current passing effectiveness or assurance evidence: 01, 02, 03, 04, 07, 11, 12.", out)
        self.assertIn("does not change the exit status", out)


class RiskTests(unittest.TestCase):
    def test_clean_row(self):
        self.assertEqual(risks(risk_row()), ([], 1))

    def test_rating_must_match_scores(self):
        problems, _ = risks(risk_row(lk="4", im="4", rating="Medium"))
        self.assertTrue(any("does not match 4 x 4 = 16 (critical)" in p for p in problems), problems)

    def test_bands(self):
        for lk, im, band in ((1, 4, "low"), (1, 5, "medium"), (3, 3, "medium"), (2, 5, "high"), (3, 5, "high"), (4, 4, "critical")):
            self.assertEqual(ka.band(lk * im), band)

    def test_scores_must_be_1_to_5(self):
        problems, _ = risks(risk_row(lk="0"), risk_row(id="R-002", im="six"))
        self.assertEqual(sum("whole numbers from 1 to 5" in p for p in problems), 2)

    def test_treatment_required(self):
        problems, _ = risks(risk_row(treat=""))
        self.assertTrue(any("no treatment decision" in p for p in problems))

    def test_owner_and_review_date(self):
        problems, _ = risks(risk_row(owner="<role>", review="2026-02-01"))
        self.assertTrue(any("no owner" in p for p in problems))
        self.assertTrue(any("review overdue" in p for p in problems))

    def test_passed_target_date(self):
        problems, _ = risks(risk_row(target="2026-01-01"))
        self.assertTrue(any("target date" in p and "passed" in p for p in problems))
        self.assertEqual(risks(risk_row(target="2026-01-01", status="Treated"))[0], [])

    def test_accepted_high_risk_cannot_be_accepted_by_its_owner(self):
        problems, _ = risks(risk_row(lk="3", im="4", rating="High", treat="Accept", acc="Engineer", target="n/a", status="Accepted"))
        self.assertTrue(any("accepted by its own owner" in p for p in problems), problems)
        ok, _ = risks(risk_row(lk="3", im="4", rating="High", treat="Accept", acc="Founder", target="n/a", status="Accepted"))
        self.assertEqual(ok, [])

    def test_accepted_low_risk_may_be_accepted_by_its_owner(self):
        ok, _ = risks(risk_row(lk="1", im="2", rating="Low", treat="Accept", acc="Engineer", target="n/a", status="Accepted"))
        self.assertEqual(ok, [])

    def test_accept_needs_a_named_acceptor(self):
        problems, _ = risks(risk_row(treat="Accept", acc="", target="n/a", status="Accepted"))
        self.assertTrue(any("nobody recorded as accepting" in p for p in problems))

    def test_closed_needs_evidence(self):
        problems, _ = risks(risk_row(status="Closed", ev=""))
        self.assertEqual(problems, ["R-001: closed without evidence of treatment"])
        self.assertEqual(risks(risk_row(status="Closed", ev="see access review"))[0], [])

    def test_escaped_pipe_in_a_cell_keeps_columns_aligned(self):
        self.assertEqual(risks(risk_row(threat="a \\| b")), ([], 1))

    def test_empty_trailing_cell_is_kept(self):
        self.assertEqual(risks(risk_row(ev="")), ([], 1))

    def test_missing_register_is_reported(self):
        self.assertTrue(ka.check_risks(None, ka.parse_date("2026-10-09"))[0])


class ReviewFindings(unittest.TestCase):
    """Cases raised in an external review of the audit."""

    def test_same_date_fail_beats_pass(self):
        with tempfile.TemporaryDirectory() as d:
            _w(os.path.join(d, "01-pass.md"), "<!-- kit-evidence: control=01 date=2026-10-01 result=pass -->\n")
            _w(os.path.join(d, "01-fail.md"), "<!-- kit-evidence: control=01 date=2026-10-01 result=fail -->\n")
            rows = ka.judge(ka.load_evidence(d), ka.parse_date("2026-10-09"))
            self.assertEqual(dict((r[0], r[2]) for r in rows)["01"], "NOT PASSING")

    def test_same_date_partial_beats_pass(self):
        with tempfile.TemporaryDirectory() as d:
            _w(os.path.join(d, "a.md"), "<!-- kit-evidence: control=05 date=2026-10-01 result=partial -->\n")
            _w(os.path.join(d, "b.md"), "<!-- kit-evidence: control=05 date=2026-10-01 result=pass -->\n")
            rows = ka.judge(ka.load_evidence(d), ka.parse_date("2026-10-09"))
            self.assertEqual(dict((r[0], r[2]) for r in rows)["05"], "NOT PASSING")

    def test_newer_pass_still_supersedes_older_fail(self):
        with tempfile.TemporaryDirectory() as d:
            _w(os.path.join(d, "a.md"), "<!-- kit-evidence: control=05 date=2026-09-01 result=fail -->\n")
            _w(os.path.join(d, "b.md"), "<!-- kit-evidence: control=05 date=2026-10-01 result=pass -->\n")
            rows = ka.judge(ka.load_evidence(d), ka.parse_date("2026-10-09"))
            self.assertEqual(dict((r[0], r[2]) for r in rows)["05"], "PRESENT")

    def test_invalid_json_from_gh_is_an_error_not_a_crash(self):
        class R:
            returncode = 0
            stdout = "<html>rate limited</html>"
            stderr = ""
        real = ka.subprocess.run
        ka.subprocess.run = lambda *a, **k: R()
        try:
            calls, findings = ka.check_github("owner/repo", "main")
        finally:
            ka.subprocess.run = real
        self.assertEqual(findings[0][0], "ERROR")


class WorkedExampleTests(unittest.TestCase):
    """The worked example in examples/ must stay true to what the tool really says."""

    def test_example_co_control_05_is_present_with_both_kinds(self):
        ex = os.path.join(EX, "..", "..", "examples", "example-co")
        rc, out = run("--evidence", os.path.join(ex, "evidence"), "--risks", os.path.join(ex, "risks.md"), "--today", "2026-10-09")
        self.assertIn("| 05 | Backups and tested restores | **PRESENT** | 05-backup-configuration-2026-09-20.md, 19 days old, pass | config, effectiveness |", out)
        self.assertIn("1 row(s), none overdue, all with an owner.", out)
        doc = open(os.path.join(ex, "..", "completed-control-backups.md"), encoding="utf-8").read()
        self.assertIn("| 05 | Backups and tested restores | **PRESENT** | 05-backup-configuration-2026-09-20.md, 19 days old, pass | config, effectiveness |", doc)


class FailClearlyTests(unittest.TestCase):
    """The audit must fail clearly and conservatively, never report success because it could not read something."""

    def dirs(self):
        d = tempfile.TemporaryDirectory()
        os.makedirs(os.path.join(d.name, "ev"))
        return d

    def test_missing_evidence_folder_is_an_input_error(self):
        rc, out = run("--evidence", os.path.join(tempfile.gettempdir(), "kit-no-such-folder"))
        self.assertEqual(rc, 2)

    def test_missing_register_file_that_was_asked_for_is_an_input_error(self):
        with self.dirs() as d:
            rc, _ = run("--evidence", os.path.join(d, "ev"), "--risks", os.path.join(d, "nope.md"))
            self.assertEqual(rc, 2)
            rc, _ = run("--evidence", os.path.join(d, "ev"), "--incidents", os.path.join(d, "nope.md"))
            self.assertEqual(rc, 2)

    def test_bad_today_is_an_input_error(self):
        with self.dirs() as d:
            rc, _ = run("--evidence", os.path.join(d, "ev"), "--today", "2026-13-45")
            self.assertEqual(rc, 2)

    def test_non_utf8_evidence_file_is_reported_not_a_crash(self):
        with self.dirs() as d:
            with open(os.path.join(d, "ev", "bad.md"), "wb") as fh:
                fh.write(b"\xff\xfe\x00 not text")
            rc, out = run("--evidence", os.path.join(d, "ev"), "--today", "2026-10-09")
            self.assertEqual(rc, 1)
            self.assertIn("not valid UTF-8", out)
            self.assertNotIn("Traceback", out)

    def test_malformed_headers_are_reported(self):
        with self.dirs() as d:
            _w(os.path.join(d, "ev", "a.md"), "<!-- kit-evidence: control=05 date=2026-13-45 result=pass -->\n")
            _w(os.path.join(d, "ev", "b.md"), "<!-- kit-evidence: control=05 date=2026-10-01 result=maybe -->\n")
            _w(os.path.join(d, "ev", "c.md"), "<!-- kit-evidence: control=99 date=2026-10-01 result=pass -->\n")
            _w(os.path.join(d, "ev", "d.md"), "<!-- kit-evidence: control=NN date=YYYY-MM-DD result=pass type=config -->\n")
            found, issues, nfiles = ka.scan_evidence(os.path.join(d, "ev"))
            msgs = " | ".join(m for _, m in issues)
            self.assertEqual(found, {})
            self.assertIn("impossible date", msgs)
            self.assertIn("malformed evidence header", msgs)
            self.assertIn("unknown control", msgs)
            self.assertIn("placeholder values", msgs)
            self.assertEqual(len(issues), 4)

    def test_a_malformed_register_row_is_never_silently_skipped(self):
        with self.dirs() as d:
            _w(os.path.join(d, "r.md"), "| R-001 | 2026-09-01 | x | y | 2 | 4 | Medium |\n")
            problems, total = ka.check_risks(os.path.join(d, "r.md"), ka.parse_date("2026-10-09"))
            self.assertEqual(total, 1)
            self.assertTrue(any("row has 7 columns, expected 15" in p for p in problems), problems)
            _w(os.path.join(d, "r2.md"), risk_row().rstrip("\n").rstrip("|") + "| extra |\n")
            problems, _ = ka.check_risks(os.path.join(d, "r2.md"), ka.parse_date("2026-10-09"))
            self.assertTrue(any("expected 15" in p for p in problems), problems)
            _w(os.path.join(d, "i.md"), "| INC-001 | 2026-09-01 | SEV3 | x |\n")
            problems, total = ka.check_incidents(os.path.join(d, "i.md"), ka.parse_date("2026-10-09"))
            self.assertEqual(total, 1)
            self.assertTrue(any("expected 9" in p for p in problems), problems)

    def test_unreadable_register_is_reported(self):
        with self.dirs() as d:
            with open(os.path.join(d, "r.md"), "wb") as fh:
                fh.write(b"\xff\xfe\x00")
            problems, total = ka.check_risks(os.path.join(d, "r.md"), ka.parse_date("2026-10-09"))
            self.assertTrue(problems and total == 0)

    def test_report_says_what_was_checked_and_what_was_not(self):
        rc, out = run("--evidence", os.path.join(EX, "filled", "evidence"), "--today", "2026-10-09")
        self.assertIn("## What this run checked", out)
        self.assertIn("Risk register | **not run** (not supplied)", out)
        self.assertIn("GitHub branch rules | **not run** (not requested)", out)
        self.assertIn("Not assessed by this tool, in any run:", out)
        self.assertIn("whether any control actually works", out)

    def test_not_supplying_a_register_is_not_a_pass(self):
        rc, out = run("--evidence", os.path.join(EX, "filled", "evidence"), "--today", "2026-10-09")
        self.assertEqual(rc, 1)
        self.assertIn("NOT ASSESSED: no risk register supplied", out)

    def test_missing_gh_binary_is_an_error_not_a_crash(self):
        real = ka.subprocess.run
        def boom(*a, **k):
            raise FileNotFoundError("gh")
        ka.subprocess.run = boom
        try:
            calls, findings = ka.check_github("owner/repo", "main")
        finally:
            ka.subprocess.run = real
        self.assertEqual(findings[0][0], "ERROR")

    def test_permission_error_from_gh_is_an_error_not_a_pass(self):
        class R:
            returncode = 1
            stdout = ""
            stderr = "HTTP 403: Resource not accessible"
        real = ka.subprocess.run
        ka.subprocess.run = lambda *a, **k: R()
        try:
            calls, findings = ka.check_github("owner/repo", "main")
        finally:
            ka.subprocess.run = real
        self.assertEqual(findings[0][0], "ERROR")
        self.assertIn("403", findings[0][1])

    def test_a_repo_with_no_rulesets_fails(self):
        class R:
            returncode = 0
            stdout = "[]"
            stderr = ""
        real = ka.subprocess.run
        ka.subprocess.run = lambda *a, **k: R()
        try:
            calls, findings = ka.check_github("owner/repo", "main")
        finally:
            ka.subprocess.run = real
        self.assertEqual(findings[0][0], "FAIL")


if __name__ == "__main__":
    unittest.main()
