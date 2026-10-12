import importlib.util, os, tempfile, unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sanitise_check", os.path.join(HERE, "..", "..", "scripts", "sanitise_check.py"))
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)

# Built at run time so this file does not itself contain what the scanner looks for.
IP = ".".join(["54", "76", "175", "146"])
DOC_IPS = " ".join([".".join(["192", "0", "2", "10"]), ".".join(["203", "0", "113", "5"]), "127.0.0.1", "0.0.0.0"])
ACCOUNT = "0" * 6 + "1" * 6
KEY = "-----BEGIN " + "RSA PRIVATE KEY-----"
TOKEN = "ghp_" + "a" * 22
AKIA = "AKIA" + "A" * 16


def scan_text(text, denylist=None, name="x.md"):
    with tempfile.TemporaryDirectory() as d:
        Path(d, name).write_text(text)
        old = {k: os.environ.pop(k, None) for k in ("DENYLIST", "DENYLIST_FILE")}
        try:
            if denylist is not None:
                os.environ["DENYLIST"] = denylist
            findings, have = sc.scan(d)
        finally:
            for k in ("DENYLIST", "DENYLIST_FILE"):
                os.environ.pop(k, None)
            for k, v in old.items():
                if v is not None:
                    os.environ[k] = v
        return [f[0] for f in findings], have


class SanitiseTests(unittest.TestCase):
    def test_clean_text_is_clean(self):
        self.assertEqual(scan_text("Nothing to see. Version 2.0.1 and 1.2.3.\n")[0], [])

    def test_public_ip_is_flagged(self):
        self.assertIn("IPv4 address", scan_text(f"host {IP}\n")[0])

    def test_ip_at_the_end_of_a_sentence_is_still_flagged(self):
        self.assertIn("IPv4 address", scan_text(f"reach it at {IP}.\n")[0])

    def test_documentation_and_loopback_addresses_are_allowed(self):
        self.assertEqual(scan_text(DOC_IPS + "\n")[0], [])

    def test_a_longer_dotted_number_is_not_an_ip(self):
        self.assertEqual(scan_text("1.2.3.4.5.6\n")[0], [])

    def test_account_id_key_token_and_access_key(self):
        got = scan_text(f"{ACCOUNT}\n{KEY}\n{TOKEN}\n{AKIA}\n")[0]
        for label in ("12-digit account ID", "private key block", "token-like string", "cloud access key id"):
            self.assertIn(label, got)

    def test_thirteen_digits_is_not_an_account_id(self):
        self.assertEqual(scan_text("1" * 13 + "\n")[0], [])

    def test_denylist_from_environment(self):
        got, have = scan_text("the Acme-Internal-Name box\n", denylist="acme-internal-name\n# comment\n")
        self.assertTrue(have)
        self.assertEqual(got, ["denylist pattern matched (pattern not shown)"])

    def test_a_denylist_pattern_can_allow_exactly_one_role_address(self):
        pattern = r"(?<!role@)example-domain\.com"
        self.assertEqual(scan_text("write to role@example-domain.com\n", denylist=pattern)[0], [])
        self.assertEqual(scan_text("see www.example-domain.com\n", denylist=pattern)[0], ["denylist pattern matched (pattern not shown)"])
        self.assertEqual(scan_text("other@example-domain.com\n", denylist=pattern)[0], ["denylist pattern matched (pattern not shown)"])

    def test_denylist_skips_notice_and_readme_only(self):
        self.assertEqual(scan_text("acme-internal-name\n", denylist="acme-internal-name", name="NOTICE")[0], [])
        self.assertEqual(scan_text("acme-internal-name\n", denylist="acme-internal-name", name="README.md")[0], [])
        self.assertTrue(scan_text("acme-internal-name\n", denylist="acme-internal-name", name="other.md")[0])

    def test_no_denylist_is_reported(self):
        self.assertFalse(scan_text("x\n")[1])

    def test_output_never_shows_the_match(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "x.md").write_text(f"secret {TOKEN}\n")
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = sc.main([d])
            self.assertEqual(rc, 1)
            self.assertNotIn(TOKEN, buf.getvalue())

    def test_compiled_python_and_other_banned_files_are_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            for rel in ("__pycache__/x.cpython-312.pyc", "mod.pyc", ".DS_Store", "id.pem", "a/.env", "denylist.txt", "ok/readme.md"):
                p = Path(d, rel); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b"x")
            got = set(sc.banned_files(d))
            self.assertEqual(got, {"__pycache__", "__pycache__/x.cpython-312.pyc", "mod.pyc", ".DS_Store", "id.pem", "a/.env", "denylist.txt"})

    def test_the_repository_itself_has_no_banned_files(self):
        # run from a clean checkout: __pycache__ may exist locally from running the tests, so look at tracked files only
        import subprocess
        try:
            out = subprocess.run(["git", "ls-files"], cwd=os.path.join(HERE, "..", ".."), capture_output=True, text=True)
        except OSError:
            self.skipTest("git is not installed here")
        if out.returncode != 0:
            self.skipTest("not a git checkout")
        bad = [f for f in out.stdout.splitlines() if sc.BANNED_FILES.search(f)]
        self.assertEqual(bad, [])

    def test_the_repository_itself_is_clean_of_the_built_in_patterns(self):
        root = os.path.join(HERE, "..", "..")
        old = {k: os.environ.pop(k, None) for k in ("DENYLIST", "DENYLIST_FILE")}
        try:
            findings, _ = sc.scan(root)
        finally:
            for k, v in old.items():
                if v is not None:
                    os.environ[k] = v
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
