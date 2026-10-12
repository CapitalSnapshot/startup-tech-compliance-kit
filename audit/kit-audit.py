#!/usr/bin/env python3
"""kit-audit: an EVIDENCE check, not a compliance assessment.

Reads your evidence files and registers and reports, per control, whether dated evidence exists, is fresh, and
passed. It makes no changes. The base layer needs no credentials and no network. The optional GitHub layer makes
read-only API calls through the `gh` CLI and says which ones.

  kit-audit.py --evidence DIR [--risks FILE] [--incidents FILE] [--controls DIR] [--github OWNER/REPO [--branch main]]
               [--today YYYY-MM-DD] [--out report.md]

Exit status: 0 if every control has fresh, passing evidence and nothing is overdue or unassessed; 1 if anything needs attention;
2 if an input is missing or unusable (a folder or file that does not exist, a bad date). It never reports success
because it could not read something.

Evidence files are Markdown with one header comment anywhere near the top:

  <!-- kit-evidence: control=05 date=2026-10-09 result=pass -->

result is pass, partial or fail. date is the day the evidence was produced. The templates in ../evidence/ carry it.
"""
import argparse, datetime as dt, glob, json, os, re, subprocess, sys

CONTROLS = {
    "01": ("Access control", 100), "02": ("Secrets management", 365), "03": ("Change management", 100),
    "04": ("Environment separation", 365), "05": ("Backups and tested restores", 100),
    "06": ("Logging and monitoring", 365), "07": ("Vendor management", 365), "08": ("Data protection (GDPR)", 365),
    "09": ("Incident response", 365), "10": ("Supply chain and signing", 100),
    "11": ("Vulnerability management", 100), "12": ("Risk and governance", 365),
}
HEADER = re.compile(r"<!--\s*kit-evidence:\s*control=(\d{2})\s+date=(\d{4}-\d{2}-\d{2})\s+result=(pass|partial|fail)(?:\s+type=(\w+))?\s*-->")
TYPES = ("config", "operational", "effectiveness", "assurance")
RANK = {"fail": 0, "partial": 1, "pass": 2}
HEADLINE = "This is an evidence check, not a compliance assessment."


def split_row(line):
    """Split a Markdown table row into cells. A pipe inside a cell must be written \\| ; it is kept as |."""
    cells = re.split(r"(?<!\\)\|", line.strip())
    if cells and cells[0] == "":
        cells.pop(0)
    if cells and cells[-1] == "":
        cells.pop()
    return [c.replace("\\|", "|").strip() for c in cells]


def parse_date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


ANY_HEADER = re.compile(r"<!--\s*kit-evidence:(.*?)-->", re.S)


def scan_evidence(path):
    """Return (found, issues, nfiles). Nothing is skipped silently: unreadable files and bad headers are issues."""
    found, issues, nfiles = {}, [], 0
    for f in sorted(glob.glob(os.path.join(path, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(f, path)
        try:
            with open(f, encoding="utf-8") as fh:
                text = fh.read()
        except UnicodeDecodeError:
            issues.append((rel, "not valid UTF-8 text; not read"))
            continue
        except OSError as e:
            issues.append((rel, f"could not be read ({e.strerror or 'error'})"))
            continue
        nfiles += 1
        text = re.sub(r"```.*?```", "", text, flags=re.S)  # examples in code fences are not evidence
        for m in ANY_HEADER.finditer(text):
            body = m.group(1).strip()
            full = HEADER.fullmatch(m.group(0))
            if not full:
                if re.search(r"YYYY|NN\b|<", body):
                    issues.append((rel, "evidence header still has placeholder values (fill it in or remove the file)"))
                else:
                    issues.append((rel, f"malformed evidence header: {body[:70]}"))
                continue
            d = parse_date(full.group(2))
            if d is None:
                issues.append((rel, f"evidence header has an impossible date: {full.group(2)}"))
                continue
            if full.group(1) not in CONTROLS:
                issues.append((rel, f"evidence header names an unknown control: {full.group(1)}"))
                continue
            typ = full.group(4) if full.group(4) in TYPES else "unspecified"
            found.setdefault(full.group(1), []).append((d, full.group(3), rel, typ))
    return found, issues, nfiles


def load_evidence(path):
    return scan_evidence(path)[0]


def judge(found, today):
    rows = []
    for cid, (name, max_age) in CONTROLS.items():
        items = found.get(cid, [])
        if not items:
            rows.append((cid, name, "MISSING", "no dated evidence file", None, []))
            continue
        newest = max(i[0] for i in items)
        # Several files on the newest date: the worst result decides, so a pass cannot hide a fail.
        d, res, f, _ = min((i for i in items if i[0] == newest), key=lambda i: (RANK[i[1]], i[2]))
        # Which kinds of evidence are current and passing? (a file counts only if it is within the freshness limit)
        kinds = sorted({i[3] for i in items if i[1] == "pass" and i[0] <= today and (today - i[0]).days <= max_age})
        age = (today - d).days
        if d > today:
            status, note = "INVALID", f"{f} is dated in the future ({d})"
        elif age > max_age:
            status, note = "STALE", f"newest is {f}, {age} days old (limit {max_age})"
        elif res != "pass":
            status, note = "NOT PASSING", f"newest is {f}, result {res}"
        else:
            status, note = "PRESENT", f"{f}, {age} days old, pass"
        rows.append((cid, name, status, note, d, kinds))
    return rows


BANDS = [(4, "low"), (9, "medium"), (15, "high"), (25, "critical")]
TREATMENTS = {"mitigate", "avoid", "transfer", "accept"}


def band(score):
    return next(name for top, name in BANDS if score <= top)


def check_risks(path, today):
    """Risk register (evidence/risk-register.md): 15 columns. See risk/methodology.md for the rules checked."""
    problems, total = [], 0
    if not path or not os.path.exists(path):
        return ["NOT ASSESSED: no risk register supplied"], 0
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except (OSError, UnicodeDecodeError) as e:
        return [f"risk register could not be read ({type(e).__name__})"], 0
    for line in lines:
        cells = split_row(line)
        if not cells or not re.match(r"R-\d+", cells[0]):
            continue
        if len(cells) != 15:
            total += 1
            problems.append(f"{cells[0]}: row has {len(cells)} columns, expected 15 (an unescaped | inside a cell shifts the columns); not assessed")
            continue
        rid, likelihood, impact, rating, treatment, accepted_by, owner, target, review, status, evidence = (
            cells[0], cells[4], cells[5], cells[6], cells[8], cells[9], cells[10], cells[11], cells[12], cells[13], cells[14])
        total += 1
        closed = status.lower().startswith("closed")
        if closed:
            if placeholder(evidence):
                problems.append(f"{rid}: closed without evidence of treatment")
            continue
        try:
            lk, im = int(likelihood), int(impact)
            if not (1 <= lk <= 5 and 1 <= im <= 5):
                raise ValueError
            if rating.strip().lower() != band(lk * im):
                problems.append(f"{rid}: rating '{rating}' does not match {lk} x {im} = {lk * im} ({band(lk * im)})")
        except ValueError:
            lk = im = None
            problems.append(f"{rid}: likelihood and impact must be whole numbers from 1 to 5")
        t = treatment.strip().lower()
        if t not in TREATMENTS:
            problems.append(f"{rid}: no treatment decision (mitigate, avoid, transfer or accept)")
        if placeholder(owner):
            problems.append(f"{rid}: no owner")
        rd = parse_date(review)
        if rd is None:
            problems.append(f"{rid}: no valid review date")
        elif rd < today:
            problems.append(f"{rid}: review overdue since {rd}")
        if t in ("mitigate", "avoid", "transfer"):
            td = parse_date(target)
            if td is None:
                problems.append(f"{rid}: {t} but no valid target date")
            elif td < today and not status.lower().startswith("treated"):
                problems.append(f"{rid}: target date {td} has passed")
        if t == "accept":
            if placeholder(accepted_by):
                problems.append(f"{rid}: accepted but nobody recorded as accepting it")
            elif lk and im and band(lk * im) in ("high", "critical") and accepted_by.strip().lower() == owner.strip().lower():
                problems.append(f"{rid}: a {band(lk * im)} risk is accepted by its own owner")
    return problems, total


def placeholder(v):
    v = v.strip()
    return (not v) or v.startswith("<") or v in ("-", "TBD", "tbd")


def check_incidents(path, today, open_days=30):
    """Incident register. Returns (problems, total). One row per INC-n; see evidence/incident-register.md."""
    if not path or not os.path.exists(path):
        return ["NOT ASSESSED: no incident register supplied (a register saying 'no incidents recorded since <date>' is fine)"], 0
    problems, total = [], 0
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except (OSError, UnicodeDecodeError) as e:
        return [f"incident register could not be read ({type(e).__name__})"], 0
    for line in lines:
        cells = split_row(line)
        if not cells or not re.match(r"INC-\d+", cells[0]):
            continue
        if len(cells) != 9:
            total += 1
            problems.append(f"{cells[0]}: row has {len(cells)} columns, expected 9 (an unescaped | inside a cell shifts the columns); not assessed")
            continue
        iid, detected, sev, summary, personal, notif, report, owner, status = cells[:9]
        total += 1
        if placeholder(sev) or placeholder(summary) or placeholder(owner):
            problems.append(f"{iid}: severity, summary or owner not filled in")
        m = re.search(r"\d{4}-\d{2}-\d{2}", detected)
        d = parse_date(m.group(0)) if m else None
        if d is None:
            problems.append(f"{iid}: no valid detected date")
        if personal.lower().startswith(("yes", "unknown")) and placeholder(notif):
            problems.append(f"{iid}: personal data involved or unknown but no notification decision recorded (GDPR Art. 33(5))")
        closed = status.lower().startswith("closed")
        if closed and placeholder(report):
            problems.append(f"{iid}: closed without a linked report")
        if not closed and d and (today - d).days > open_days:
            problems.append(f"{iid}: still {status or 'open'} after {(today - d).days} days")
    return problems, total


def unticked(controls_dir):
    out = []
    if controls_dir and os.path.isdir(controls_dir):
        for f in sorted(glob.glob(os.path.join(controls_dir, "[0-9][0-9]-*.md"))):
            with open(f, encoding="utf-8") as fh:
                n = sum(1 for l in fh if l.lstrip().startswith("- [ ]"))
            if n:
                out.append((os.path.basename(f), n))
    return out


def gh(args):
    r = subprocess.run(["gh", "api"] + args, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    try:
        return json.loads(r.stdout or "null")
    except ValueError:
        raise RuntimeError("gh returned something that is not JSON (rate limit or an error page?)")


def check_github(repo, branch):
    """Read-only. Calls: GET /repos/{repo}/rulesets, GET /repos/{repo}/rulesets/{id}."""
    calls = [f"GET /repos/{repo}/rulesets", f"GET /repos/{repo}/rulesets/<id> (once per ruleset)"]
    findings = []
    try:
        listing = gh([f"repos/{repo}/rulesets"])
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as e:
        return calls, [("ERROR", f"could not read rulesets: {e}")]
    rulesets = []
    for rs in listing or []:
        try:
            rulesets.append(gh([f"repos/{repo}/rulesets/{rs['id']}"]))
        except (RuntimeError, OSError, subprocess.TimeoutExpired) as e:
            findings.append(("ERROR", f"could not read ruleset {rs.get('id')}: {e}"))
    active = [r for r in rulesets if r.get("enforcement") == "active" and r.get("target") == "branch"]

    def applies(r):
        inc = r.get("conditions", {}).get("ref_name", {}).get("include", [])
        return any(i in ("~DEFAULT_BRANCH", f"refs/heads/{branch}", "~ALL") for i in inc)

    mine = [r for r in active if applies(r)]
    types = {x["type"] for r in mine for x in r.get("rules", [])}
    if not mine:
        findings.append(("FAIL", f"no active branch ruleset applies to {branch}"))
    else:
        for need, why in (("pull_request", "pull request required"), ("required_status_checks", "named status checks required"),
                          ("non_fast_forward", "force pushes blocked"), ("deletion", "deletion blocked")):
            findings.append(("PASS" if need in types else "FAIL", why))
        ctx = [c for r in mine for x in r.get("rules", []) if x["type"] == "required_status_checks"
               for c in x.get("parameters", {}).get("required_status_checks", [])]
        findings.append(("PASS" if ctx else "FAIL", f"{len(ctx)} required check(s) listed by name"))
        bypass = [b for r in mine for b in r.get("bypass_actors", [])]
        findings.append(("PASS" if not bypass else "FAIL", "no bypass actors" if not bypass else f"{len(bypass)} bypass actor(s)"))
    return calls, findings


def main(argv=None):
    ap = argparse.ArgumentParser(description="Evidence check, not a compliance assessment.")
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--risks")
    ap.add_argument("--incidents")
    ap.add_argument("--controls")
    ap.add_argument("--github")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--today")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    today = parse_date(a.today) if a.today else dt.date.today()
    if a.today and today is None:
        print("error: --today must be a date like 2026-10-09", file=sys.stderr)
        return 2
    if not os.path.isdir(a.evidence):
        print(f"error: evidence folder not found: {a.evidence}", file=sys.stderr)
        return 2
    for flag, val in (("--risks", a.risks), ("--incidents", a.incidents)):
        if val and not os.path.isfile(val):
            print(f"error: {flag} file not found: {val}", file=sys.stderr)
            return 2
    if a.controls and not os.path.isdir(a.controls):
        print(f"error: --controls folder not found: {a.controls}", file=sys.stderr)
        return 2
    found, issues, nfiles = scan_evidence(a.evidence)
    rows = judge(found, today)
    risk_problems, risk_total = check_risks(a.risks, today)
    inc_problems, inc_total = check_incidents(a.incidents, today)
    ticks = unticked(a.controls)
    L = [f"# Evidence check, {today}", "", f"**{HEADLINE}** Present evidence shows a control was exercised on a date; "
         "it does not show the control is adequate or that you comply with any framework.", "",
         "| # | Control | Status | Detail | Current passing evidence types |", "|---|---|---|---|---|"]
    bad = 0
    for cid, name, status, note, _, kinds in rows:
        L.append(f"| {cid} | {name} | **{status}** | {note} | {', '.join(kinds) or 'none'} |")
        bad += status != "PRESENT"
    no_eff = [cid for cid, _, _, _, _, kinds in rows if "effectiveness" not in kinds and "assurance" not in kinds]
    L += ["", "## Kinds of evidence", "",
          "Evidence types: **config** (a setting is on), **operational** (a process was carried out), **effectiveness** (a test showed the control achieves its outcome), **assurance** (an independent party assessed it). "
          "Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.", "",
          "Controls with no current passing effectiveness or assurance evidence: " + (", ".join(no_eff) if no_eff else "none") + ". "
          "This is information, not a failure, and it does not change the exit status."]
    L += ["", "## Evidence file problems", ""]
    if issues:
        L += [f"- `{f}`: {m}" for f, m in issues]
        bad += len(issues)
    else:
        L.append("None. Every evidence header that was found could be read.")
    L += ["", "## Risk register", ""]
    if risk_problems:
        L += [f"- {p}" for p in risk_problems]
        bad += len(risk_problems)
    else:
        L.append(f"{risk_total} row(s), none overdue, all with an owner.")
    L += ["", "## Incident register", ""]
    if inc_problems:
        L += [f"- {p}" for p in inc_problems]
        bad += len(inc_problems)
    else:
        L.append(f"{inc_total} incident(s) recorded; each has an owner, and every closed one has a report. "
                 + ("Confirm that zero incidents is true." if inc_total == 0 else ""))
    if a.controls:
        L += ["", "## Unticked 'Done when' boxes", ""]
        L += ([f"- {f}: {n} unticked" for f, n in ticks] if ticks else ["None."])
        bad += sum(n for _, n in ticks)
    if a.github:
        calls, findings = check_github(a.github, a.branch)
        L += ["", f"## GitHub: {a.github} ({a.branch})", "", "Automated configuration check. It is reported separately from the evidence files above and says nothing about whether your delivery process as a whole is secure.", "", "Read-only calls made: " + ", ".join(f"`{c}`" for c in calls), ""]
        L += [f"- {st}: {t}" for st, t in findings]
        bad += sum(1 for s, _ in findings if s != "PASS")
    ran = lambda ok: "ran" if ok else "**not run**"
    L += ["", "## What this run checked", "", "| Check | Result |", "|---|---|",
          f"| Evidence files | {nfiles} read, {sum(len(v) for v in found.values())} valid header(s), {len(issues)} problem(s) |",
          f"| Risk register | {ran(bool(a.risks))}{'' if a.risks else ' (not supplied)'} |",
          f"| Incident register | {ran(bool(a.incidents))}{'' if a.incidents else ' (not supplied)'} |",
          f"| Unticked 'Done when' boxes | {ran(bool(a.controls))}{'' if a.controls else ' (not requested)'} |",
          f"| GitHub branch rules | {ran(bool(a.github))}{'' if a.github else ' (not requested)'} |",
          "", "**Not assessed by this tool, in any run:** whether any control actually works; whether you comply with any law, contract or framework; "
          "cloud configuration (use the commands in `verify/` and save the output as evidence); and the contents of an evidence file beyond its header.", "",
          f"**Result: {'INTERNAL EVIDENCE CHECK COMPLETE' if bad == 0 else str(bad) + ' item(s) need attention'}.** {HEADLINE}"]
    if bad == 0:
        L.append("Complete here means the check found nothing missing. It is not an examination, certification or audit, and it does not mean any control works.")
    L.append("")
    report = "\n".join(L)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(report)
    print(report)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
