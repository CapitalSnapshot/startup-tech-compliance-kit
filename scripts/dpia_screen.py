#!/usr/bin/env python3
"""Preliminary DPIA screening: decision support, not a legal threshold.

  python3 scripts/dpia_screen.py answers.json [--markdown]

Reads a JSON file of answers (see privacy/dpia-answers.example.json) and prints the screening outcome with its reasons and
anything missing. It implements the rules on privacy/dpia-screening.md so they can be tested.

Rules:
  * A SERIOUS indicator (GDPR Art. 35(3)(a) to (c), or the processing is on your supervisory authority's published list,
    Art. 35(4)) answered "yes" or "unsure" gives "DPIA likely required or seek advice", whatever the number of other
    answers. A score never overrides a serious indicator.
  * Further risk factors only count toward "DPIA recommended". They are NOT from Article 35 itself (see the page).
  * "May not be required" is allowed only when every field is complete, including the supervisory authority list you
    consulted, and no serious indicator is present. It is never a conclusion that a DPIA is not required.
Python 3 standard library only.
"""
import argparse
import json
import sys

SERIOUS = {
    "art35_3a": "Systematic and extensive evaluation of personal aspects based on automated processing, including profiling, on which decisions are based that produce legal effects or similarly significantly affect people (Art. 35(3)(a))",
    "art35_3b": "Large-scale processing of special categories of data (Art. 9(1)) or of data on criminal convictions and offences (Art. 10) (Art. 35(3)(b))",
    "art35_3c": "Systematic monitoring of a publicly accessible area on a large scale (Art. 35(3)(c))",
    "authority_list": "The kind of processing is on your supervisory authority's published list of processing that needs a DPIA (Art. 35(4))",
}
FACTORS = {
    "vulnerable_people": "Vulnerable people (for example children, patients, employees in some settings)",
    "innovative_technology": "Innovative technology, or a new use of existing technology (including some AI uses)",
    "combining_datasets": "Matching or combining data sets from different sources",
    "blocks_a_right": "Processing that may stop people exercising a right or using a service",
}
FIELDS = ["activity", "context", "nature", "scope", "purposes", "affected_people", "severity_of_harm", "likelihood_of_harm",
          "decision_owner", "decision_date", "review_date", "authority_name", "authority_list_name", "authority_list_checked_on"]
ANSWERS = ("yes", "no", "unsure")

LIKELY = "DPIA likely required or seek advice"
RECOMMENDED = "DPIA recommended; document your reasoning"
MAY_NOT = "DPIA may not be required; record the reasons and review"
INCOMPLETE = "Cannot decide: complete the missing fields"


def _blank(v):
    return v is None or str(v).strip() == "" or str(v).strip().startswith("<")


def screen(a):
    """Return the outcome and the reasons. Raises ValueError for an answer that is not yes, no or unsure."""
    missing, reasons = [], []
    answers = {}
    for key in list(SERIOUS) + list(FACTORS):
        v = a.get(key)
        if _blank(v):
            missing.append(key)
            continue
        v = str(v).strip().lower()
        if v not in ANSWERS:
            raise ValueError(f"{key}: answer must be one of {', '.join(ANSWERS)}, not {v!r}")
        answers[key] = v
    for f in FIELDS:
        if _blank(a.get(f)):
            missing.append(f)
    serious = [k for k in SERIOUS if answers.get(k) in ("yes", "unsure")]
    factors = [k for k in FACTORS if answers.get(k) in ("yes", "unsure")]
    for k in serious:
        reasons.append(("Unsure answer treated as a hit: " if answers[k] == "unsure" else "Serious indicator: ") + SERIOUS[k])
    if serious:
        outcome = LIKELY
        reasons.append("A single serious indicator is enough. The number of other answers does not change this outcome.")
    elif missing:
        outcome = INCOMPLETE
        reasons.append("Missing: " + ", ".join(missing))
    elif len(factors) >= 2:
        outcome = RECOMMENDED
        reasons += ["Further risk factor: " + FACTORS[k] for k in factors]
        reasons.append("Two or more further risk factors were found. This is a screening aid, not a legal threshold.")
    else:
        outcome = MAY_NOT
        reasons += ["Further risk factor: " + FACTORS[k] for k in factors]
        reasons.append("No serious indicator was found on the facts recorded and the supervisory authority list was consulted. "
                       "This is not a conclusion that a DPIA is not required: Art. 35(1) turns on whether the processing is likely to "
                       "result in a high risk, taking into account its nature, scope, context and purposes.")
    return {"outcome": outcome, "reasons": reasons, "missing": missing, "record_complete": not missing,
            "score": len(factors), "score_is_not_a_legal_threshold": True,
            "decision": {k: a.get(k) for k in ("decision_owner", "decision_date", "review_date")}}


def render(result):
    out = [f"# DPIA screening outcome", "", f"**{result['outcome']}**", "",
           "Preliminary screening. Decision support only, not a legal threshold or a legal conclusion.", "", "## Reasons", ""]
    out += [f"- {r}" for r in result["reasons"]]
    out += ["", "## Decision record", "", f"- Owner: {result['decision']['decision_owner'] or 'MISSING'}",
            f"- Date: {result['decision']['decision_date'] or 'MISSING'}", f"- Review date: {result['decision']['review_date'] or 'MISSING'}",
            f"- Record complete: {'yes' if result['record_complete'] else 'no, missing: ' + ', '.join(result['missing'])}", ""]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Preliminary DPIA screening (decision support).")
    ap.add_argument("answers", help="JSON file of answers")
    ap.add_argument("--markdown", action="store_true", help="print Markdown instead of JSON")
    a = ap.parse_args(argv)
    try:
        with open(a.answers, encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError("the answers file must contain a JSON object")
        result = screen(data)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(render(result) if a.markdown else json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
