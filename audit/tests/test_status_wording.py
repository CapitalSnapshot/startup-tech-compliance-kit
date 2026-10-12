import ast, contextlib, copy, glob, importlib.util, io, itertools, json, os, re, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
PY = [sys.executable, "-I"]


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


PHRASES = json.loads(read("scripts/prohibited_phrases.json"))["phrases"]


def hits(text):
    """Prohibited phrases found in text. Multi-word phrases match as substrings; single words match as whole words."""
    t = text.lower()
    found = []
    for p in PHRASES:
        if " " in p or "-" in p:
            if p in t:
                found.append(p)
        elif re.search(rf"\b{re.escape(p)}\b", t):
            found.append(p)
    return found


ka = load("kit_audit", "audit/kit-audit.py")
ks = load("kit_start", "scripts/kit_start.py")
ds = load("dpia_screen", "scripts/dpia_screen.py")
si = load("source_impact", "scripts/source_impact.py")
vm = load("validate_mappings", "scripts/validate_mappings.py")
cov = load("coverage_reports", "scripts/coverage_reports.py")
EX = os.path.join(ROOT, "audit", "examples")


def run(script, *args, cwd=ROOT):
    return subprocess.run(PY + [os.path.join(ROOT, script), *args], capture_output=True, text=True, cwd=cwd)


def generated_outputs():
    """Everything the kit prints or generates that reports a status, result or label."""
    out = {}
    filled = ["--evidence", os.path.join(EX, "filled", "evidence"), "--risks", os.path.join(EX, "filled", "risks.md"),
              "--incidents", os.path.join(EX, "filled", "incidents.md")]
    out["audit: all evidence present"] = run("audit/kit-audit.py", *filled, "--today", "2026-10-09").stdout
    out["audit: empty"] = run("audit/kit-audit.py", "--evidence", os.path.join(EX, "empty"), "--today", "2026-10-09").stdout
    out["audit: stale"] = run("audit/kit-audit.py", *filled, "--today", "2027-09-01").stdout
    out["audit: no registers"] = run("audit/kit-audit.py", "--evidence", os.path.join(EX, "filled", "evidence"), "--today", "2026-10-09").stdout
    full = {"id": 1, "enforcement": "active", "target": "branch", "bypass_actors": [],
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"]}},
            "rules": [{"type": t} for t in ("pull_request", "non_fast_forward", "deletion")] +
                     [{"type": "required_status_checks", "parameters": {"required_status_checks": [{"context": "x"}]}}]}
    bare = dict(full, rules=[], bypass_actors=[{"actor_id": 1}])
    real = ka.gh
    try:
        for label, rs in (("full ruleset", full), ("weak ruleset", bare), ("no ruleset", None)):
            ka.gh = lambda args, rs=rs: ([] if rs is None else [{"id": 1}]) if args[0].endswith("/rulesets") else rs
            out[f"audit github: {label}"] = json.dumps(ka.check_github("o/r", "main"))
    finally:
        ka.gh = real
    data = si.load(si.MAPPINGS)
    out["validate summary"] = vm.summary(data, vm.validate(data, si.load(vm.SCHEMA), {c["id"] for c in si.load(vm.CONTROLS)["controls"]})[1])
    for rel in ("controls/framework-mappings.md", "docs/maintenance/source-watch-list.md", "docs/maintenance/worked-example.md"):
        out[rel] = read(rel)
    for rel in sorted(glob.glob(os.path.join(ROOT, "docs", "coverage", "*.md"))):
        out[os.path.relpath(rel, ROOT)] = Path(rel).read_text(encoding="utf-8")
    sources, mappings = si.load(si.SOURCES), si.load(si.MAPPINGS)
    import datetime as dt
    for d in (dt.date(2026, 10, 12), dt.date(2028, 1, 1)):
        out[f"release notes {d}"] = si.release_notes(sources, mappings, d)
    for fw in ("SOC 2", "ISO/IEC 27001", "GDPR", "DORA", "wp248"):
        out[f"impact {fw}"] = run("scripts/source_impact.py", "list", "--framework", fw).stdout
    opts = [[o[0] for o in q[2]] for q in ks.QUESTIONS]
    for combo in itertools.product(*opts):
        out["kit_start " + "/".join(combo)] = ks.render(dict(zip([q[0] for q in ks.QUESTIONS], combo)))
    base = json.loads(read("privacy/dpia-answers.example.json"))
    for k, v in (("art35_3a", "yes"), ("vulnerable_people", "yes"), ("combining_datasets", "yes"), ("purposes", "")):
        a = dict(base); a[k] = v
        if k in ("vulnerable_people", "combining_datasets"):
            a["innovative_technology"] = "yes"
        out[f"dpia {k}"] = ds.render(ds.screen(a))
    out["dpia example"] = ds.render(ds.screen(base))
    gates = load("check_gates", "skills/production-migration/scripts/check_gates.py")
    for phase in gates.PHASES:
        with tempfile.TemporaryDirectory() as d:
            out[f"gates {phase} empty"] = run("skills/production-migration/scripts/check_gates.py", "--infra", d, "--phase", str(phase)).stdout
            for rel, tag in gates.PHASES[phase]:
                p = Path(d) / rel
                if rel.endswith("/"):
                    (p / "x").mkdir(parents=True, exist_ok=True); (p / "x" / "n.md").write_text("x")
                else:
                    p.parent.mkdir(parents=True, exist_ok=True); p.write_text("x")
            out[f"gates {phase} complete"] = run("skills/production-migration/scripts/check_gates.py", "--infra", d, "--phase", str(phase)).stdout
    return out


class Matcher(unittest.TestCase):
    def test_the_list_catches_external_outcome_wording(self):
        for text in ("You are SOC 2 ready", "ISO 27001 certified", "audit-ready", "Audit passed", "Fully compliant", "assurance achieved", "Certified."):
            self.assertTrue(hits(text), text)

    def test_the_list_does_not_flag_ordinary_words(self):
        for text in ("ensured", "evidence check complete", "not a measure of anyone's compliance", "internal checklist complete", "certificate holder", "insured"):
            self.assertEqual(hits(text), [], text)

    def test_the_list_file_has_the_core_phrases(self):
        for p in ("soc 2 ready", "audit-ready", "audit passed", "certified", "compliance achieved", "ready for certification"):
            self.assertIn(p, PHRASES)


class GeneratedStatusOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = generated_outputs()

    def test_there_is_a_lot_of_output_and_none_is_empty(self):
        self.assertGreater(len(self.outputs), 250)
        for name, text in self.outputs.items():
            if name.startswith("gates") or name.startswith("impact") or name.startswith("audit:"):
                self.assertTrue(text.strip(), name)

    def test_no_generated_status_implies_an_external_outcome(self):
        bad = {name: hits(text) for name, text in self.outputs.items() if hits(text)}
        self.assertEqual(bad, {})

    def test_the_audit_result_describes_an_internal_check(self):
        complete = self.outputs["audit: all evidence present"]
        self.assertIn("**Result: INTERNAL EVIDENCE CHECK COMPLETE.**", complete)
        self.assertIn("It is not an examination, certification or audit", complete)
        self.assertNotIn("ALL EVIDENCE PRESENT", complete)
        for name in ("audit: empty", "audit: stale", "audit: no registers"):
            self.assertIn("need attention", self.outputs[name], name)
            self.assertNotIn("INTERNAL EVIDENCE CHECK COMPLETE", self.outputs[name], name)

    def test_every_audit_report_says_it_is_not_a_compliance_assessment(self):
        for name, text in self.outputs.items():
            if name.startswith("audit:"):
                self.assertIn("evidence check, not a compliance assessment", text, name)


class StaticStrings(unittest.TestCase):
    """Catch a status string that no test exercises: scan every string literal in the tools."""

    FILES = sorted(glob.glob(os.path.join(ROOT, "scripts", "*.py")) + [os.path.join(ROOT, "audit", "kit-audit.py"),
                                                                        os.path.join(ROOT, "skills", "production-migration", "scripts", "check_gates.py")])

    def literals(self, path):
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
        skip = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                body = node.body
                if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) and isinstance(body[0].value.value, str):
                    skip.add(id(body[0].value))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip:
                yield node.value

    def test_no_string_in_the_tools_uses_prohibited_wording(self):
        self.assertGreaterEqual(len(self.FILES), 9)
        bad = {}
        for path in self.FILES:
            if path.endswith("prohibited_phrases.json"):
                continue
            for s in self.literals(path):
                h = hits(s)
                if h:
                    bad.setdefault(os.path.relpath(path, ROOT), []).append((h, s[:60]))
        self.assertEqual(bad, {})


class PathBoundaries(unittest.TestCase):
    def soc2(self):
        return read("guide/paths/soc2.md")

    def iso(self):
        return read("guide/paths/iso27001.md")

    def test_soc2_says_the_kit_cannot_issue_or_guarantee_a_report(self):
        t = self.soc2()
        self.assertIn("The kit cannot issue or guarantee a SOC 2 report", t)
        self.assertIn("Review label: community draft", t)

    def test_soc2_separates_type_i_from_type_ii(self):
        t = self.soc2()
        self.assertIn("Type I and Type II are different reports", t)
        for needle in ("suitably designed", "A point in time", "operated effectively", "A period", "only time and the examiner do"):
            self.assertIn(needle, t, needle)

    def test_soc2_lists_the_decisions_only_the_team_can_make(self):
        t = self.soc2()
        self.assertIn("Decisions the team must make", t)
        for needle in ("System scope", "Trust Services Criteria that apply", "evidence period"):
            self.assertIn(needle, t, needle)

    def test_both_paths_have_a_coverage_matrix_with_only_the_three_allowed_values(self):
        for name, t in (("soc2", self.soc2()), ("iso", self.iso())):
            sec = t.split("## Coverage matrix: what the kit covers")[1].split("## Exit criteria")[0]
            rows = [l for l in sec.splitlines() if l.startswith("| ") and not l.startswith("| Area") and not l.startswith("|---")]
            self.assertGreaterEqual(len(rows), 9, name)
            for r in rows:
                self.assertRegex(r, r"\| \*\*(covers in part|does not cover|covers)\*\* \|", (name, r))
            self.assertIn("does not cover", sec, name)
            self.assertNotIn("**covers** |", sec, name)    # nothing is plainly "covered"

    def test_matrices_name_the_required_work_the_kit_does_not_do(self):
        soc = self.soc2().split("## Coverage matrix")[1]
        for row in ("Readiness assessment by an independent party", "Choosing and engaging the examiner", "The examination and the report"):
            line = [l for l in soc.splitlines() if l.startswith(f"| {row}")][0]
            self.assertIn("**does not cover**", line, row)
        iso = self.iso().split("## Coverage matrix")[1]
        for row in ("Statement of Applicability", "Internal audit", "Certification audit (Stage 1 and Stage 2)", "Risk treatment plan"):
            line = [l for l in iso.splitlines() if l.startswith(f"| {row}")][0]
            self.assertIn("**does not cover**", line, row)

    def test_exit_criteria_state_what_each_shows_and_does_not_show(self):
        for name, t in (("soc2", self.soc2()), ("iso", self.iso())):
            sec = t.split("## Exit criteria: what completing each shows, and what it does not")[1].split("## Common mistakes")[0]
            self.assertIn("| Exit criterion | What it shows | What it does not show |", sec, name)
            self.assertIn("Internal checklist complete", sec, name)
            self.assertIn("does not mean", sec, name)
            self.assertIn("internal evidence check complete", sec, name)
        self.assertIn("**Only here does a SOC 2 report exist**", self.soc2())
        self.assertIn("**Only here does certification become possible**", self.iso())

    def test_iso_separates_implementing_an_isms_from_certification(self):
        t = self.iso()
        for needle in ("Implementing an ISMS is not the same as being certified", "accredited", "Clauses 4 to 10", "Statement of Applicability",
                       "A small control baseline is not a complete ISMS", "internal audit", "management review", "Review label: community draft"):
            self.assertIn(needle, t, needle)

    def test_the_maturity_model_says_level_4_cannot_be_reached_by_the_kit(self):
        self.assertIn("Level 4 cannot be reached by completing the kit", read("guide/maturity-model.md"))

    def test_the_matrices_agree_with_the_mapping_records(self):
        recs = json.loads(read("controls/mappings.json"))["records"]
        iso = [r for r in recs if r["framework"] == "ISO/IEC 27001"]
        text = " ".join(" ".join(r["exclusions"]) for r in iso)
        for needle in ("Statement of Applicability", "internal audit programme"):
            self.assertIn(needle, text)
        self.assertTrue(all(r["coverage_status"] == "needs expert review" for r in iso + [r for r in recs if r["framework"] == "SOC 2"]))


if __name__ == "__main__":
    unittest.main()
