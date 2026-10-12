import importlib.util, json, os, re, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ci = load("controls_index", "scripts/controls_index.py")
ka = load("kit_audit", "audit/kit-audit.py")


class ControlStructure(unittest.TestCase):
    def setUp(self):
        self.controls = json.load(open(os.path.join(ROOT, "controls", "controls.json"), encoding="utf-8"))["controls"]

    def test_twelve_controls_with_every_field(self):
        self.assertEqual(len(self.controls), 12)
        for c in self.controls:
            for k in ("id", "evidence_number", "applies_to", "owner", "review_frequency", "limitations", "objective", "freshness_days"):
                self.assertTrue(c[k], f"{c['file']}: {k}")
            self.assertTrue(c["done_when"], c["file"])
            for kind, text in c["evidence_kinds"].items():
                self.assertTrue(text, f"{c['file']}: {kind}")
            self.assertTrue(c["indicative_references"], c["file"])

    def test_ids_are_stable_looking_and_unique(self):
        ids = [c["id"] for c in self.controls]
        self.assertEqual(len(ids), len(set(ids)))
        for i in ids:
            self.assertRegex(i, r"^KIT-[A-Z]{3}-\d{2}$")

    def test_index_is_up_to_date_with_the_markdown(self):
        self.assertEqual(ci.main(["--check"]), 0)

    def test_review_frequency_matches_the_audits_freshness_limits(self):
        for c in self.controls:
            name, limit = ka.CONTROLS[c["evidence_number"]]
            self.assertEqual(c["freshness_days"], limit, c["file"])
            self.assertEqual(c["title"], name, c["file"])

    def test_every_limitation_says_what_the_evidence_does_not_prove(self):
        for c in self.controls:
            self.assertGreater(len(c["limitations"]), 40, c["file"])


if __name__ == "__main__":
    unittest.main()
