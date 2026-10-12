#!/usr/bin/env python3
"""Fail if the repository contains anything that looks like a real hostname, address, account ID or credential.

  python3 scripts/sanitise_check.py [path]

Two layers:
  1. Built-in patterns: IPv4 addresses (documentation ranges and loopback are allowed), 12-digit cloud account
     IDs, private key blocks, cloud access key IDs, common token formats.
  2. The maintainers' private denylist: one regular expression per line, from the file named by DENYLIST_FILE or
     from the DENYLIST environment variable (a repository secret in CI). It is kept out of the repository on
     purpose, because publishing the list would publish the identifiers.

Prints file:line, never the matching text. Exit 0 if clean, 1 if anything matches. Python 3 standard library
only; behaves the same on Linux, macOS and Windows.
"""
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git"}
SELF = {"sanitise_check.py"}
DENYLIST_SKIP_FILES = {"NOTICE", "README.md"}  # the author credit may appear in these

IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?!\.?\d)")  # not part of a longer dotted number; a full stop after is fine
IPV4_OK = re.compile(r"^(192\.0\.2\.|198\.51\.100\.|203\.0\.113\.|0\.0\.0\.0$|127\.0\.0\.1$|255\.255\.255\.)")
BUILTIN = [
    ("12-digit account ID", re.compile(r"(?<!\d)\d{12}(?!\d)")),
    ("private key block", re.compile(r"BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY")),
    ("cloud access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("token-like string", re.compile(r"(ghp_|github_pat_|sk-ant-|sk_live_|xox[bap]-)[A-Za-z0-9_-]{10,}")),
]


def files(root):
    root = Path(root)
    for dirpath, dirnames, names in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for n in names:
            p = Path(dirpath) / n
            if n in SELF:
                continue
            try:
                data = p.read_bytes()
            except OSError:
                continue
            if b"\0" in data[:4096]:
                continue  # binary
            yield p, data.decode("utf-8", errors="replace").splitlines()


BANNED_FILES = re.compile(r"(^|/)(__pycache__|\.DS_Store|Thumbs\.db)(/|$)|\.(pyc|pyo|pem|key|bundle)$|(^|/)\.env(\..*)?$|(^|/)denylist[^/]*\.txt$")


def banned_files(root):
    """Files that must never be committed: compiled Python (it records local paths), keys, env files, denylists.

    Inside a git repository only tracked files count (an ignored __pycache__ on your disk is harmless);
    elsewhere every file under the path counts."""
    import subprocess
    root = Path(root)
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, timeout=30)
        if out.returncode == 0 and (root / ".git").exists():
            return sorted(f for f in out.stdout.splitlines() if BANNED_FILES.search(f))
    except (OSError, subprocess.TimeoutExpired):
        pass
    found = []
    for dirpath, dirnames, names in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for n in list(dirnames) + names:
            rel = (Path(dirpath) / n).relative_to(root).as_posix()
            if BANNED_FILES.search(rel):
                found.append(rel)
    return found


def load_denylist():
    text = None
    path = os.environ.get("DENYLIST_FILE")
    if path and os.path.isfile(path):
        text = Path(path).read_text(encoding="utf-8")
    elif os.environ.get("DENYLIST"):
        text = os.environ["DENYLIST"]
    pats = []
    for line in (text or "").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            pats.append(re.compile(line, re.I))
    return pats, text is not None


def scan(root):
    findings = []  # (label, file, line)
    denylist, have_denylist = load_denylist()
    for p, lines in files(root):
        for i, line in enumerate(lines, 1):
            if any(not IPV4_OK.match(m.group(0)) for m in IPV4.finditer(line)):
                findings.append(("IPv4 address", p, i))
            for label, rx in BUILTIN:
                if rx.search(line):
                    findings.append((label, p, i))
            if p.name not in DENYLIST_SKIP_FILES:
                for rx in denylist:
                    if rx.search(line):
                        findings.append(("denylist pattern matched (pattern not shown)", p, i))
    return findings, have_denylist


def main(argv=None):
    root = (argv or sys.argv[1:] or ["."])[0]
    findings, have_denylist = scan(root)
    bad_files = banned_files(root)
    if not have_denylist:
        print("NOTE  no private denylist supplied; only the built-in patterns ran")
    if bad_files:
        print("FAIL  file that must not be committed (delete it; inside a git checkout only tracked files count)")
        for f in sorted(bad_files):
            print(f"        {f}")
    if findings or bad_files:
        last = None
        for label, p, i in sorted(findings, key=lambda f: (f[0], str(f[1]), f[2])):
            if label != last:
                print(f"FAIL  {label}")
                last = label
            print(f"        {Path(p).as_posix()}:{i}")
        return 1
    print("sanitise-check: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
