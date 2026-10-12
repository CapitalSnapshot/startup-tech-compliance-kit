import importlib.util, itertools, json, os, subprocess, sys, tempfile, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
spec = importlib.util.spec_from_file_location("dpia_screen", os.path.join(ROOT, "scripts", "dpia_screen.py"))
ds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ds)


def base(**kw):
    with open(os.path.join(ROOT, "privacy", "dpia-answers.example.json"), encoding="utf-8") as fh:
        a = json.load(fh)
    a.update(kw)
    return a


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as fh:
        return fh.read()


class ScreeningLogic(unittest.TestCase):
    def test_example_answers_give_a_reasoned_may_not_outcome(self):
        r = ds.screen(base())
        self.assertEqual(r["outcome"], ds.MAY_NOT)
        self.assertTrue(r["record_complete"])
        self.assertEqual(r["score"], 0)
        self.assertIn("not a conclusion", " ".join(r["reasons"]))
        self.assertTrue(r["score_is_not_a_legal_threshold"])

    def test_each_serious_indicator_alone_is_enough_whatever_the_score(self):
        for key in ds.SERIOUS:
            r = ds.screen(base(**{key: "yes"}))
            self.assertEqual(r["outcome"], ds.LIKELY, key)
            self.assertEqual(r["score"], 0, key)   # a score of zero must not dismiss it

    def test_unsure_on_a_serious_indicator_counts_as_a_hit(self):
        self.assertEqual(ds.screen(base(art35_3a="unsure"))["outcome"], ds.LIKELY)

    def test_a_score_can_never_override_a_serious_indicator(self):
        factors = list(ds.FACTORS)
        for serious in ds.SERIOUS:
            for combo in itertools.product(("yes", "no", "unsure"), repeat=len(factors)):
                a = base(**{serious: "yes"}, **dict(zip(factors, combo)))
                self.assertEqual(ds.screen(a)["outcome"], ds.LIKELY, (serious, combo))

    def test_one_risk_factor_is_not_enough_for_recommended(self):
        self.assertEqual(ds.screen(base(vulnerable_people="yes"))["outcome"], ds.MAY_NOT)

    def test_many_low_indicators_recommend_a_dpia(self):
        r = ds.screen(base(vulnerable_people="yes", innovative_technology="yes", combining_datasets="yes", blocks_a_right="yes"))
        self.assertEqual(r["outcome"], ds.RECOMMENDED)
        self.assertEqual(r["score"], 4)

    def test_two_factors_recommend_and_unsure_counts_as_a_factor(self):
        self.assertEqual(ds.screen(base(vulnerable_people="yes", innovative_technology="unsure"))["outcome"], ds.RECOMMENDED)

    def test_missing_context_fields_block_a_may_not_outcome(self):
        for field in ds.FIELDS:
            a = base()
            a[field] = ""
            r = ds.screen(a)
            self.assertEqual(r["outcome"], ds.INCOMPLETE, field)
            self.assertIn(field, r["missing"])
            self.assertFalse(r["record_complete"])

    def test_missing_authority_list_prevents_may_not(self):
        a = base(authority_name="", authority_list_name="", authority_list_checked_on="")
        r = ds.screen(a)
        self.assertEqual(r["outcome"], ds.INCOMPLETE)
        self.assertEqual({"authority_name", "authority_list_name", "authority_list_checked_on"}, set(r["missing"]))

    def test_an_unanswered_indicator_is_incomplete(self):
        a = base()
        del a["combining_datasets"]
        self.assertEqual(ds.screen(a)["outcome"], ds.INCOMPLETE)

    def test_placeholders_count_as_missing(self):
        self.assertEqual(ds.screen(base(purposes="<...>"))["outcome"], ds.INCOMPLETE)

    def test_a_serious_indicator_wins_even_when_the_record_is_incomplete(self):
        r = ds.screen(base(art35_3c="yes", purposes=""))
        self.assertEqual(r["outcome"], ds.LIKELY)
        self.assertFalse(r["record_complete"])

    def test_an_invalid_answer_is_rejected(self):
        with self.assertRaises(ValueError):
            ds.screen(base(art35_3a="maybe"))

    def test_the_decision_record_carries_owner_date_and_review_date(self):
        r = ds.screen(base())
        self.assertEqual(set(r["decision"]), {"decision_owner", "decision_date", "review_date"})
        self.assertTrue(all(r["decision"].values()))


class CommandLine(unittest.TestCase):
    def run_cli(self, data, *extra):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "a.json")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(data if isinstance(data, str) else json.dumps(data))
            r = subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts", "dpia_screen.py"), p, *extra], capture_output=True, text=True)
            return r.returncode, r.stdout, r.stderr

    def test_json_and_markdown_output(self):
        rc, out, _ = self.run_cli(base())
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["outcome"], ds.MAY_NOT)
        rc, out, _ = self.run_cli(base(art35_3b="yes"), "--markdown")
        self.assertIn("**DPIA likely required or seek advice**", out)
        self.assertIn("not a legal threshold", out)

    def test_bad_input_exits_2_with_a_message(self):
        for bad in ("not json", "[1, 2]", json.dumps(base(art35_3a="maybe"))):
            rc, _, err = self.run_cli(bad)
            self.assertEqual(rc, 2, bad)
            self.assertIn("error:", err)


class Page(unittest.TestCase):
    def test_page_is_labelled_a_preliminary_screening_not_a_legal_threshold(self):
        t = read("privacy/dpia-screening.md")
        self.assertIn("not a legal threshold", t)
        self.assertIn("preliminary screening", t.lower())
        self.assertIn("Review label: community draft", t)
        self.assertNotIn("Rule of thumb", t)
        self.assertNotIn("two or more \"yes\" answers usually mean", t)

    def test_page_cites_the_articles_and_marks_unverified_sources(self):
        t = read("privacy/dpia-screening.md")
        for n in ("35(1)", "35(3)", "35(4)", "35(7)", "35(11)", "36(1)", "Official Journal", "Source verification pending", "Maintainer review needed"):
            self.assertIn(n, t, n)

    def test_page_says_a_serious_indicator_beats_a_low_score(self):
        t = read("privacy/dpia-screening.md")
        self.assertIn("A low score never overrides a serious indicator", t)
        self.assertIn("Any one", t)

    def test_page_requires_the_context_and_authority_fields_and_a_reviewable_record(self):
        t = read("privacy/dpia-screening.md")
        for f in ("Context", "Nature", "Scope", "Purposes", "Affected people", "Severity of potential harm", "Likelihood of that harm",
                  "Supervisory authority consulted", "Decision owner", "Decision date", "Review date"):
            self.assertIn(f, t, f)

    def test_page_and_script_use_the_same_outcome_labels(self):
        t = read("privacy/dpia-screening.md")
        for label in (ds.LIKELY, ds.RECOMMENDED, ds.MAY_NOT, ds.INCOMPLETE):
            self.assertIn(label, t, label)

    def test_other_documents_no_longer_ask_for_a_yes_no_answer(self):
        t = read("privacy/privacy-by-design-review.md")
        self.assertNotIn("<Yes / No>", t.split("DPIA")[1][:200])
        self.assertIn("not a legal threshold", read("privacy/README.md"))


if __name__ == "__main__":
    unittest.main()
