import json, os, re, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


WS = "scoping/extensions/nis2-screening.md"
README = "scoping/extensions/README.md"


class ExtensionArea(unittest.TestCase):
    def test_the_extension_area_states_its_boundaries(self):
        t = read(README)
        for needle in ("An extension is a screening aid.", "The kit does not assess compliance with any extension regime.",
                       "Nothing here is mapped to controls", "National law decides.", "does not state the transposition status of any Member State",
                       "Review label: community draft"):
            self.assertIn(needle, t, needle)

    def test_extensions_are_separate_from_the_core_mappings(self):
        recs = json.loads(read("controls/mappings.json"))["records"]
        self.assertEqual({r["framework"] for r in recs}, {"SOC 2", "ISO/IEC 27001", "GDPR", "DORA"})
        self.assertFalse(any("NIS2" in json.dumps(r) for r in recs))

    def test_scoping_readme_points_to_extensions(self):
        self.assertIn("extensions/README.md", read("scoping/README.md"))


class Nis2Worksheet(unittest.TestCase):
    def setUp(self):
        self.t = read(WS)

    def test_states_plainly_that_the_kit_does_not_assess_nis2_compliance(self):
        self.assertIn("**The kit does not assess NIS2 compliance.**", self.t)
        self.assertIn("Review label: community draft", self.t)

    def test_all_the_required_things_are_recorded(self):
        for h in ("## 1. Sector, subsector and type of entity", "## 2. Size", "## 3. Routes that do not depend on size", "## 4. Exceptions and exclusions",
                  "## 5. Jurisdiction and registration", "## 6. National law for each Member State involved", "## 7. Outcome"):
            self.assertIn(h, self.t, h)
        for field in ("Annex and sector", "Subsector and type of entity", "Persons employed", "Main establishment in the Union",
                      "| Member State | National law (name and reference) | Status as you found it | Date checked | Source (link) |",
                      "Legal review outcome", "Reviewer (role)"):
            self.assertIn(field, self.t, field)

    def test_the_three_outcomes_and_nothing_else(self):
        sec = self.t.split("## 7. Outcome")[1].split("| Field | Entry |")[0]
        found = re.findall(r"(?m)^\| \*\*([^*]+)\*\* \|", sec)
        self.assertEqual(found, ["Potentially in scope", "Not in scope based on a documented assessment", "Requires advice"])

    def test_not_in_scope_needs_a_rationale_a_reviewer_and_no_unsure_answers(self):
        row = [l for l in self.t.splitlines() if l.startswith("| **Not in scope based on a documented assessment**")][0]
        for needle in ("**no answer is \"unsure\"**", "**each** Member State involved", "**written rationale**", "**reviewer**", "use \"requires advice\""):
            self.assertIn(needle, row, needle)

    def test_unsure_or_blank_defaults_to_requires_advice(self):
        self.assertIn("Any \"unsure\" or blank in sections 1 to 6 means the outcome is **requires advice**.", self.t)
        self.assertIn("This is the default.", self.t)

    def test_no_member_state_transposition_status_is_stated(self):
        self.assertIn("does not state the transposition status of any Member State", self.t)
        self.assertIn("That date does not tell you whether a given Member State has done so.", self.t)
        sec = self.t.split("## 6. National law")[1].split("## 7.")[0]
        rows = [l for l in sec.splitlines() if l.startswith("| <...>")]
        self.assertEqual(len(rows), 1)                                    # the row is blank for the user to fill in
        for member_state in ("Ireland", "Germany", "France", "Netherlands", "Spain", "Italy", "Belgium", "Poland", "Sweden", "Denmark"):
            self.assertNotIn(member_state, self.t, member_state)

    def test_size_text_follows_the_recommendation_and_covers_partner_and_linked_enterprises(self):
        for needle in ("fewer than 250 persons", "EUR 50 million", "EUR 43 million", "fewer than 50 persons", "EUR 10 million", "fewer than 10 persons",
                       "EUR 2 million", "Partner and linked enterprises count", "Art. 2(1), second subparagraph"):
            self.assertIn(needle, self.t, needle)

    def test_size_independent_routes_exceptions_and_jurisdiction_follow_the_directive(self):
        for needle in ("Art. 2(2)(a)", "Art. 2(2)(f)", "Art. 2(3)", "Art. 2(4)", "Art. 2(7) and (8)", "Art. 2(9)", "Art. 2(10)", "Art. 2(5)",
                       "Art. 26(1)", "Art. 26(2)", "Art. 26(3)", "Art. 27"):
            self.assertIn(needle, self.t, needle)

    def test_it_does_not_claim_a_software_vendor_is_or_is_not_a_listed_type(self):
        self.assertIn("The Directive does not list \"software vendor\" or \"SaaS provider\" as a type.", self.t)
        self.assertIn("**If it is not clear, answer \"unsure\".**", self.t)

    def test_customer_flow_down_is_a_contract_request_not_a_direct_duty(self):
        self.assertIn("Art. 21(2)(d)", self.t)
        self.assertIn("That is a contractual request, not a direct duty on you under the Directive.", self.t)

    def test_what_was_not_read_is_listed_as_pending(self):
        self.assertIn("**Pending:**", self.t)
        self.assertIn("were **not read**", self.t)


class ShallowStatementReplaced(unittest.TestCase):
    def test_the_matrix_row_links_the_worksheet_and_drops_the_size_class_shorthand(self):
        row = [l for l in read("scoping/applicability-matrix.md").splitlines() if l.startswith("| **NIS2**")][0]
        self.assertIn("extensions/nis2-screening.md", row)
        self.assertIn("**Not assessed by the kit.**", row)
        self.assertIn("does not assess NIS2 compliance", row)
        self.assertIn("national law of a Member State", row)
        self.assertNotIn("covered sector and size class", row)
        self.assertNotIn("some digital providers and managed service providers do", row)

    def test_the_questionnaire_links_the_worksheet_and_the_three_outcomes(self):
        t = read("scoping/questionnaire.md")
        self.assertIn("extensions/nis2-screening.md", t)
        for o in ("potentially in scope", "not in scope based on a documented assessment", "requires advice"):
            self.assertIn(o, t, o)

    def test_every_nis2_link_resolves(self):
        for f in ("scoping/applicability-matrix.md", "scoping/questionnaire.md", "scoping/README.md", README, WS):
            base = os.path.dirname(os.path.join(ROOT, f))
            for target in re.findall(r"\]\(([^)#]+?\.md)\)", read(f)):
                self.assertTrue(os.path.exists(os.path.normpath(os.path.join(base, target))), (f, target))


class Nis2SourceRecords(unittest.TestCase):
    def sources(self):
        return {s["id"]: s for s in json.loads(read("docs/maintenance/sources.json"))["sources"]}

    def test_nis2_was_read_and_says_what_was_not(self):
        s = self.sources()["nis2"]
        self.assertIsNotNone(s["last_checked"])
        self.assertIn("Annexes I and II", s["checked_what"])
        self.assertIn("scoping/extensions/nis2-screening.md", s["documents"])
        self.assertIn("National transposition is not tracked", s["notes"])
        self.assertIn("were not read", s["notes"])

    def test_the_size_recommendation_is_listed_as_a_source(self):
        s = self.sources()["recommendation-2003-361"]
        self.assertIn("Articles 4 to 6", s["notes"])
        self.assertIn("scoping/extensions/nis2-screening.md", s["documents"])


if __name__ == "__main__":
    unittest.main()
