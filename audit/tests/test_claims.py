"""Tests for the prohibited-claims check (scripts/check_claims.py), the standing notice and the reworded skill text."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
spec = importlib.util.spec_from_file_location("check_claims", os.path.join(ROOT, "scripts", "check_claims.py"))
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

NOTICE = "**Standing notice.**"
NOTICE_PARTS = ("repository based, community maintained guidance", "not legal advice", "a formal compliance assessment",
                "a certification or an independent security audit", "unverified unless their review label says otherwise")
NOTICE_FILES = ["README.md", "controls/framework-mappings.md", "guide/paths/README.md", "guide/paths/soc2.md", "guide/paths/iso27001.md",
                "privacy/README.md", "scoping/applicability-matrix.md", "scoping/dora-screening.md",
                "scoping/gdpr-territorial-scope.md", "scoping/extensions/nis2-screening.md"]
PRIVACY_PAGES = sorted(f for f in os.listdir(os.path.join(ROOT, "privacy")) if f.endswith(".md"))


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


class RepositoryIsClean(unittest.TestCase):
    def test_check_exits_zero(self):
        p = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts", "check_claims.py")], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_no_stale_allowlist_entries(self):
        blocked, stale = cc.evaluate(cc.scan(), cc.load_allowlist())
        self.assertEqual(blocked, {})
        self.assertEqual(stale, [])

    def test_every_allowlist_entry_has_a_reason(self):
        for e in cc.load_allowlist():
            self.assertTrue(e["reason"].strip(), e)

    def test_skill_prose_no_longer_claims_readiness(self):
        for rel in ("skills/README.md", "skills/production-migration/SKILL.md",
                    "skills/production-migration/references/README.md", "skills/production-migration/references/prompts/A1-draft-plan.md"):
            t = read(rel).lower()
            for phrase in ("audit-ready", "compliance-ready", "evidence-ready", "survive security due diligence", "stand up to security"):
                self.assertNotIn(phrase, t, f"{rel}: {phrase}")

    def test_phrase_list_includes_prose_only_phrases(self):
        self.assertIn("legally sound", cc.load_phrases())
        self.assertIn("audit-ready", cc.load_phrases())


class Rules(unittest.TestCase):
    def tree(self, files, allow=()):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        for rel, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(d.name, rel)) or d.name, exist_ok=True)
            with open(os.path.join(d.name, rel), "w", encoding="utf-8") as fh:
                fh.write(text)
        hits = cc.scan(d.name, ["compliant", "audit-ready", "legally sound"])
        return d.name, hits, list(allow)

    def test_hit_is_blocked_without_allowlist(self):
        root, hits, allow = self.tree({"a.md": "Your setup is audit-ready.\n"})
        blocked, _ = cc.evaluate(hits, allow, root)
        self.assertEqual(list(blocked), [("a.md", "audit-ready")])
        self.assertEqual(blocked[("a.md", "audit-ready")], [1])

    def test_case_and_whole_word_matching(self):
        root, hits, _ = self.tree({"a.md": "AUDIT-READY. Also noncompliant and compliantly are not the word.\n"})
        self.assertIn(("a.md", "audit-ready"), hits)
        self.assertNotIn(("a.md", "compliant"), hits)

    def test_allowlist_entry_permits_one_phrase_in_one_file(self):
        allow = [{"file": "a.md", "phrase": "compliant", "reason": "negation"}]
        root, hits, allow = self.tree({"a.md": "Not compliant by default.\n", "b.md": "Not compliant by default.\n"}, allow)
        blocked, stale = cc.evaluate(hits, allow, root)
        self.assertEqual(list(blocked), [("b.md", "compliant")])
        self.assertEqual(stale, [])

    def test_wildcard_entry_permits_a_whole_file(self):
        allow = [{"file": "a.md", "phrase": "*", "reason": "test"}]
        root, hits, allow = self.tree({"a.md": "compliant, audit-ready, legally sound\n"}, allow)
        self.assertEqual(cc.evaluate(hits, allow, root), ({}, []))

    def test_stale_entry_is_reported(self):
        allow = [{"file": "a.md", "phrase": "compliant", "reason": "negation"}]
        root, hits, allow = self.tree({"a.md": "Nothing to see.\n"}, allow)
        _, stale = cc.evaluate(hits, allow, root)
        self.assertEqual(len(stale), 1)

    def test_entry_for_missing_file_is_ignored(self):
        allow = [{"file": "gone.md", "phrase": "*", "reason": "removed before release"}]
        root, hits, allow = self.tree({"a.md": "fine\n"}, allow)
        self.assertEqual(cc.evaluate(hits, allow, root), ({}, []))

    def test_allowlist_entry_without_reason_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "allow.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"allow": [{"file": "a.md", "phrase": "compliant", "reason": " "}]}, fh)
            with self.assertRaises(ValueError):
                cc.load_allowlist(path)

    def test_non_text_files_and_skipped_dirs_are_ignored(self):
        root, hits, _ = self.tree({"a.bin": "audit-ready", ".git/x.md": "audit-ready", "__pycache__/y.md": "audit-ready"})
        self.assertEqual(hits, {})


class StandingNotice(unittest.TestCase):
    def test_notice_is_on_readme_and_each_framework_guide(self):
        for rel in NOTICE_FILES:
            t = read(rel)
            self.assertIn(NOTICE, t, rel)
            block = t[t.index(NOTICE):].split("\n", 1)[0]
            for part in NOTICE_PARTS:
                self.assertIn(part, block, f"{rel}: {part}")

    def test_notice_is_near_the_top(self):
        for rel in NOTICE_FILES:
            lines = read(rel).splitlines()
            self.assertLess(next(i for i, l in enumerate(lines) if NOTICE in l), 14, rel)

    def test_every_privacy_page_carries_a_review_label(self):
        for rel in PRIVACY_PAGES:
            t = read("privacy/" + rel)
            self.assertTrue("Review label: community draft" in t or "Review label: **community draft" in t or NOTICE in t, rel)

    def test_notice_links_resolve(self):
        for rel in NOTICE_FILES:
            t = read(rel)
            block = t[t.index(NOTICE):].split("\n", 1)[0]
            link = block[block.index("](") + 2:block.index(")", block.index("]("))]
            self.assertTrue(os.path.isfile(os.path.normpath(os.path.join(ROOT, os.path.dirname(rel), link))), f"{rel}: {link}")


if __name__ == "__main__":
    unittest.main()
