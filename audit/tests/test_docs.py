import glob, os, re, unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
STATUS = re.compile(r"^\*\*Status:\*\* (UNTESTED|NOT APPLICABLE|TESTED on \d{4}-\d{2}-\d{2}|RAN, NO DATA on \d{4}-\d{2}-\d{2})\s*$", re.M)
PROVIDER_FILES = [f for f in glob.glob(os.path.join(ROOT, "verify", "*.md"))
                  if os.path.basename(f) not in ("README.md", "_template.md", "common.md")]
CONTROLS = [f"{n:02d}" for n in range(1, 13)]


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


class VerifyDocs(unittest.TestCase):
    def test_provider_files_exist(self):
        names = {os.path.basename(f) for f in PROVIDER_FILES}
        self.assertTrue({"aws.md", "gcp.md", "azure.md"} <= names, names)

    def test_every_provider_has_every_control_section(self):
        for f in PROVIDER_FILES + [os.path.join(ROOT, "verify", "_template.md")]:
            t = read(f)
            for c in CONTROLS:
                self.assertRegex(t, rf"(?m)^## {c} ", f"{os.path.basename(f)} lacks section {c}")

    def test_every_command_has_a_status_line(self):
        for f in PROVIDER_FILES + [os.path.join(ROOT, "verify", "common.md")]:
            t = read(f)
            blocks = len(re.findall(r"(?m)^```bash$", t))
            statuses = len(STATUS.findall(t))
            na = len(re.findall(r"\*\*Status:\*\* NOT APPLICABLE", t))
            self.assertEqual(statuses - na, blocks, f"{os.path.basename(f)}: {blocks} commands, {statuses - na} status lines")

    def test_untested_providers_claim_nothing(self):
        for name in ("gcp.md", "azure.md"):
            t = read(os.path.join(ROOT, "verify", name))
            self.assertNotRegex(t, r"\*\*Status:\*\* (TESTED|RAN)", name)

    def test_commands_are_read_only(self):
        banned = re.compile(r"\b(create|delete|put|update|modify|remove|terminate|start|stop|attach|detach|set-|add-|get-secret-value|secret show|versions access)\b")
        for f in PROVIDER_FILES + [os.path.join(ROOT, "verify", "common.md")]:
            for block in re.findall(r"(?s)```bash\n(.*?)\n```", read(f)):
                if block.startswith("("):
                    continue
                self.assertIsNone(banned.search(block), f"{os.path.basename(f)}: {block[:80]}")

    def test_every_control_links_to_verify(self):
        for f in glob.glob(os.path.join(ROOT, "controls", "[0-9][0-9]-*.md")):
            self.assertIn("## How to verify", read(f), os.path.basename(f))

    def test_no_broken_relative_links(self):
        bad = []
        for f in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
            t = re.sub(r"```.*?```", "", read(f), flags=re.S)
            for m in re.finditer(r"\[[^\]]*\]\(([^)#\s]+)(#[^)]*)?\)", t):
                u = m.group(1)
                if re.match(r"[a-z]+:", u):
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), u))):
                    bad.append((os.path.relpath(f, ROOT), u))
        self.assertEqual(bad, [])


class MappingsAndWorkflow(unittest.TestCase):
    def test_every_control_has_a_row_for_every_framework_with_status_edition_and_label(self):
        t = read(os.path.join(ROOT, "controls", "framework-mappings.md"))
        for c in CONTROLS:
            sec = re.search(rf"(?ms)^## {c} .*?(?=^## |\Z)", t)
            self.assertIsNotNone(sec, c)
            rows = [l for l in sec.group(0).splitlines() if l.startswith("| ") and not l.startswith("| Framework") and not l.startswith("|---")]
            self.assertGreaterEqual(len(rows), 4, c)
            for fw in ("SOC 2", "ISO/IEC 27001", "GDPR", "DORA"):
                self.assertTrue(any(r.startswith(f"| {fw}") for r in rows), (c, fw))
            for r in rows:
                self.assertRegex(r, r"(2017|2022|2016/679|2022/2554)", r)
                self.assertRegex(r, r"\| (covered in part|not covered|not applicable|not assessed|needs expert review) \|", r)
                self.assertIn("| community draft |", r, r)

    def test_nine_workflow_steps(self):
        t = read(os.path.join(ROOT, "workflow", "README.md"))
        self.assertEqual(len(re.findall(r"(?m)^\| \d \| \*\*", t)), 9)

    def test_every_control_lists_kinds_of_evidence(self):
        for f in glob.glob(os.path.join(ROOT, "controls", "[0-9][0-9]-*.md")):
            t = read(f)
            for word in ("Configuration:", "Operational:", "Effectiveness:", "Independent assurance:"):
                self.assertIn(word, t, os.path.basename(f))

    def test_remediation_standard_covers_the_required_topics(self):
        t = read(os.path.join(ROOT, "policies", "vulnerability-remediation-standard.md"))
        for h in ("discovered", "severity is assessed", "remediation times", "owns remediation", "Exceptions", "fixes are verified", "escalated"):
            self.assertIn(h, t)
        self.assertIn("illustrative", t)
        self.assertIn("actively exploited", t)


class TrustFiles(unittest.TestCase):
    def test_trust_files_exist(self):
        for f in ("LICENSE", "NOTICE", "SECURITY.md", "CONTRIBUTING.md", "VERSIONING.md", "CHANGELOG.md", "MAINTENANCE.md", "RELEASE.md", "VERSION",
                  ".github/pull_request_template.md", ".github/ISSUE_TEMPLATE/config.yml", ".github/ISSUE_TEMPLATE/bug_report.md",
                  ".github/ISSUE_TEMPLATE/new_control.md", ".github/ISSUE_TEMPLATE/doc_correction.md", ".github/ISSUE_TEMPLATE/provider_commands.md"):
            self.assertTrue(os.path.exists(os.path.join(ROOT, f)), f)

    def test_version_matches_the_newest_changelog_entry(self):
        v = read(os.path.join(ROOT, "VERSION")).strip()
        self.assertRegex(v, r"^\d+\.\d+\.\d+$")
        first = re.search(r"(?m)^## \[(\d+\.\d+\.\d+)\]", read(os.path.join(ROOT, "CHANGELOG.md")))
        self.assertEqual(first.group(1), v)

    def test_security_policy_gives_a_private_route_and_says_no_sla(self):
        t = read(os.path.join(ROOT, "SECURITY.md"))
        self.assertIn("Report a vulnerability", t)
        self.assertIn("Do not open a public issue with exploit details", t)
        self.assertIn("no service level agreement", t)

    def test_issue_templates_ask_for_sources_and_safe_reproduction(self):
        d = os.path.join(ROOT, ".github", "ISSUE_TEMPLATE")
        self.assertIn("authoritative source", read(os.path.join(d, "doc_correction.md")))
        self.assertIn("without sharing secrets", read(os.path.join(d, "bug_report.md")))
        self.assertIn("What evidence would show it works", read(os.path.join(d, "new_control.md")))
        self.assertIn("blank_issues_enabled: false", read(os.path.join(d, "config.yml")))

    def test_readme_answers_the_five_first_questions(self):
        t = read(os.path.join(ROOT, "README.md"))[:6000]
        for h in ("## What problem does it solve?", "## Who is it for?", "## What will you have when you finish?", "## How do I start?", "## What this project does not do"):
            self.assertIn(h, t)
        self.assertIn("does not guarantee compliance", t)

    def test_privacy_and_legal_material_tells_users_to_get_specialist_advice(self):
        readme = read(os.path.join(ROOT, "README.md"))
        self.assertIn("Get specialist advice", readme)
        self.assertIn("written by engineers, not lawyers", readme)
        priv = read(os.path.join(ROOT, "privacy", "README.md"))
        self.assertIn("Get specialist advice", priv)
        self.assertIn("not been reviewed by a privacy specialist", priv)
        self.assertIn("specialist advice", read(os.path.join(ROOT, "RELEASE.md")))

    def test_readme_supported_python_matches_ci(self):
        readme = read(os.path.join(ROOT, "README.md"))
        ci = read(os.path.join(ROOT, ".github", "workflows", "sanitise.yml"))
        for v in ("3.9", "3.10", "3.11", "3.12", "3.13"):
            self.assertIn(v, readme)
            self.assertIn(f'"{v}"', ci)


class GdprTerritorialScope(unittest.TestCase):
    """F-01: the location of the data subject must not be presented as the only test for GDPR scope."""

    def worksheet(self):
        return read(os.path.join(ROOT, "scoping", "gdpr-territorial-scope.md"))

    def test_three_routes_and_the_unclear_case_are_distinguished(self):
        t = self.worksheet()
        for needle in ("Art. 3(1)", "Art. 3(2)(a)", "Art. 3(2)(b)", "Art. 3(3)", "Needs advice", "needs advice", "not the only test",
                       "whether or not the processing takes place in the Union", "irrespective of whether a payment is required"):
            self.assertIn(needle, t, needle)

    def test_it_asks_about_an_eu_representative(self):
        t = self.worksheet()
        self.assertIn("Article 27", t)
        self.assertIn("representative", t)

    def test_it_is_labelled_community_draft_and_cites_sources(self):
        t = self.worksheet()
        self.assertIn("Review label: community draft", t)
        self.assertIn("Regulation (EU) 2016/679", t)
        self.assertIn("Official Journal", t)
        self.assertIn("Guidelines 3/2018", t)
        self.assertIn("source verification pending", t)

    def test_it_never_states_a_legal_conclusion(self):
        t = self.worksheet()
        for banned in ("you are subject to", "you are not subject", "you are exempt", "GDPR applies to you", "GDPR does not apply to you", "you are out of scope", "you are in scope"):
            self.assertNotIn(banned, t, banned)
        self.assertIn("not a finding that the GDPR does not apply", t)

    def test_the_old_one_line_rule_is_gone_everywhere(self):
        old = ("personal data of people in the EU/EEA, or you are established", "You process personal data of people in the EU |",
               "teams established in, or serving people", "personal data of people in the EU or EEA, and anywhere")
        for f in ("scoping/applicability-matrix.md", "guide/roadmap.md", "privacy/README.md", "controls/08-data-protection.md", "controls/controls.json"):
            t = read(os.path.join(ROOT, f))
            for o in old:
                self.assertNotIn(o, t, f"{f}: {o}")

    def test_every_place_that_states_the_rule_points_to_the_worksheet(self):
        for f in ("scoping/applicability-matrix.md", "guide/roadmap.md", "privacy/README.md", "controls/08-data-protection.md", "scoping/questionnaire.md"):
            self.assertIn("gdpr-territorial-scope", read(os.path.join(ROOT, f)), f)

    def test_questionnaire_asks_the_establishment_offering_and_monitoring_questions(self):
        t = read(os.path.join(ROOT, "scoping", "questionnaire.md"))
        self.assertIn("## 4a. GDPR territorial scope", t)
        for q in ("establishment in the Union", "offer goods or services", "monitor the behaviour", "controller, a processor", "EU representative"):
            self.assertIn(q, t, q)


class DoraObligationTypes(unittest.TestCase):
    """F-02: direct duties, contractual flow-down and oversight obligations must not be conflated."""

    TYPES = ("direct statutory duty", "contractual flow-down", "oversight obligation")

    def test_screening_page_separates_the_three_kinds_with_sources(self):
        t = read(os.path.join(ROOT, "scoping", "dora-screening.md"))
        for needle in ("Direct statutory duty", "Contractual flow-down", "Oversight obligation", "Article 2(1)", "Article 30", "Article 31",
                       "Review label: community draft", "Regulation (EU) 2022/2554", "source verification pending",
                       "ICT third-party service providers", "fully responsible", "Needs advice", "needs advice"):
            self.assertIn(needle, t, needle)

    def test_screening_page_does_not_state_a_legal_conclusion(self):
        t = read(os.path.join(ROOT, "scoping", "dora-screening.md"))
        for banned in ("DORA applies to you", "DORA does not apply to you", "you are subject to DORA", "you are exempt"):
            self.assertNotIn(banned, t, banned)
        self.assertIn("Not a finding that DORA is irrelevant to you", t.replace("**", ""))

    def test_matrix_has_three_dora_rows_each_with_one_exact_obligation_type(self):
        t = read(os.path.join(ROOT, "scoping", "applicability-matrix.md"))
        self.assertIn("| Item | Obligation type |", t)
        rows = [l for l in t.splitlines() if l.startswith("| **DORA")]
        self.assertEqual(len(rows), 3, rows)
        found = sorted(r.split("|")[2].strip().lower() for r in rows)
        self.assertEqual(found, sorted(self.TYPES))
        self.assertNotIn("(directly or through contract flow-down)", t)

    def test_every_dora_mapping_row_carries_an_obligation_type_from_the_vocabulary(self):
        t = read(os.path.join(ROOT, "controls", "framework-mappings.md"))
        rows = [l for l in t.splitlines() if l.startswith("| DORA (Regulation")]
        self.assertGreaterEqual(len(rows), 12)
        for r in rows:
            labels = re.findall(r"\*\*([a-z -]+)\*\*", r.split("|")[2])
            self.assertTrue(labels, r)
            for lab in labels:
                self.assertTrue(any(lab.startswith(v) for v in self.TYPES), (lab, r))
            self.assertNotIn("Only if in scope", r)

    def test_contract_articles_are_never_labelled_as_direct_duties(self):
        t = read(os.path.join(ROOT, "controls", "framework-mappings.md"))
        for r in (l for l in t.splitlines() if l.startswith("| DORA (Regulation")):
            ref = r.split("|")[2]
            if "Art. 30" in ref:
                self.assertIn("contractual flow-down", ref, r)

    def test_other_places_do_not_present_dora_as_applying_to_providers_by_default(self):
        layers = read(os.path.join(ROOT, "guide", "layers-and-outcomes.md"))
        self.assertIn("contract terms", layers)
        self.assertIn("dora-screening", layers)
        self.assertIn("dora-screening", read(os.path.join(ROOT, "scripts", "kit_start.py")))


class BreachRoles(unittest.TestCase):
    """F-06: controller and processor breach duties must be kept apart, and contract terms kept apart from statute."""

    RUNBOOK = "runbooks/incident-response.md"

    def test_runbook_has_a_role_decision_tree(self):
        t = read(os.path.join(ROOT, self.RUNBOOK))
        for needle in ("We are a processor for the affected data", "We are the controller", "We are both", "Joint controllers, or the roles are unclear",
                       "route to legal review", "Art. 4(7)", "Art. 4(8)", "Art. 4(12)", "4A. Processor path", "4B. Controller path"):
            self.assertIn(needle, t, needle)

    def test_processor_has_no_72_hour_deadline_in_article_33(self):
        t = read(os.path.join(ROOT, self.RUNBOOK))
        self.assertIn("Article 33 gives the processor no 72-hour deadline", t)
        self.assertIn("Art. 33(2)", t)
        self.assertIn("without undue delay after becoming aware", t)

    def test_contract_deadlines_are_separate_from_statutory_ones(self):
        t = read(os.path.join(ROOT, self.RUNBOOK))
        self.assertIn("contract term, not a statutory deadline", t)
        self.assertIn("Processor notification deadline in the contract", t)

    def test_runbook_records_awareness_decision_log_and_escalation_contacts(self):
        t = read(os.path.join(ROOT, self.RUNBOOK))
        for needle in ("became aware", "how that was decided", "Decision log", "Escalation contacts", "Basis (article, contract clause, or reasoning)"):
            self.assertIn(needle, t, needle)

    def test_runbook_assesses_whether_individuals_must_be_told(self):
        t = read(os.path.join(ROOT, self.RUNBOOK))
        for needle in ("Assess whether affected people must be told", "Art. 34(1)", "Art. 34(3)", "Art. 34(4)", "unintelligible", "disproportionate effort"):
            self.assertIn(needle, t, needle)

    def test_runbook_mentions_other_regimes_and_links_the_matrix(self):
        t = read(os.path.join(ROOT, self.RUNBOOK))
        self.assertIn("Other incident reporting regimes may apply", t)
        self.assertIn("applicability-matrix.md", t)

    def test_runbook_is_labelled_community_draft_with_sources(self):
        t = read(os.path.join(ROOT, self.RUNBOOK))
        self.assertIn("Review label: community draft", t)
        self.assertIn("Get specialist advice", t)
        self.assertIn("Official Journal", t)

    def test_every_72_hour_statement_is_in_a_controller_context(self):
        files = (self.RUNBOOK, "privacy/README.md", "controls/08-data-protection.md", "controls/09-incident-response.md", "evidence/incident-report.md")
        for f in files:
            heading = ""
            for line in read(os.path.join(ROOT, f)).splitlines():
                if line.startswith("#"):
                    heading = line
                if re.search(r"72[- ]hours?", line):
                    self.assertTrue("controller" in line.lower() or "controller" in heading.lower(), f"{f}: {line[:100]}")

    def test_no_document_applies_the_72_hours_to_everyone(self):
        for f in (self.RUNBOOK, "privacy/README.md", "controls/08-data-protection.md", "controls/09-incident-response.md", "evidence/incident-report.md"):
            t = read(os.path.join(ROOT, f))
            self.assertNotIn("Within 72 hours of awareness, unless", t, f)
            self.assertNotIn("The 72-hour clock for a personal-data breach starts at awareness", t, f)

    def test_control_09_is_role_aware(self):
        t = read(os.path.join(ROOT, "controls", "09-incident-response.md"))
        self.assertIn("by role", t)
        self.assertIn("processor", t)
        self.assertIn("contractual deadlines separate from statutory ones", t)
        self.assertIn("tabletop-incident-notification", t)

    def test_templates_capture_awareness_role_and_contract_deadlines(self):
        rep = read(os.path.join(ROOT, "evidence", "incident-report.md"))
        for needle in ("Aware (UTC)", "How awareness was decided", "Role for the affected personal data", "Contractual notification deadlines",
                       "Never record a contract term as a statutory deadline"):
            self.assertIn(needle, rep, needle)
        reg = read(os.path.join(ROOT, "evidence", "incident-register.md"))
        self.assertIn("became aware", reg)
        self.assertIn("keep contractual deadlines separate from statutory ones", reg)


class TabletopExercise(unittest.TestCase):
    PATH = "runbooks/tabletop-incident-notification.md"

    def test_three_scenarios_with_questions_and_expected_answers(self):
        t = read(os.path.join(ROOT, self.PATH))
        for h in ("## Scenario A: processor breach discovered", "## Scenario B: controller breach, low risk", "## Scenario C: controller breach, high risk to individuals"):
            self.assertIn(h, t, h)
        self.assertEqual(t.count("**Expected answers**"), 3)
        self.assertEqual(t.count("**Questions**"), 3)

    def test_it_teaches_contract_versus_statute(self):
        t = read(os.path.join(ROOT, self.PATH))
        self.assertIn("contractual", t)
        self.assertIn("statutory", t)
        self.assertIn("24 hours", t)
        self.assertIn("does not replace or relax the statutory duty", t)
        self.assertIn("**None.**", t)    # the processor has no Art. 33(1) 72-hour rule
        self.assertIn("Monday 17:30 UTC", t)
        self.assertIn("does not apply", t)  # Art. 34(3)(a) encryption exception
        self.assertIn("Review label: community draft", t)
        self.assertIn("Get specialist advice", t)

    def test_the_runbook_links_the_tabletop(self):
        self.assertIn("tabletop-incident-notification", read(os.path.join(ROOT, "runbooks", "incident-response.md")))
        self.assertIn("tabletop-incident-notification", read(os.path.join(ROOT, "runbooks", "README.md")) + read(os.path.join(ROOT, "runbooks", "incident-response.md")))


class ReviewLabelsAndStatuses(unittest.TestCase):
    """F-12 and F-14: the label shown must match the review actually done; gaps and exclusions must be distinct."""

    DOC = "docs/review-labels.md"
    STATUSES = {"covered", "covered in part", "not covered", "not applicable", "not assessed", "needs expert review"}

    def doc(self):
        return read(os.path.join(ROOT, self.DOC))

    def test_three_labels_defined_exactly(self):
        t = self.doc()
        for needle in ("**Community draft**", "**Maintainer reviewed**", "**Specialist reviewed**",
                       "Proposed. Formatting and basic automated checks may have passed.", "It does **not** mean substantively verified.",
                       "Source and reasoning checked; limitations documented.", "It does **not** mean legal or specialist approval.",
                       "A qualified reviewer examined the material within a recorded scope.",
                       "It does **not** mean a guarantee of compliance. Only the reviewed material is covered."):
            self.assertIn(needle, t, needle)
        self.assertEqual(len(re.findall(r"(?m)^\| \*\*(Community draft|Maintainer reviewed|Specialist reviewed)\*\* \|", t)), 3)

    def test_ci_and_maintainer_approval_do_not_imply_specialist_approval(self):
        t = self.doc()
        self.assertIn("Passing CI, or a maintainer's approval of a pull request, does not imply legal or specialist approval", t)
        self.assertIn("Never record a reviewer, a review date or a stronger label that did not happen", t)

    def test_exactly_six_coverage_statuses_and_covered_needs_a_reviewed_label(self):
        sec = self.doc().split("## Coverage statuses")[1].split("How to tell a gap")[0]
        found = {m.lower() for m in re.findall(r"(?m)^\| \*\*([a-z ]+)\*\* \|", sec)}
        self.assertEqual(found, self.STATUSES)
        self.assertIn("There is **no seventh status**", sec)
        self.assertIn("allowed only on a record labelled maintainer reviewed or specialist reviewed", sec)
        row = [l for l in sec.splitlines() if l.startswith("| **covered** |")][0]
        self.assertIn("does **not** mean you meet the requirement", row)

    def test_blank_values_and_silence_are_not_statuses(self):
        t = self.doc()
        self.assertIn("A **blank value is not allowed**", t)
        self.assertIn("silence must never be read as a status", t)

    def test_rationale_required_for_not_covered_and_not_applicable(self):
        sec = self.doc().split("## Coverage statuses")[1]
        for status in ("not covered", "not applicable"):
            row = [l for l in sec.splitlines() if l.startswith(f"| **{status}**")][0]
            self.assertIn("| **Yes** |", row, status)

    def test_gap_versus_exclusion_is_explained(self):
        t = self.doc()
        self.assertIn("**not covered** is an actual gap", t)
        self.assertIn("**not applicable** is a deliberate, documented exclusion", t)
        self.assertIn("**not assessed** is neither", t)

    def test_current_position_is_community_draft(self):
        t = self.doc()
        self.assertIn("All compliance content in this kit is a **community draft**", t)
        self.assertIn("no mapping, guide or template carries the label", t)

    def test_contributing_and_templates_start_as_community_draft_and_say_ci_is_not_approval(self):
        c = read(os.path.join(ROOT, "CONTRIBUTING.md"))
        self.assertIn("community draft", c)
        self.assertIn("docs/review-labels.md", c)
        self.assertIn("does not imply legal or specialist approval", c)
        for f in (".github/pull_request_template.md", ".github/ISSUE_TEMPLATE/new_control.md", ".github/ISSUE_TEMPLATE/doc_correction.md",
                  ".github/ISSUE_TEMPLATE/provider_commands.md"):
            t = read(os.path.join(ROOT, f))
            self.assertIn("community draft", t, f)
            self.assertIn("does not imply legal or specialist approval", t, f)
            self.assertIn("review-labels.md", t, f)

    def test_linked_from_readme_mappings_and_matrix(self):
        self.assertIn("docs/review-labels.md", read(os.path.join(ROOT, "README.md")))
        self.assertIn("All compliance content is currently a community draft", read(os.path.join(ROOT, "README.md")))
        self.assertIn("review-labels.md", read(os.path.join(ROOT, "controls", "framework-mappings.md")))
        self.assertIn("review-labels.md", read(os.path.join(ROOT, "scoping", "applicability-matrix.md")))

    def test_mappings_do_not_overstate_review(self):
        t = read(os.path.join(ROOT, "controls", "framework-mappings.md"))
        self.assertIn("Review label for every record: community draft", t)
        self.assertIn("Coverage statuses are the authors' draft judgements and none has been reviewed", t)
        self.assertIn("It is not a statement that you meet the requirement", t)
        self.assertIn("has simply **not been assessed**", t)
        self.assertNotIn("by the authors, against the editions above", t)
        self.assertNotIn("Last reviewed", t)
        for row in (l for l in t.splitlines() if l.startswith("| ") and "| Framework (edition)" not in l and not l.startswith("|---")):
            if row.count("|") >= 8:
                self.assertNotIn("maintainer reviewed", row)
                self.assertNotIn("specialist reviewed", row)

    def test_matrix_separates_applicability_from_coverage(self):
        t = read(os.path.join(ROOT, "scoping", "applicability-matrix.md"))
        self.assertIn("Applicability is not coverage", t)
        self.assertIn("has not been assessed", t)

    def test_changelog_does_not_claim_a_review_that_did_not_happen(self):
        t = read(os.path.join(ROOT, "CHANGELOG.md"))
        self.assertNotIn("Framework mappings reviewed by the authors", t)
        self.assertIn("no row reviewed by a maintainer or a specialist", t)


class ContactAndNames(unittest.TestCase):
    ADDRESS = "compliance" + "@" + "capitalsnapshot" + ".com"    # built from parts so this file does not itself carry the address

    def walk(self):
        for dirpath, dirs, names in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "tests", "__pycache__")]
            for n in names:
                p = os.path.join(dirpath, n)
                try:
                    yield os.path.relpath(p, ROOT), read(p)
                except (UnicodeDecodeError, OSError):
                    continue

    def test_maintenance_has_exactly_one_contact_line_naming_the_role_mailbox(self):
        t = read(os.path.join(ROOT, "MAINTENANCE.md"))
        lines = [l for l in t.splitlines() if self.ADDRESS in l]
        self.assertEqual(len(lines), 1, lines)
        self.assertTrue(lines[0].startswith("**Contact:**"))
        for needle in ("role mailbox", "not a person", "source updates", "review"):
            self.assertIn(needle, lines[0])

    def test_the_mailbox_is_a_role_and_is_the_only_address_in_the_repository(self):
        self.assertTrue(self.ADDRESS.startswith("compliance@"))
        found = {}
        for rel, text in self.walk():
            if rel.startswith("skills/"):
                continue
            for m in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", text):
                found.setdefault(m, []).append(rel)
        self.assertEqual(set(found), {self.ADDRESS}, found)
        self.assertEqual(found[self.ADDRESS], ["MAINTENANCE.md"])

    def test_the_domain_appears_nowhere_else(self):
        for rel, text in self.walk():
            if rel.startswith("skills/") or rel == "MAINTENANCE.md":
                continue
            self.assertNotIn("capitalsnapshot" + ".com", text.lower(), rel)

    def test_the_watch_list_names_roles_not_people(self):
        for s in read_json_sources():
            self.assertNotIn("@", s["owner"])
            self.assertNotRegex(s["owner"], r"^[A-Z][a-z]+ [A-Z][a-z]+$", s["owner"])    # not a "First Last" name


def read_json_sources():
    import json
    with open(os.path.join(ROOT, "docs", "maintenance", "sources.json"), encoding="utf-8") as fh:
        return json.load(fh)["sources"]


if __name__ == "__main__":
    unittest.main()
