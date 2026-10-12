#!/usr/bin/env python3
"""kit-start: five questions, then a prioritised list of what to do first.

  python3 scripts/kit_start.py                      # asks the questions
  python3 scripts/kit_start.py --stage production --hosting managed-cloud --data personal \\
                               --framework questionnaires --people 4-10 [--out plan.md]

It reads nothing from your systems and sends nothing anywhere. It turns your answers into an ordered
reading and action list with links into this kit. It is a starting point, not an assessment: it cannot
tell you what law applies to you (see scoping/applicability-matrix.md).
Python 3 standard library only.
"""
import argparse
import sys

QUESTIONS = [
    ("stage", "Where are you?", [
        ("prelaunch", "Pre-launch, no customers yet"),
        ("production", "In production, with customers"),
        ("enterprise", "Serving, or selling to, enterprise customers")]),
    ("hosting", "Where does your application run?", [
        ("managed-cloud", "Managed cloud services (containers, a managed database)"),
        ("single-host", "A single server or virtual machine"),
        ("paas", "A platform-as-a-service"),
        ("legacy", "A legacy production environment I need to move off")]),
    ("data", "What kinds of data do you process?", [
        ("none", "No customer data yet"),
        ("business", "Business data, but no personal data"),
        ("personal", "Personal data"),
        ("special", "Special-category data, children's data or payment card data")]),
    ("framework", "Does any customer require a specific compliance framework?", [
        ("none", "No"),
        ("questionnaires", "Security questionnaires only"),
        ("soc2", "SOC 2 has been asked for"),
        ("iso27001", "ISO 27001 has been asked for"),
        ("financial", "We serve regulated financial services customers")]),
    ("people", "How many people have access to your systems?", [
        ("1-3", "1 to 3"), ("4-10", "4 to 10"), ("11-50", "11 to 50"), ("50+", "More than 50")]),
]

C = "controls/"
LINKS = {
    "scoping": ("Fill in the scoping questionnaire and read the applicability matrix", "scoping/questionnaire.md"),
    "firstweek": ("Do the first-week checklist", "checklists/first-week.md"),
    "layers": ("Read what the kit can and cannot establish", "guide/layers-and-outcomes.md"),
    "01": ("Access control: MFA, named accounts, a second owner", C + "01-access-control.md"),
    "02": ("Secrets management: out of code, in a secrets manager", C + "02-secrets-management.md"),
    "03": ("Change management: protected branches, reviewed changes", C + "03-change-management.md"),
    "04": ("Environment separation: no production data outside production", C + "04-environment-separation.md"),
    "05": ("Backups, and a tested restore", C + "05-backups-and-restore.md"),
    "06": ("Logging and monitoring: audit trail, alerts with recipients", C + "06-logging-and-monitoring.md"),
    "07": ("Vendor management: a register and signed agreements", C + "07-vendor-management.md"),
    "09": ("Incident response: an owner, a register, the first-hour runbook", C + "09-incident-response.md"),
    "10": ("Supply chain: signed builds verified on the host", C + "10-supply-chain-and-signing.md"),
    "11": ("Vulnerability management: scans and remediation deadlines", C + "11-vulnerability-management.md"),
    "12": ("Risk and governance: roles, risk register, short policies", C + "12-risk-and-governance.md"),
    "risk": ("Start the risk register with the five biggest gaps you know about", "evidence/risk-register.md"),
    "securedev": ("Secure development policy", "policies/secure-development-policy.md"),
    "beforecustomer": ("Work through the before-the-first-customer checklist", "checklists/before-first-customer.md"),
    "dd": ("Prepare the due diligence pack", "checklists/before-investor-data-room.md"),
    "verify": ("Produce evidence with the read-only verify commands", "verify/README.md"),
    "audit": ("Run the evidence check regularly", "audit/README.md"),
    "migration": ("Plan the move off the legacy environment with the migration skill (separately, with a tested restore first)", "skills/production-migration/SKILL.md"),
    "restore": ("Restore-test runbook, before you migrate anything", "runbooks/restore-test.md"),
    "gdprscope": ("Check whether the GDPR's territorial scope may apply to you (the location of people is not the only test)", "scoping/gdpr-territorial-scope.md"),
    "privacy": ("Privacy operating process", "privacy/README.md"),
    "dpia": ("Screen for a DPIA and a DPO", "privacy/dpia-screening.md"),
    "special": ("Special-category or card data: take specialist advice; avoid card-data scope by using a payment processor", "scoping/applicability-matrix.md"),
    "soc2": ("Read the SOC 2 path", "guide/paths/soc2.md"),
    "iso": ("Read the ISO 27001 path", "guide/paths/iso27001.md"),
    "financial": ("Screen for DORA: direct duties, contract terms from financial-entity customers, or oversight", "scoping/dora-screening.md"),
    "mapreq": ("Map each customer requirement to your controls", "controls/framework-mappings.md"),
    "formal": ("Decide whether formal assurance is needed", "guide/roadmap.md"),
    "accessreview": ("Schedule the access review", "evidence/access-review.md"),
    "joiners": ("Joiner, mover, leaver process", "policies/onboarding-and-offboarding.md"),
    "policies": ("Short policies, acknowledged by staff", "policies/README.md"),
    "training": ("Security awareness training", "policies/security-awareness-training.md"),
    "paas": ("PaaS: know your exit path and shared-responsibility limits", C + "07-vendor-management.md"),
    "singlehost": ("Single host: snapshots, a second admin, no hand edits on the server", C + "05-backups-and-restore.md"),
    "workflow": ("Follow the end-to-end workflow", "workflow/README.md"),
}


def plan(a):
    """Return {"now": [...], "next": [...], "later": [...]} of link keys, in order, no duplicates."""
    now, nxt, later = ["layers", "scoping", "firstweek", "01", "02", "03"], [], []
    st, hosting, data, fw, people = a["stage"], a["hosting"], a["data"], a["framework"], a["people"]
    if st == "prelaunch":
        now += ["securedev", "04"]
        nxt += ["05", "06", "beforecustomer"]
        later += ["09", "07", "11", "12"]
    elif st == "production":
        now += ["05", "06", "09"]
        nxt += ["07", "11", "12", "risk"]
        later += ["audit", "verify"]
    else:  # enterprise
        now += ["05", "06", "09"]
        nxt += ["07", "11", "12", "risk", "verify", "audit"]
        later += ["dd", "mapreq", "formal"]
    if hosting == "legacy":
        now += ["restore"]
        nxt += ["migration"]
    elif hosting == "single-host":
        now += ["singlehost"]
    elif hosting == "paas":
        nxt += ["paas"]
    elif hosting == "managed-cloud":
        nxt += ["verify"]
    if data in ("personal", "special"):
        (now if st != "prelaunch" else nxt).extend(["gdprscope", "privacy"])
        nxt += ["dpia"]
        if data == "special":
            now += ["special"]
    elif data == "business" or data == "none":
        later += ["privacy"]
    if fw == "soc2":
        nxt += ["soc2", "mapreq"]
        later += ["formal"]
    elif fw == "iso27001":
        nxt += ["iso", "mapreq"]
        later += ["formal"]
    elif fw == "financial":
        now += ["financial"]
        nxt += ["mapreq"]
        later += ["formal"]
    elif fw == "questionnaires":
        nxt += ["dd", "verify"]
    if people in ("4-10", "11-50", "50+"):
        nxt += ["joiners", "accessreview"]
    if people in ("11-50", "50+"):
        nxt += ["policies", "training"]
    later += ["workflow"]
    seen, out = set(), {"now": [], "next": [], "later": []}
    for bucket, items in (("now", now), ("next", nxt), ("later", later)):
        for k in items:
            if k not in seen:
                seen.add(k)
                out[bucket].append(k)
    return out


def render(a):
    p = plan(a)
    lines = ["# Your starting plan", "",
             "Generated by `scripts/kit_start.py` from five answers. A starting point, not an assessment. What applies to you "
             "depends on your customers, data and law: see `scoping/applicability-matrix.md`.", "", "## Your answers", ""]
    for key, question, options in QUESTIONS:
        label = dict(options)[a[key]]
        lines.append(f"- {question} **{label}**")
    for bucket, title in (("now", "Do now (this week)"), ("next", "Next (this month)"), ("later", "Later (when it applies)")):
        lines += ["", f"## {title}", ""]
        for i, k in enumerate(p[bucket], 1):
            text, path = LINKS[k]
            lines.append(f"{i}. {text}: `{path}`")
    lines += ["", "Do not pursue a formal framework because it is on a list. Pursue it when a customer, contract, regulator or plan requires it.", ""]
    return "\n".join(lines)


def ask(key, question, options):
    print(f"\n{question}")
    for i, (val, label) in enumerate(options, 1):
        print(f"  {i}. {label}")
    while True:
        raw = input("Choose a number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1][0]
        print("Please enter one of the numbers shown.")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Five questions, then a prioritised plan.")
    for key, question, options in QUESTIONS:
        ap.add_argument(f"--{key}", choices=[o[0] for o in options], help=question)
    ap.add_argument("--out", help="write the plan to this Markdown file")
    a = vars(ap.parse_args(argv))
    out = a.pop("out")
    answers = {k: a[k] for k, _, _ in QUESTIONS}
    if any(v is None for v in answers.values()):
        if not sys.stdin.isatty() and all(v is None for v in answers.values()):
            ap.error("give all five answers as options, or run this in a terminal to be asked")
        for key, question, options in QUESTIONS:
            if answers[key] is None:
                answers[key] = ask(key, question, options)
    text = render(answers)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
