#!/usr/bin/env python3
"""Validate the framework mappings and keep controls/framework-mappings.md in step with them.

  python3 scripts/validate_mappings.py            # validate and print a summary
  python3 scripts/validate_mappings.py --build    # regenerate controls/framework-mappings.md from controls/mappings.json
  python3 scripts/validate_mappings.py --check    # validate AND fail if the generated Markdown is stale (CI uses this)

controls/mappings.json is the source of truth. controls/mapping.schema.json describes one record. This script checks the
schema (a small standard-library checker for the keywords the schema uses) and the cross-field rules below.

Exit status: 0 valid (incomplete records are reported, and allowed only for community drafts); 1 errors or stale output;
2 an input file is missing or unreadable.

Rules beyond types:
  * coverage_status is one of exactly six values and is never blank.
  * "not covered" and "not applicable" need a substantive written rationale (mapping_rationale).
  * "covered" is allowed only when review.label is "maintainer reviewed" or "specialist reviewed"; a community draft cannot claim it.
  * "covered in part" must say what is not covered (exclusions).
  * review.label is one of three. For "maintainer reviewed" and "specialist reviewed", reviewer_role, review_date and decision are
    required. For "community draft" they (and the review rationale) must be null. review_date must be a real date, not in the future.
  * A value that starts with "<pending" is an explicit placeholder and the record is reported as incomplete. Placeholders are allowed
    only for a community draft whose coverage_status is "not assessed" or "needs expert review".
  * control_id must exist in controls/controls.json; ids are unique and start with the control id; every control has at least one
    record for every framework (silence is not a status).
  * data_date (top level) is a real date, not in the future; the coverage reports state it as "data as of".
  * DORA records need obligation_type; other frameworks must not have it; Art. 30 references must include "contractual flow-down".
"""
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MAPPINGS = os.path.join(ROOT, "controls", "mappings.json")
SCHEMA = os.path.join(ROOT, "controls", "mapping.schema.json")
CONTROLS = os.path.join(ROOT, "controls", "controls.json")
DOC = os.path.join(ROOT, "controls", "framework-mappings.md")
FRAMEWORKS = ["SOC 2", "ISO/IEC 27001", "GDPR", "DORA"]
PLACEHOLDER = "<pending"
OPEN_STATUSES = ("not assessed", "needs expert review")
OBLIGATION = ("direct statutory duty", "contractual flow-down", "oversight obligation")
FIELDS_WITH_PLACEHOLDERS = ["source_url", "mapping_rationale", "requirements_covered", "exclusions", "dependencies", "limitations", "source_reference"]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def is_placeholder(v):
    if isinstance(v, str):
        return v.strip().startswith(PLACEHOLDER)
    if isinstance(v, list):
        return any(is_placeholder(x) for x in v)
    return False


# ---- a small JSON Schema checker: type, enum, pattern, minLength, minItems, items, required, properties, additionalProperties ----
def _types(t):
    return t if isinstance(t, list) else [t]


def _is(v, t):
    return {"string": isinstance(v, str), "array": isinstance(v, list), "object": isinstance(v, dict), "null": v is None,
            "integer": isinstance(v, int) and not isinstance(v, bool), "boolean": isinstance(v, bool)}[t]


def check_schema(v, schema, path="$"):
    errs = []
    if "type" in schema and not any(_is(v, t) for t in _types(schema["type"])):
        return [f"{path}: expected {'/'.join(_types(schema['type']))}, got {type(v).__name__}"]
    if "enum" in schema and v not in schema["enum"]:
        errs.append(f"{path}: {v!r} is not one of {schema['enum']}")
    if isinstance(v, str):
        if "minLength" in schema and len(v) < schema["minLength"]:
            errs.append(f"{path}: must not be empty")
        if "pattern" in schema and not re.search(schema["pattern"], v):
            errs.append(f"{path}: {v!r} does not match {schema['pattern']}")
    if isinstance(v, list):
        if "minItems" in schema and len(v) < schema["minItems"]:
            errs.append(f"{path}: needs at least {schema['minItems']} item(s)")
        if "items" in schema:
            for i, x in enumerate(v):
                errs += check_schema(x, schema["items"], f"{path}[{i}]")
    if isinstance(v, dict):
        for k in schema.get("required", []):
            if k not in v:
                errs.append(f"{path}: missing required field '{k}'")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for k in v:
                if k not in props:
                    errs.append(f"{path}: unknown field '{k}'")
        for k, sub in props.items():
            if k in v:
                errs += check_schema(v[k], sub, f"{path}.{k}")
    return errs


def valid_date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def validate(data, schema, control_ids, today=None):
    """Return (errors, incomplete) where incomplete is a list of (record id, [fields])."""
    today = today or dt.date.today()
    errors, incomplete, seen = [], [], set()
    records = data.get("records") if isinstance(data, dict) else None
    if not isinstance(records, list):
        return ["$: mappings file must be an object with a 'records' list"], []
    dd = valid_date(data.get("data_date"))
    if dd is None:
        errors.append("$: data_date is required and must be a real date (YYYY-MM-DD); set it to the day a record last changed")
    elif dd > today:
        errors.append(f"$: data_date {dd} is in the future")
    for i, r in enumerate(records):
        rid = r.get("id", f"#{i}") if isinstance(r, dict) else f"#{i}"
        where = f"{rid}"
        if not isinstance(r, dict):
            errors.append(f"{where}: record must be an object")
            continue
        if isinstance(r.get("coverage_status"), str) and r["coverage_status"].strip() == "":
            errors.append(f"{where}: coverage_status is blank (a blank value is not allowed)")
        errors += [f"{where}: {e}" for e in check_schema(r, schema, "$")]
        if rid in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(rid)
        cid = r.get("control_id")
        if cid is not None and cid not in control_ids:
            errors.append(f"{where}: control_id {cid} is not a control in controls/controls.json")
        if isinstance(rid, str) and isinstance(cid, str) and not rid.startswith(cid + "."):
            errors.append(f"{where}: id must start with the control id {cid}")
        status = r.get("coverage_status")
        rev = r.get("review") if isinstance(r.get("review"), dict) else {}
        label = rev.get("label")
        pend = [f for f in FIELDS_WITH_PLACEHOLDERS if is_placeholder(r.get(f))]
        if pend:
            incomplete.append((rid, pend))
            if label != "community draft" or status not in OPEN_STATUSES:
                errors.append(f"{where}: placeholders ({', '.join(pend)}) are only allowed on a community draft with coverage_status "
                              f"'not assessed' or 'needs expert review'")
        if status in ("not covered", "not applicable"):
            why = r.get("mapping_rationale")
            if not isinstance(why, str) or is_placeholder(why) or len(why.strip()) < 20:
                errors.append(f"{where}: '{status}' needs a substantive written rationale in mapping_rationale")
        if status == "covered" and label not in ("maintainer reviewed", "specialist reviewed"):
            errors.append(f"{where}: 'covered' needs a maintainer reviewed or specialist reviewed label (a community draft cannot claim it)")
        if status == "covered in part" and (not r.get("exclusions") or is_placeholder(r.get("exclusions"))):
            errors.append(f"{where}: 'covered in part' must say what is not covered (exclusions)")
        if label in ("maintainer reviewed", "specialist reviewed"):
            for f in ("reviewer_role", "review_date", "decision"):
                if not rev.get(f):
                    errors.append(f"{where}: review.{f} is required when the label is '{label}'")
        elif label == "community draft":
            for f in ("reviewer_role", "review_date", "decision", "rationale"):
                if rev.get(f) is not None:
                    errors.append(f"{where}: review.{f} must be null for a community draft (no review has happened)")
        if rev.get("review_date") is not None:
            d = valid_date(rev["review_date"])
            if d is None:
                errors.append(f"{where}: review.review_date is not a real date")
            elif d > today:
                errors.append(f"{where}: review.review_date {d} is in the future")
        fw = r.get("framework")
        if fw == "DORA":
            if not r.get("obligation_type"):
                errors.append(f"{where}: DORA records need obligation_type")
            if any("Art. 30" in x for x in r.get("source_reference", []) if isinstance(x, str)) and "contractual flow-down" not in (r.get("obligation_type") or []):
                errors.append(f"{where}: an Art. 30 reference must include the obligation type 'contractual flow-down'")
        elif "obligation_type" in r or "obligation_detail" in r:
            errors.append(f"{where}: obligation_type is only for DORA records")
    present = {(r.get("control_id"), r.get("framework")) for r in records if isinstance(r, dict)}
    for cid in sorted(control_ids):
        for fw in FRAMEWORKS:
            if (cid, fw) not in present:
                errors.append(f"{cid}: no mapping record for {fw} (silence is not a status: add a record, even if 'not assessed')")
    return errors, incomplete


# ---- the generated Markdown ----
def fw_label(r):
    return {"SOC 2": "SOC 2 ({e})", "ISO/IEC 27001": "ISO/IEC 27001:{e}", "GDPR": "GDPR ({e})", "DORA": "DORA ({e})"}[r["framework"]].format(e=r["edition"])


def ref_cell(r):
    base = ", ".join(r["source_reference"])
    if r["framework"] == "DORA":
        detail = r.get("obligation_detail") or " and ".join(r["obligation_type"])
        for o in OBLIGATION:
            detail = detail.replace(o, f"**{o}**")
        return f"{base}: {detail}"
    return base


def cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


HEADER = """# Framework mappings

<!-- Generated by scripts/validate_mappings.py from controls/mappings.json. Do not edit by hand. -->

> **Standing notice.** This is repository based, community maintained guidance. It is not legal advice, a formal compliance assessment, a certification or an independent security audit. Mappings and statements about frameworks are unverified unless their review label says otherwise ([review labels](../docs/review-labels.md)).

Each row says: which framework **and edition**, the **reference**, the **coverage status**, **why it is relevant**, **what more is required**, and the **review label**. A control can support several requirements without satisfying any of them. **A reference means "relevant to", never "satisfies".** The data behind this page is [`mappings.json`](mappings.json), checked against [`mapping.schema.json`](mapping.schema.json).

## Editions mapped

| Framework | Edition | Notes |
|---|---|---|
| SOC 2 | AICPA 2017 Trust Services Criteria (with the 2022 revised points of focus) | Security (the common criteria) is always in scope; Availability, Confidentiality, Processing Integrity and Privacy are optional categories |
| ISO/IEC 27001 | 2022 edition (Annex A has 93 controls in four themes) | Certification also needs an ISMS: clauses 4 to 10 |
| GDPR | Regulation (EU) 2016/679 | National laws and your supervisory authority's guidance add detail |
| DORA | Regulation (EU) 2022/2554, applying from 17 January 2025 | **Not a universal startup requirement.** It applies to certain financial entities and their ICT third-party providers: see [`../scoping/applicability-matrix.md`](../scoping/applicability-matrix.md) |

## Review status

**Review label for every record: community draft** ([`../docs/review-labels.md`](../docs/review-labels.md)). The authors drafted these records. For GDPR and DORA they read the official text of the articles cited; for SOC 2 and ISO/IEC 27001 the criteria and standard text could not be read, and each such record says so. **No record has been reviewed by a maintainer or by a specialist**, so no reviewer, review date or decision is recorded. Frameworks change; check the current text before relying on a reference.

**Coverage statuses are the authors' draft judgements and none has been reviewed.** The six statuses (covered, covered in part, not covered, not applicable, not assessed, needs expert review) are defined in the same document. "Needs expert review" is used where the source text could not be read for this mapping, or a qualified judgement is needed; see each record's limitations. A status says how far the kit addresses a requirement. **It is not a statement that you meet the requirement.** A framework requirement that does not appear here has simply **not been assessed**.

{status_table}

**Record: incomplete** means one or more fields still hold an explicit "pending" placeholder that must be filled from the source. Only a community draft that is "not assessed" or "needs expert review" may be incomplete.

Companion files: [`evidence-map.md`](evidence-map.md) (which evidence supports which control) and the generated [coverage reports](../docs/coverage/README.md) (counts and lists per framework).

## Reminders that matter most

- **ISO/IEC 27001:** implementing the twelve controls does not replace an ISMS, risk treatment, a Statement of Applicability, internal audit, management review and continual improvement ([`../guide/paths/iso27001.md`](../guide/paths/iso27001.md)).
- **SOC 2:** the controls do not set your scope, choose your criteria, or create the operating history an examination needs ([`../guide/paths/soc2.md`](../guide/paths/soc2.md)).
- **GDPR:** security measures are one part; lawful basis, rights, retention and transfers are separate duties ([`../privacy/`](../privacy/)).
- **DORA:** check applicability first, and then **which kind of obligation** it would be. Duties of a financial entity are direct statutory duties on that entity. A startup serving one usually meets DORA as contractual flow-down (Art. 28 and 30). Designated critical ICT providers face oversight (Art. 31 onwards). See [`../scoping/dora-screening.md`](../scoping/dora-screening.md).
"""


def status_table(recs):
    statuses = ["covered", "covered in part", "not covered", "not applicable", "not assessed", "needs expert review"]
    rows = ["| Framework | " + " | ".join(statuses) + " | Records | Incomplete |", "|---|" + "---|" * (len(statuses) + 2)]
    inc = {rid for rid, _ in validate({"records": recs}, load(SCHEMA), {r["control_id"] for r in recs})[1]}
    for fw in FRAMEWORKS:
        rs = [r for r in recs if r["framework"] == fw]
        rows.append(f"| {fw} | " + " | ".join(str(sum(1 for r in rs if r["coverage_status"] == st)) for st in statuses)
                    + f" | {len(rs)} | {sum(1 for r in rs if r['id'] in inc)} |")
    return "\n".join(rows)


def build_doc(data, controls):
    out = [HEADER.replace("{status_table}", status_table(data["records"]))]
    recs = data["records"]
    inc = {rid for rid, _ in validate(data, load(SCHEMA), {c["id"] for c in controls})[1]}
    for c in controls:
        out.append(f"\n## {c['evidence_number']} {c['title']}\n")
        out.append(f"Control ID: `{c['id']}`\n")
        out.append("| Framework (edition) | Reference | Coverage status | Why relevant | What more is required | Review label | Record |")
        out.append("|---|---|---|---|---|---|---|")
        for r in (x for x in recs if x["control_id"] == c["id"]):
            record = "incomplete" if r["id"] in inc else "complete"
            out.append(f"| {cell(fw_label(r))} | {cell(ref_cell(r))} | {r['coverage_status']} | {cell(r['mapping_rationale'])} | "
                       f"{cell('; '.join(r['exclusions']))} | {r['review']['label']} | {record} |")
    return "\n".join(out) + "\n"


def summary(data, incomplete):
    from collections import Counter
    recs = data["records"]
    lines = [f"{len(recs)} record(s): {len(recs) - len(incomplete)} complete, {len(incomplete)} incomplete"]
    for fw in FRAMEWORKS:
        rs = [r for r in recs if r.get("framework") == fw]
        pend = sum(1 for rid, _ in incomplete if any(r.get("id") == rid and r.get("framework") == fw for r in rs))
        lines.append(f"  {fw}: {len(rs)} record(s), {pend} incomplete")
    lines.append("  coverage status: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(r.get("coverage_status") for r in recs).items())))
    lines.append("  review label: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter((r.get("review") or {}).get("label") for r in recs).items())))
    return "\n".join(lines)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        data, schema, controls = load(MAPPINGS), load(SCHEMA), load(CONTROLS)["controls"]
    except (OSError, ValueError) as e:
        print(f"error: could not read an input file: {e}", file=sys.stderr)
        return 2
    errors, incomplete = validate(data, schema, {c["id"] for c in controls})
    if "--build" in argv:
        if errors:
            print("not building: the mappings are invalid\n" + "\n".join(f"  {e}" for e in errors), file=sys.stderr)
            return 1
        with open(DOC, "w", encoding="utf-8") as fh:
            fh.write(build_doc(data, controls))
        print(f"wrote {os.path.relpath(DOC, ROOT)}")
        return 0
    rc = 0
    if errors:
        print("INVALID\n" + "\n".join(f"  {e}" for e in errors))
        rc = 1
    else:
        print("mappings are valid")
    if "--check" in argv and not errors:
        try:
            with open(DOC, encoding="utf-8") as fh:
                current = fh.read()
        except OSError:
            current = ""
        if current != build_doc(data, controls):
            print("controls/framework-mappings.md is out of date: run python3 scripts/validate_mappings.py --build", file=sys.stderr)
            rc = 1
        else:
            print("framework-mappings.md is up to date")
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        print(summary(data, incomplete))
    return rc


if __name__ == "__main__":
    sys.exit(main())
