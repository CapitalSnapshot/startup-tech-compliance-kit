#!/usr/bin/env python3
"""Fail if any text file in the repository uses a phrase that could be read as a compliance, certification or examination outcome.

  python3 scripts/check_claims.py           # exit 1 on a phrase outside the allowlist, or on a stale allowlist entry
  python3 scripts/check_claims.py --list    # show every hit, allowed or not

The phrases are in scripts/prohibited_phrases.json ("phrases" and "prose_only_phrases"). Matching is case-insensitive and by whole
word. A place that must mention a phrase (a negation, a test that checks the wording guard, the phrase list itself) is listed
in a claims_allowlist*.json file (the main one is scripts/claims_allowlist.json) with a file, a phrase (or "*" for a file that must mention many) and a reason. An entry whose file no longer contains the phrase is reported as
stale, so the list cannot rot. An entry for a file that does not exist is ignored, so files removed before release do not break the
check. Python 3 standard library only.
"""
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PHRASES_FILE = os.path.join(ROOT, "scripts", "prohibited_phrases.json")
EXTENSIONS = (".md", ".json", ".py", ".yml", ".yaml", ".txt", ".sh")
SKIP_DIRS = {".git", "__pycache__", "node_modules"}


def load_phrases(path=PHRASES_FILE):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return [p.lower() for p in data["phrases"] + data.get("prose_only_phrases", [])]


def allowlist_paths(root=ROOT):
    """The main allowlist, plus any other claims_allowlist*.json file in the repository."""
    found = [os.path.join(root, rel) for rel in files(root) if os.path.basename(rel).startswith("claims_allowlist") and rel.endswith(".json")]
    return sorted(found)


def load_allowlist(path=None):
    entries = []
    for one in [path] if path else allowlist_paths():
        with open(one, encoding="utf-8") as fh:
            entries.extend(json.load(fh)["allow"])
    for e in entries:
        if not (e.get("file") and e.get("phrase") and str(e.get("reason", "")).strip()):
            raise ValueError(f"allowlist entry needs file, phrase and a reason: {e}")
    return entries


def files(root=ROOT):
    for base, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            if name.endswith(EXTENSIONS):
                yield os.path.relpath(os.path.join(base, name), root).replace(os.sep, "/")


def scan(root=ROOT, phrases=None):
    """Return {(file, phrase): [line numbers]} for every hit."""
    phrases = phrases or load_phrases()
    patterns = [(p, re.compile(r"(?<!\w)" + re.escape(p) + r"(?!\w)", re.IGNORECASE)) for p in phrases]
    hits = {}
    for rel in files(root):
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for n, line in enumerate(lines, 1):
            for phrase, pat in patterns:
                if pat.search(line):
                    hits.setdefault((rel, phrase), []).append(n)
    return hits


def evaluate(hits, allow, root=ROOT):
    """Return (blocked, stale): blocked hits not in the allowlist, and allowlist entries that no longer match."""
    allowed = {(e["file"], e["phrase"].lower()) for e in allow}
    whole_file = {e["file"] for e in allow if e["phrase"] == "*"}
    blocked = {k: v for k, v in hits.items() if k not in allowed and k[0] not in whole_file}
    stale = []
    for e in allow:
        if not os.path.isfile(os.path.join(root, e["file"])):
            continue
        used = any(f == e["file"] for f, _ in hits) if e["phrase"] == "*" else (e["file"], e["phrase"].lower()) in hits
        if not used:
            stale.append(e)
    return blocked, stale


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    hits = scan()
    allow = load_allowlist()
    blocked, stale = evaluate(hits, allow)
    if "--list" in argv:
        for (rel, phrase), lines in sorted(hits.items()):
            status = "BLOCKED" if (rel, phrase) in blocked else "allowed"
            print(f"{status}: {rel}: '{phrase}' on line(s) {', '.join(map(str, lines))}")
    for (rel, phrase), lines in sorted(blocked.items()):
        print(f"claims-check: '{phrase}' in {rel} on line(s) {', '.join(map(str, lines))}. Reword it, or add it to scripts/claims_allowlist.json with a reason.")
    for e in stale:
        print(f"claims-check: stale allowlist entry: '{e['phrase']}' no longer appears in {e['file']}. Remove the entry.")
    if blocked or stale:
        return 1
    print(f"claims-check: clean ({len(hits)} allowed mention(s) across {len({k[0] for k in hits})} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
