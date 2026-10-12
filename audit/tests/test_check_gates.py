import importlib.util, os, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
GATES = os.path.join(HERE, "..", "..", "skills", "production-migration", "scripts", "check_gates.py")
spec = importlib.util.spec_from_file_location("check_gates", GATES)
cg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cg)


def make(root, phase, empty=(), skip=()):
    for rel, tag in cg.PHASES[phase]:
        if rel in skip:
            continue
        p = Path(root) / rel
        if rel.endswith("/"):
            (p / "nested" / "deeper").mkdir(parents=True, exist_ok=True)
            (p / "nested" / "note.md").write_text("x")
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("" if rel in empty else "x")


def run(*args):
    r = subprocess.run([sys.executable, "-I", GATES, *args], capture_output=True, text=True)
    return r.returncode, r.stdout


class GateTests(unittest.TestCase):
    def test_empty_infra_folder_fails_every_phase(self):
        for phase in cg.PHASES:
            with tempfile.TemporaryDirectory() as d:
                rc, out = run("--infra", d, "--phase", str(phase))
                self.assertEqual(rc, 1, (phase, out))
                self.assertIn("NOT met", out)

    def test_complete_phase_passes(self):
        for phase in cg.PHASES:
            with tempfile.TemporaryDirectory() as d:
                make(d, phase)
                rc, out = run("--infra", d, "--phase", str(phase))
                self.assertEqual(rc, 0, (phase, out))

    def test_empty_file_is_reported_empty(self):
        with tempfile.TemporaryDirectory() as d:
            make(d, 0, empty={"evidence/snapshot.md"})
            rc, out = run("--infra", d, "--phase", "0")
            self.assertEqual(rc, 1)
            self.assertIn("EMPTY    evidence/snapshot.md", out)

    def test_lean_skips_demo_and_pack(self):
        with tempfile.TemporaryDirectory() as d:
            make(d, 2, skip={"evidence/demo-promotions.md"})
            rc, out = run("--infra", d, "--phase", "2", "--lean")
            self.assertEqual(rc, 0, out)
            self.assertIn("SKIPPED", out)
        with tempfile.TemporaryDirectory() as d:
            make(d, 4, skip={"evidence-pack/"})
            rc, _ = run("--infra", d, "--phase", "4", "--lean")
            self.assertEqual(rc, 0)
            rc, _ = run("--infra", d, "--phase", "4")
            self.assertEqual(rc, 1)

    def test_forward_slash_paths_resolve(self):
        with tempfile.TemporaryDirectory() as d:
            make(d, 2)
            results = cg.check(Path(d), 2, False, False)
            self.assertTrue(all(r[1] == "OK" for r in results), results)

    def test_missing_infra_folder_exits_2(self):
        rc, _ = run("--infra", os.path.join(tempfile.gettempdir(), "no-such-folder-kit-test"), "--phase", "0")
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
