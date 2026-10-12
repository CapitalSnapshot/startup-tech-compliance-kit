#!/usr/bin/env python3
"""List and check a specialist review scope file. Nothing here writes to the repository.

  python3 scripts/review_scope.py list    docs/specialist-reviews/scopes/gdpr-privacy.json
  python3 scripts/review_scope.py check   docs/specialist-reviews/scopes/gdpr-privacy.json   # or --all
  python3 scripts/review_scope.py preview docs/specialist-reviews/scopes/<completed>.json

A scope file names the mapping records and documents a review covers, the editions, and the exclusions. Only what a scope names can
become "specialist reviewed". `check` fails on an unknown record or document, a scope that claims a reviewer or date before a review
happened, and a completed scope that is missing a role, a date or a decision for any item. `preview` prints, for a completed scope,
the review block each record would receive and the label line each document would carry. It never edits a file: the update is made
by hand, following docs/specialist-reviews/update-procedure.md. Python 3 standard library only.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MAPPINGS = os.path.join(ROOT, "controls", "mappings.json")
SCOPE_DIR = os.path.join(ROOT, "docs", "specialist-reviews", "scopes")
STATUSES = ("proposed", "completed")
DECISIONS = ("accepted", "accepted with changes", "not accepted", "not reviewed")
GRANTING = ("accepted", "accepted with changes")
REQUIRED = ["scope_id", "title", "status", "reviewer_role", "review_date", "source_editions", "records", "documents", "exclusions",
            "limitations", "decisions"]
LABEL_LINE = re.compile(r"\*\*Review label:\s*([^*.]+)")


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _records():
    return {r["id"]: r for r in _load(MAPPINGS)["records"]}


def _nonblank(value):
    return isinstance(value, str) and value.strip() != ""


def check_scope(scope, records=None, root=ROOT, today=None):
    """Return a list of error strings. An empty list means the scope file is valid."""
    records = _records() if records is None else records
    today = today or datetime.date.today()
    errors = []
    if not isinstance(scope, dict):
        return ["scope file must be a JSON object"]
    for key in REQUIRED:
        if key not in scope:
            errors.append(f"missing field: {key}")
    if errors:
        return errors
    status = scope["status"]
    if status not in STATUSES:
        errors.append(f"status must be one of {', '.join(STATUSES)}")
    for key in ("source_editions", "records", "documents", "exclusions"):
        if not isinstance(scope[key], list) or not scope[key] or not all(_nonblank(x) for x in scope[key]):
            errors.append(f"{key} must be a non-empty list of non-blank strings")
    if errors:
        return errors
    for key in ("records", "documents"):
        if len(set(scope[key])) != len(scope[key]):
            errors.append(f"{key} lists an item twice")
    for rid in scope["records"]:
        if rid not in records:
            errors.append(f"unknown mapping record: {rid}")
    for doc in scope["documents"]:
        full = os.path.normpath(os.path.join(root, doc))
        if doc.startswith(("/", "..")) or not full.startswith(os.path.normpath(root)) or not os.path.isfile(full):
            errors.append(f"document not found in the repository: {doc}")
    if not isinstance(scope["decisions"], dict):
        errors.append("decisions must be an object")
        return errors
    items = set(scope["records"]) | set(scope["documents"])
    if status == "proposed":
        for key in ("reviewer_role", "review_date", "limitations"):
            if scope[key] is not None:
                errors.append(f"a proposed scope must have {key} null: no review has happened")
        if scope["decisions"]:
            errors.append("a proposed scope must have no decisions: no review has happened")
        return errors
    role = scope["reviewer_role"]
    if not _nonblank(role):
        errors.append("a completed scope needs a reviewer_role")
    elif re.search(r"maintainer|author", role, re.IGNORECASE):
        errors.append("reviewer_role names a maintainer or an author: those roles cannot award specialist reviewed")
    date = scope["review_date"]
    if not isinstance(date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        errors.append("a completed scope needs a review_date as YYYY-MM-DD")
    else:
        try:
            if datetime.date.fromisoformat(date) > today:
                errors.append("review_date is in the future")
        except ValueError:
            errors.append("review_date is not a real date")
    if not _nonblank(scope["limitations"]):
        errors.append("a completed scope needs limitations (write what the review did not cover)")
    for item in sorted(items):
        entry = scope["decisions"].get(item)
        if not isinstance(entry, dict):
            errors.append(f"no decision recorded for {item}")
            continue
        if entry.get("decision") not in DECISIONS:
            errors.append(f"{item}: decision must be one of {', '.join(DECISIONS)}")
        if not _nonblank(entry.get("rationale")):
            errors.append(f"{item}: a rationale is required")
    for item in scope["decisions"]:
        if item not in items:
            errors.append(f"decision for something outside the scope: {item}")
    return errors


def _label_of(path, root=ROOT):
    with open(os.path.join(root, path), encoding="utf-8") as fh:
        for line in fh.read().splitlines()[:12]:
            m = LABEL_LINE.search(line)
            if m:
                return m.group(1).strip()
    return None


def cmd_list(scope, records, root=ROOT):
    lines = [f"Scope {scope['scope_id']}: {scope['title']}", f"Status: {scope['status']}",
             "Editions: " + "; ".join(scope["source_editions"]), "", f"Mapping records ({len(scope['records'])}):"]
    for rid in scope["records"]:
        r = records.get(rid)
        if r:
            lines.append(f"  {rid} | {r['coverage_status']} | {r['review']['label']} | {', '.join(r['source_reference'])}")
        else:
            lines.append(f"  {rid} | UNKNOWN RECORD")
    lines += ["", f"Documents ({len(scope['documents'])}):"]
    for doc in scope["documents"]:
        lines.append(f"  {doc} | label: {_label_of(doc, root) or 'no label line found'}")
    lines += ["", "Excluded:"] + [f"  {x}" for x in scope["exclusions"]]
    lines += ["", "Only the records and documents above can become specialist reviewed. Nothing else changes."]
    return "\n".join(lines)


def cmd_preview(scope, records, root=ROOT):
    if scope["status"] != "completed":
        return "This scope is not completed, so there is nothing to preview. No review has been recorded."
    lines = [f"Scope {scope['scope_id']}, reviewer role: {scope['reviewer_role']}, review date: {scope['review_date']}",
             "Edit by hand. This preview writes nothing.", ""]
    for rid in scope["records"]:
        d = scope["decisions"][rid]
        if d["decision"] in GRANTING:
            lines.append(f"{rid}: set review.label to \"specialist reviewed\", reviewer_role \"{scope['reviewer_role']}\", "
                         f"review_date \"{scope['review_date']}\", decision \"{d['decision']}\", rationale as recorded"
                         + (f"; reviewer's coverage_status: {d['coverage_status']}" if d.get("coverage_status") else "; coverage_status unchanged"))
        else:
            lines.append(f"{rid}: no change (decision: {d['decision']}). The label stays {records[rid]['review']['label']}.")
    for doc in scope["documents"]:
        d = scope["decisions"][doc]
        if d["decision"] in GRANTING:
            lines.append(f"{doc}: change the label line from \"{_label_of(doc, root)}\" to \"specialist reviewed\" and name the scope")
        else:
            lines.append(f"{doc}: no change (decision: {d['decision']})")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("command", choices=["list", "check", "preview"])
    ap.add_argument("scope", nargs="?", help="path to a scope file")
    ap.add_argument("--all", action="store_true", help="check every file in docs/specialist-reviews/scopes/")
    args = ap.parse_args(argv)
    if args.command == "check" and args.all:
        paths = sorted(glob.glob(os.path.join(SCOPE_DIR, "*.json")))
        if not paths:
            print("no scope files found")
            return 1
    elif args.scope:
        paths = [args.scope]
    else:
        ap.error("give a scope file, or --all with check")
    records = _records()
    failed = False
    for path in paths:
        try:
            scope = _load(path)
        except (OSError, ValueError) as exc:
            print(f"{path}: cannot read: {exc}")
            failed = True
            continue
        errors = check_scope(scope, records)
        if errors:
            failed = True
            print(f"{path}: {len(errors)} problem(s)")
            for e in errors:
                print(f"  {e}")
            continue
        if args.command == "check":
            print(f"{path}: scope is valid ({scope['status']}, {len(scope['records'])} records, {len(scope['documents'])} documents)")
        elif args.command == "list":
            print(cmd_list(scope, records))
        else:
            print(cmd_preview(scope, records))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
