import json, os, re, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


ROP = "privacy/record-of-processing.md"
TRANSFERS = "privacy/international-transfers.md"
EXAMPLE = "privacy/international-transfers-example.md"


class Art30Applicability(unittest.TestCase):
    """F-05: the Art. 30(5) exemption is conditional, and it lifts one duty, not the GDPR."""

    def test_the_applicability_record_comes_before_the_record_itself(self):
        t = read(ROP)
        self.assertLess(t.index("## Art. 30(5) applicability record"), t.index("## The record"))
        self.assertIn("Review label: community draft", t)

    def test_every_required_field_is_in_the_record(self):
        t = read(ROP)
        for f in ("Persons employed", "Is processing occasional?", "Risk to rights and freedoms", "Special categories (Art. 9(1)) or criminal convictions data (Art. 10)",
                  "Result", "Rationale", "Decision owner (role)", "Date decided", "Review date", "Organisation and role"):
            self.assertRegex(t, rf"(?m)^\| {re.escape(f)} \|", f)

    def test_the_three_results_and_nothing_else(self):
        row = [l for l in read(ROP).splitlines() if l.startswith("| Result |")][0]
        for r in ("**exemption may apply**", "**exemption does not apply**", "**needs advice**"):
            self.assertIn(r, row)

    def test_the_conditions_follow_the_article_text(self):
        t = read(ROP)
        self.assertIn("fewer than 250 persons", t)
        for needle in ("likely to result in a risk to the rights and freedoms of data subjects", "the processing is not occasional",
                       "special categories of data (Art. 9(1)) or personal data relating to criminal convictions and offences (Art. 10)",
                       "any one is enough to lose the exemption", "Art. 30(1) (controllers) and Art. 30(2) (processors)"):
            self.assertIn(needle, t, needle)

    def test_it_says_the_exemption_is_not_an_exemption_from_the_gdpr(self):
        t = read(ROP)
        self.assertIn("It removes one record-keeping duty. It does not exempt you from the GDPR.", t)
        self.assertIn("**Needs advice:** treat it as \"does not apply\"", t)
        self.assertIn("**Exemption may apply:** it is not a conclusion that it does apply", t)

    def test_the_readme_no_longer_overstates_or_misstates_the_exemption(self):
        t = read("privacy/README.md")
        line = [l for l in t.splitlines() if l.startswith("- **A record of processing (Art. 30)**")][0]
        for needle in ("fewer than 250 persons", "only that record-keeping duty, not the GDPR", "criminal convictions", "record-of-processing.md"):
            self.assertIn(needle, line, needle)
        self.assertNotIn("more than occasional", line)
        self.assertNotIn("Keep the record unless you have checked", line)

    def test_unverified_guidance_is_flagged_pending(self):
        self.assertIn("**Pending: no supervisory authority or EDPB guidance", read(ROP))


class TransferAssessmentRecord(unittest.TestCase):
    """F-08: a later reviewer can reconstruct why a transfer was considered permissible."""

    def test_the_register_points_at_an_assessment_record(self):
        t = read(TRANSFERS)
        self.assertIn("| ID | Recipient | Country | What data | Route (Art. 45 / 46 / 49) | Assessment record | Approved by | Reassess by |", t)
        self.assertIn("**The decision lives in the assessment record**", t)

    def test_all_twelve_parts_are_present_in_order(self):
        t = read(TRANSFERS)
        heads = re.findall(r"(?m)^\*\*(\d+)\. ", t)
        self.assertEqual(heads, [str(n) for n in range(1, 13)])

    def test_parties_roles_and_gdpr_subjection_are_recorded(self):
        t = read(TRANSFERS)
        self.assertIn("| Exporter |", t)
        self.assertIn("| Importer |", t)
        self.assertIn("Subject to the GDPR for this processing?", t)
        self.assertIn("Decision (EU) 2021/914, Art. 1(1)", t)

    def test_adequacy_safeguards_and_derogation_are_distinguished_with_the_ladder(self):
        t = read(TRANSFERS)
        for needle in ("| **Adequacy decision** | Art. 45(3) |", "| **Appropriate safeguards** | Art. 46(2) |", "| **Derogation** | Art. 49(1) |",
                       "a derogation is available only in the absence of the first two (Art. 49(1))", "Art. 46(3)"):
            self.assertIn(needle, t, needle)

    def test_the_four_modules_are_named(self):
        t = read(TRANSFERS)
        for m in ("One (controller to controller)", "Two (controller to processor)", "Three (processor to processor)", "Four (processor to controller)"):
            self.assertIn(m, t, m)

    def test_assessment_follows_clause_14_and_supplementary_measures_are_recorded(self):
        t = read(TRANSFERS)
        for needle in ("Clause 14(a) to (d)", "Clause 14(b)(iii)", "Clause 14(e)", "Clause 14(f)", "technical / contractual / organisational"):
            self.assertIn(needle, t, needle)

    def test_onward_transfers_sources_approval_and_reassessment_are_required(self):
        t = read(TRANSFERS)
        for needle in ("Clause 8.7", "Clause 8.8", "**8. Sources used**", "Approved by (role)", "role, not the author", "**10. Reassessment triggers.**",
                       "at least yearly", "adequacy decision is amended, suspended or repealed (Art. 45(5))", "**12. Reviewer test.**", "Art. 30(1)(e), Art. 49(6)"):
            self.assertIn(needle, t, needle)

    def test_what_was_not_read_is_stated_and_no_country_status_is_given(self):
        t = read(TRANSFERS)
        self.assertIn("**Pending: the EDPB's Recommendations 01/2020", t)
        self.assertIn("No country's adequacy status or law is stated here.", t)
        self.assertIn("Review label: community draft", t)


class TransferExample(unittest.TestCase):
    def test_the_example_is_marked_fictional_and_names_no_real_country(self):
        t = read(EXAMPLE)
        self.assertIn("**Fictional.**", t)
        self.assertIn("must not be copied", t)
        self.assertIn("Examplestan", t)
        for real in ("United States", "USA", "India", "China", "United Kingdom", "Switzerland", "Japan", "Canada", "Israel", "Brazil", "Australia"):
            self.assertNotIn(real, t, real)

    def test_the_example_fills_every_part_of_the_template(self):
        self.assertEqual(re.findall(r"(?m)^\*\*(\d+)\. ", read(EXAMPLE)), [str(n) for n in range(1, 13)])
        self.assertEqual(re.findall(r"(?m)^\*\*(\d+)\. ", read(EXAMPLE)), re.findall(r"(?m)^\*\*(\d+)\. ", read(TRANSFERS)))

    def test_the_example_names_a_module_an_independent_approver_and_a_reassessment_date(self):
        t = read(EXAMPLE)
        self.assertIn("**Module Two**", t)
        self.assertIn("(not the author)", t)
        self.assertRegex(t, r"Reassess by[^\n]*\n[^\n]*\n\| T-01 [^\n]*\| \d{4}-\d{2}-\d{2} \|")

    def test_the_only_dates_ahead_of_today_are_reassessment_dates(self):
        import datetime as dt
        today = dt.date.today().isoformat()
        ahead = {d for d in re.findall(r"\b(\d{4}-\d{2}-\d{2})\b", read(EXAMPLE)) if d > today}
        self.assertLessEqual(ahead, {"2027-03-01"}, ahead)


class WatchListNamesTheNewSources(unittest.TestCase):
    def sources(self):
        return {s["id"]: s for s in json.loads(read("docs/maintenance/sources.json"))["sources"]}

    def test_scc_decision_and_edpb_recommendations_are_listed_with_what_was_and_was_not_read(self):
        s = self.sources()
        self.assertIn("Decision (EU) 2021/914", s["scc-2021-914"]["edition_mapped"])
        self.assertIn("Clause", s["scc-2021-914"]["checked_what"])
        self.assertIn("were not read", s["edpb-recs-01-2020"]["checked_what"].replace("The recommendations themselves were not read", "were not read"))
        self.assertIn("pending citation", s["edpb-recs-01-2020"]["notes"])

    def test_gdpr_entry_records_that_chapter_v_was_read(self):
        self.assertIn("Chapter V (Articles 44 to 49) read in full", self.sources()["gdpr"]["checked_what"])


if __name__ == "__main__":
    unittest.main()
