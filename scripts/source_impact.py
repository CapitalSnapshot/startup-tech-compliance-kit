#!/usr/bin/env python3
"""Framework change impact tooling: the source watch list, the impact lister and the release-notes helper.

  python3 scripts/source_impact.py list --framework "SOC 2" [--edition TEXT] [--json]
                                              # every mapping record, control file and document affected by a source change
  python3 scripts/source_impact.py build      # write docs/maintenance/source-watch-list.md from docs/maintenance/sources.json
  python3 scripts/source_impact.py check      # validate the watch list against the mappings; fail if the page is stale (CI)
  python3 scripts/source_impact.py release-notes [--today YYYY-MM-DD]
                                              # sources that are current, stale or never checked, and the mappings still unreviewed

The process is in MAINTENANCE.md. Exit status: 0 ok; 1 integrity errors or a stale page; 2 an input is missing, unreadable or unknown.
Python 3 standard library only.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SOURCES = os.path.join(ROOT, "docs", "maintenance", "sources.json")
MAPPINGS = os.path.join(ROOT, "controls", "mappings.json")
CONTROLS = os.path.join(ROOT, "controls", "controls.json")
PAGE = os.path.join(ROOT, "docs", "maintenance", "source-watch-list.md")
FRAMEWORKS = ["SOC 2", "ISO/IEC 27001", "GDPR", "DORA"]
TYPES = ("law", "standard", "criteria", "regulator guidance", "tool")
REQUIRED = ["id", "name", "type", "framework", "edition_mapped", "official_url", "url_status", "last_checked", "checked_what", "owner",
            "review_cadence_days", "review_cadence", "documents", "notes"]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def valid_date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def validate(sources, mappings, root=ROOT, today=None):
    today = today or dt.date.today()
    errors = []
    items = sources.get("sources") if isinstance(sources, dict) else None
    if not isinstance(items, list) or not items:
        return ["sources.json must be an object with a non-empty 'sources' list"]
    seen = set()
    for s in items:
        sid = s.get("id", "?") if isinstance(s, dict) else "?"
        if not isinstance(s, dict):
            errors.append(f"{sid}: source must be an object")
            continue
        for k in REQUIRED:
            if k not in s:
                errors.append(f"{sid}: missing field '{k}'")
        if sid in seen:
            errors.append(f"{sid}: duplicate id")
        seen.add(sid)
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", str(sid)):
            errors.append(f"{sid}: id must be lowercase letters, digits and hyphens")
        if s.get("type") not in TYPES:
            errors.append(f"{sid}: type must be one of {', '.join(TYPES)}")
        if s.get("framework") is not None and s.get("framework") not in FRAMEWORKS:
            errors.append(f"{sid}: framework must be null or one of {', '.join(FRAMEWORKS)}")
        for k in ("name", "edition_mapped", "url_status", "owner", "review_cadence", "checked_what", "notes"):
            if k in s and (not isinstance(s[k], str) or not s[k].strip()):
                errors.append(f"{sid}: {k} must not be empty")
        if isinstance(s.get("owner"), str) and "@" in s["owner"]:
            errors.append(f"{sid}: owner must be a role, not an address")
        url = s.get("official_url")
        if url is not None and not (isinstance(url, str) and url.startswith("https://")):
            errors.append(f"{sid}: official_url must be null or an https URL")
        if "last_checked" in s and s["last_checked"] is not None:
            d = valid_date(s["last_checked"])
            if d is None:
                errors.append(f"{sid}: last_checked is not a real date")
            elif d > today:
                errors.append(f"{sid}: last_checked {d} is in the future")
        cad = s.get("review_cadence_days")
        if cad is not None and not (isinstance(cad, int) and not isinstance(cad, bool) and cad > 0):
            errors.append(f"{sid}: review_cadence_days must be null or a positive whole number")
        docs = s.get("documents")
        if not isinstance(docs, list):
            errors.append(f"{sid}: documents must be a list")
        else:
            for p in docs:
                if not os.path.exists(os.path.join(root, p)):
                    errors.append(f"{sid}: document not found: {p}")
    recs = mappings.get("records", [])
    for fw in FRAMEWORKS:
        rec_eds = {r["edition"] for r in recs if r.get("framework") == fw}
        src_eds = {s.get("edition_mapped") for s in items if isinstance(s, dict) and s.get("framework") == fw}
        if rec_eds and not src_eds:
            errors.append(f"{fw}: the mappings use this framework but no source in the watch list covers it")
        elif rec_eds != src_eds:
            errors.append(f"{fw}: mapping records use edition(s) {sorted(rec_eds)} but the watch list says {sorted(src_eds)}")
    return errors


def render_page(sources):
    out = ["# Source watch list", "",
           "<!-- Generated by scripts/source_impact.py from docs/maintenance/sources.json. Do not edit by hand. -->", "",
           "Every source the kit's content relies on, the exact edition currently mapped, where the official text lives, who looks after it and how often it is "
           "re-checked. The process for acting on a change is in [`MAINTENANCE.md`](../../MAINTENANCE.md). To see what a change touches, run "
           "`python3 scripts/source_impact.py list --framework \"<name>\"`.", "",
           "**\"Last checked\" says what was actually looked at.** A date next to \"page title only\" is not a review of the content. A source that has never been "
           "checked says so.", ""]
    for s in sources["sources"]:
        out.append(f"## {s['name']}")
        out.append("")
        out.append(f"- **Id:** `{s['id']}` · **Type:** {s['type']} · **Mapped framework:** {s['framework'] or 'none (cited, not mapped)'}")
        out.append(f"- **Edition currently mapped:** {s['edition_mapped']}")
        out.append(f"- **Official URL:** {s['official_url'] or 'not recorded'}. {s['url_status']}")
        out.append(f"- **Last checked:** {s['last_checked'] or 'never'}. {s['checked_what']}")
        out.append(f"- **Owner (role):** {s['owner']} · **Review cadence:** {s['review_cadence']}")
        docs = ", ".join(f"[`{p}`](../../{p})" for p in s["documents"]) or "none"
        out.append(f"- **Documents that rely on it:** {docs}")
        out.append(f"- **Notes:** {s['notes']}")
        out.append("")
    return "\n".join(out)


def status(s, today):
    if s["review_cadence_days"] is None:
        return "not tracked"
    if s["last_checked"] is None:
        return "never checked"
    age = (today - dt.date.fromisoformat(s["last_checked"])).days
    return "stale" if age > s["review_cadence_days"] else "current"


def impact(sources, mappings, controls, framework, edition=None):
    key = framework.strip().lower()
    srcs = [s for s in sources["sources"] if (s["framework"] or "").lower() == key or s["id"].lower() == key]
    if not srcs:
        return None
    fws = {s["framework"] for s in srcs if s["framework"]}
    ed = (edition or "").strip().lower()
    recs = [r for r in mappings["records"] if r["framework"] in fws and (not ed or ed in r["edition"].lower())]
    cfiles = {c["id"]: c["file"] for c in controls}
    ctrl = sorted({f"controls/{cfiles[r['control_id']]}" for r in recs if r["control_id"] in cfiles})
    docs = sorted({p for s in srcs for p in s["documents"]})
    return {"sources": [{k: s[k] for k in ("id", "name", "edition_mapped", "last_checked")} for s in srcs],
            "records": [{"id": r["id"], "control_id": r["control_id"], "source_reference": r["source_reference"], "coverage_status": r["coverage_status"],
                         "review_label": r["review"]["label"]} for r in recs],
            "control_files": ctrl, "documents": docs}


def release_notes(sources, mappings, today):
    out = ["## Sources and editions", "", "| Source | Edition mapped | Last checked | Status |", "|---|---|---|---|"]
    for s in sources["sources"]:
        out.append(f"| {s['name']} | {s['edition_mapped']} | {s['last_checked'] or 'never'} | {status(s, today)} |")
    recs = mappings["records"]
    unrev = [r for r in recs if r["review"]["label"] == "community draft"]
    open_ = [r for r in recs if r["coverage_status"] in ("not assessed", "needs expert review")]
    out += ["", "## Mappings left unreviewed or unresolved", "",
            f"- Community drafts (no maintainer or specialist review recorded): {len(unrev)} of {len(recs)} records.",
            f"- Records that are not assessed or need expert review: {len(open_)}.", ""]
    stale = [s for s in sources["sources"] if status(s, today) in ("stale", "never checked")]
    out.append("Sources stale or never checked: " + (", ".join(f"{s['name']} ({status(s, today)})" for s in stale) if stale else "none") + ".")
    out += ["", "## To complete for this release", "",
            "- Sources and editions changed by this release: <name each source and edition, or write none>",
            "- Mappings this release leaves stale, unreviewed or incomplete: <paste the lists above, or write none>", ""]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Framework change impact tooling.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("list"); pl.add_argument("--framework", required=True); pl.add_argument("--edition"); pl.add_argument("--json", action="store_true")
    sub.add_parser("build"); sub.add_parser("check")
    pr = sub.add_parser("release-notes"); pr.add_argument("--today")
    a = ap.parse_args(argv)
    try:
        sources, mappings, controls = load(SOURCES), load(MAPPINGS), load(CONTROLS)["controls"]
    except (OSError, ValueError) as e:
        print(f"error: could not read an input file: {e}", file=sys.stderr)
        return 2
    if a.cmd == "list":
        res = impact(sources, mappings, controls, a.framework, a.edition)
        if res is None:
            known = sorted({s["framework"] for s in sources["sources"] if s["framework"]} | {s["id"] for s in sources["sources"]})
            print(f"error: unknown framework or source '{a.framework}'. Known: {', '.join(known)}", file=sys.stderr)
            return 2
        if a.json:
            print(json.dumps(res, indent=2))
            return 0
        print("Sources:"); [print(f"  {s['id']}: {s['name']} (edition mapped: {s['edition_mapped']}; last checked: {s['last_checked'] or 'never'})") for s in res["sources"]]
        print(f"Mapping records ({len(res['records'])}): review each, update its fields and review block:")
        for r in res["records"]:
            print(f"  {r['id']}  [{', '.join(r['source_reference'])}]  {r['coverage_status']}  ({r['review_label']})")
        print("Control files that carry these records:"); [print(f"  {p}") for p in res["control_files"]]
        print("Documents that rely on the source:"); [print(f"  {p}") for p in res["documents"]]
        return 0
    if a.cmd == "release-notes":
        today = valid_date(a.today) if a.today else dt.date.today()
        if today is None:
            print("error: --today must be a date like 2026-10-09", file=sys.stderr)
            return 2
        print(release_notes(sources, mappings, today))
        return 0
    errors = validate(sources, mappings)
    if errors:
        print("INVALID\n" + "\n".join(f"  {e}" for e in errors), file=sys.stderr)
        return 1
    page = render_page(sources) + "\n"
    if a.cmd == "build":
        with open(PAGE, "w", encoding="utf-8") as fh:
            fh.write(page)
        print(f"wrote {os.path.relpath(PAGE, ROOT)}")
        return 0
    try:
        with open(PAGE, encoding="utf-8") as fh:
            cur = fh.read()
    except OSError:
        cur = None
    if cur != page:
        print("docs/maintenance/source-watch-list.md is out of date: run python3 scripts/source_impact.py build", file=sys.stderr)
        return 1
    print("source watch list is valid and up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
