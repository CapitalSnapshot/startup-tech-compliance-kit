"""Tests for scripts/review_scope.py and the published specialist review scopes."""
import copy
import datetime
import glob
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
spec = importlib.util.spec_from_file_location("review_scope", os.path.join(ROOT, "scripts", "review_scope.py"))
rs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rs)

def load_json(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return json.load(fh)


MAPPINGS = load_json("controls", "mappings.json")["records"]
SCOPES = sorted(glob.glob(os.path.join(ROOT, "docs", "specialist-reviews", "scopes", "*.json")))
FRAMEWORK_OF = {"gdpr-privacy.json": "GDPR", "iso27001.json": "ISO/IEC 27001", "soc2.json": "SOC 2", "dora.json": "DORA"}
TODAY = datetime.date(2026, 10, 12)


def proposed():
    return load_json("docs", "specialist-reviews", "scopes", "dora.json")


def completed():
    s = proposed()
    s["status"] = "completed"
    s["reviewer_role"] = "independent practitioner with a relevant qualification"
    s["review_date"] = "2026-10-01"
    s["limitations"] = "Text of the Regulation only; no national law."
    s["decisions"] = {i: {"decision": "accepted", "rationale": "checked against the article"} for i in s["records"] + s["documents"]}
    return s


def errs(scope):
    return rs.check_scope(scope, today=TODAY)


class PublishedScopes(unittest.TestCase):
    def test_four_scopes_exist(self):
        self.assertEqual(sorted(os.path.basename(p) for p in SCOPES), sorted(FRAMEWORK_OF))

    def test_every_published_scope_is_valid_and_proposed(self):
        for path in SCOPES:
            s = load_json(path)
            self.assertEqual(errs(s), [], path)
            self.assertEqual(s["status"], "proposed", path)
            self.assertIsNone(s["reviewer_role"], path)
            self.assertIsNone(s["review_date"], path)

    def test_each_scope_covers_every_record_of_its_framework(self):
        for path in SCOPES:
            s = load_json(path)
            want = sorted(r["id"] for r in MAPPINGS if r["framework"] == FRAMEWORK_OF[os.path.basename(path)])
            self.assertEqual(sorted(s["records"]), want, path)

    def test_no_record_is_claimed_reviewed_while_scopes_are_proposed(self):
        for r in MAPPINGS:
            self.assertEqual(r["review"]["label"], "community draft", r["id"])

    def test_scopes_state_exclusions_and_editions(self):
        for path in SCOPES:
            s = load_json(path)
            self.assertGreaterEqual(len(s["exclusions"]), 3, path)
            self.assertTrue(s["source_editions"], path)

    def test_check_all_command_exits_zero(self):
        p = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts", "review_scope.py"), "check", "--all"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)


class CheckRules(unittest.TestCase):
    def test_proposed_baseline_is_valid(self):
        self.assertEqual(errs(proposed()), [])

    def test_completed_baseline_is_valid(self):
        self.assertEqual(errs(completed()), [])

    def test_missing_field(self):
        s = proposed()
        del s["exclusions"]
        self.assertIn("missing field: exclusions", errs(s))

    def test_bad_status(self):
        s = proposed()
        s["status"] = "reviewed"
        self.assertTrue(any("status must be" in e for e in errs(s)))

    def test_unknown_record(self):
        s = proposed()
        s["records"].append("KIT-ACC-01.DORA.99")
        self.assertIn("unknown mapping record: KIT-ACC-01.DORA.99", errs(s))

    def test_missing_document(self):
        s = proposed()
        s["documents"].append("scoping/does-not-exist.md")
        self.assertTrue(any("document not found" in e for e in errs(s)))

    def test_document_outside_repository(self):
        s = proposed()
        s["documents"] = ["../outside.md"]
        self.assertTrue(any("document not found" in e for e in errs(s)))

    def test_duplicate_record(self):
        s = proposed()
        s["records"].append(s["records"][0])
        self.assertTrue(any("twice" in e for e in errs(s)))

    def test_empty_exclusions(self):
        s = proposed()
        s["exclusions"] = []
        self.assertTrue(any("exclusions must be" in e for e in errs(s)))

    def test_proposed_cannot_claim_a_reviewer(self):
        s = proposed()
        s["reviewer_role"] = "privacy professional"
        self.assertTrue(any("reviewer_role null" in e for e in errs(s)))

    def test_proposed_cannot_claim_a_date(self):
        s = proposed()
        s["review_date"] = "2026-10-01"
        self.assertTrue(any("review_date null" in e for e in errs(s)))

    def test_proposed_cannot_carry_decisions(self):
        s = proposed()
        s["decisions"] = {s["records"][0]: {"decision": "accepted", "rationale": "x"}}
        self.assertTrue(any("no decisions" in e for e in errs(s)))

    def test_completed_needs_role(self):
        s = completed()
        s["reviewer_role"] = " "
        self.assertTrue(any("needs a reviewer_role" in e for e in errs(s)))

    def test_completed_rejects_maintainer_and_author_roles(self):
        for role in ("Maintainer of the kit", "author of the mapping"):
            s = completed()
            s["reviewer_role"] = role
            self.assertTrue(any("cannot award" in e for e in errs(s)), role)

    def test_completed_needs_real_date(self):
        for bad in (None, "2026-13-45", "12 October 2026", "2026-10-1"):
            s = completed()
            s["review_date"] = bad
            self.assertTrue(errs(s), bad)

    def test_completed_rejects_future_date(self):
        s = completed()
        s["review_date"] = "2026-10-13"
        self.assertIn("review_date is in the future", errs(s))

    def test_completed_needs_limitations(self):
        s = completed()
        s["limitations"] = ""
        self.assertTrue(any("needs limitations" in e for e in errs(s)))

    def test_completed_needs_a_decision_for_every_item(self):
        s = completed()
        del s["decisions"][s["records"][0]]
        self.assertIn(f"no decision recorded for {s['records'][0]}", errs(s))
        s = completed()
        del s["decisions"][s["documents"][0]]
        self.assertTrue(any("no decision recorded" in e for e in errs(s)))

    def test_completed_rejects_unknown_decision_value(self):
        s = completed()
        s["decisions"][s["records"][0]]["decision"] = "approved"
        self.assertTrue(any("decision must be" in e for e in errs(s)))

    def test_completed_needs_rationale(self):
        s = completed()
        s["decisions"][s["records"][0]]["rationale"] = ""
        self.assertTrue(any("rationale is required" in e for e in errs(s)))

    def test_decision_outside_scope(self):
        s = completed()
        s["decisions"]["KIT-ACC-01.GDPR.1"] = {"decision": "accepted", "rationale": "x"}
        self.assertTrue(any("outside the scope" in e for e in errs(s)))

    def test_non_object(self):
        self.assertEqual(rs.check_scope([], today=TODAY), ["scope file must be a JSON object"])


class ListAndPreview(unittest.TestCase):
    def test_list_names_every_record_and_document_and_the_rule(self):
        s = proposed()
        out = rs.cmd_list(s, {r["id"]: r for r in MAPPINGS})
        for item in s["records"] + s["documents"]:
            self.assertIn(item, out)
        self.assertIn("Nothing else changes", out)
        self.assertNotIn("specialist reviewed |", out)

    def test_preview_of_proposed_scope_writes_nothing_and_says_so(self):
        out = rs.cmd_preview(proposed(), {r["id"]: r for r in MAPPINGS})
        self.assertIn("No review has been recorded", out)

    def test_preview_only_raises_accepted_items(self):
        s = completed()
        s["decisions"][s["records"][0]]["decision"] = "not reviewed"
        s["decisions"][s["records"][1]]["decision"] = "not accepted"
        s["decisions"][s["records"][2]]["decision"] = "accepted with changes"
        out = rs.cmd_preview(s, {r["id"]: r for r in MAPPINGS})
        lines = {l.split(":")[0]: l for l in out.splitlines() if l.startswith("KIT-")}
        self.assertIn("no change", lines[s["records"][0]])
        self.assertIn("no change", lines[s["records"][1]])
        self.assertIn("specialist reviewed", lines[s["records"][2]])
        self.assertIn("accepted with changes", lines[s["records"][2]])

    def raw(self):
        with open(os.path.join(ROOT, "controls", "mappings.json"), "rb") as fh:
            return fh.read()

    def test_preview_does_not_modify_files(self):
        before = self.raw()
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "done.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(completed(), fh)
            p = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts", "review_scope.py"), "preview", path], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(self.raw(), before)

    def test_command_fails_on_invalid_scope_and_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            bad = os.path.join(d, "bad.json")
            s = proposed()
            s["reviewer_role"] = "someone"
            with open(bad, "w", encoding="utf-8") as fh:
                json.dump(s, fh)
            for path in (bad, os.path.join(d, "missing.json")):
                p = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts", "review_scope.py"), "check", path], capture_output=True, text=True)
                self.assertEqual(p.returncode, 1, path)


class Documents(unittest.TestCase):
    def read(self, rel):
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            return fh.read()

    def test_readme_states_the_rule_and_the_current_position(self):
        t = self.read("docs/specialist-reviews/README.md")
        self.assertIn("no specialist review has been recorded", t)
        self.assertIn("Only the material named in a published review scope becomes", t)

    def test_template_has_required_headings(self):
        t = self.read("docs/specialist-reviews/review-record-template.md")
        for h in ("Review date", "Reviewer role", "## Scope", "## Exclusions", "## Outcome", "## Limitations"):
            self.assertIn(h, t)
        self.assertIn("Nothing else changes", t)

    def test_procedure_is_manual_and_forbids_self_award(self):
        t = self.read("docs/specialist-reviews/update-procedure.md")
        self.assertIn("not a maintainer or an author", t)
        self.assertIn("Nothing here is automated", t)

    def test_contributing_has_the_section_and_no_stale_label_name(self):
        t = self.read("CONTRIBUTING.md")
        self.assertIn("## Offering a specialist review", t)
        self.assertNotIn("specialist-verified", t)

    def test_public_pages_do_not_point_at_internal_working_files(self):
        internal = ("/".join(("docs", "review")) + "/", "AGENTS" + ".md")
        for rel in ("CONTRIBUTING.md", "docs/specialist-reviews/README.md", "docs/specialist-reviews/review-record-template.md",
                    "docs/specialist-reviews/update-procedure.md"):
            for needle in internal:
                self.assertNotIn(needle, self.read(rel), rel)


if __name__ == "__main__":
    unittest.main()
