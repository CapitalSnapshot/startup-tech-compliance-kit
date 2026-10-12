# Audit: an evidence check

`kit-audit.py` reads your evidence files and registers and tells you, per control, whether **dated evidence exists, is fresh, and passed**. It is the last step of the kit: do the controls, keep the evidence, then run this. When nothing is missing it says **"internal evidence check complete"**. That describes an internal check; it is not an examination, certification or audit.

> **This is an evidence check, not a compliance assessment.** Present evidence shows a control was exercised on a date. It does not show the control is adequate, or that you comply with SOC 2, ISO 27001, GDPR, DORA or anything else. The report says so at the top and the bottom.

## Run it

```bash
python3 audit/kit-audit.py --evidence path/to/your/evidence \
                           --risks    path/to/your/risk-register.md \
                           --incidents path/to/your/incident-register.md \
                           --controls path/to/your/copy/of/controls   # optional: counts unticked boxes
```

Python 3 standard library only. No network, no credentials, no changes. Add `--out report.md` to save the report. The exit status is 0 only when every control has fresh, passing evidence and nothing is overdue, so it can run in your CI.

## What it checks

| Check | Rule |
|---|---|
| Evidence exists | Each of the twelve controls has at least one file with a `kit-evidence` header (see [`../evidence/README.md`](../evidence/README.md)) |
| Evidence is fresh | Newest file is within the limit: 100 days for controls 01, 03, 05 and 10; 365 days for the others. Edit `CONTROLS` in the script to change them |
| Evidence passed | Newest result is `pass`. `partial` and `fail` are reported as not passing |
| Dates make sense | A date in the future is invalid |
| Risk register | Every open row: the rating matches likelihood times impact (1 to 5 each); a treatment (mitigate, avoid, transfer, accept); an owner; a review date that has not passed; a target date for mitigate, avoid or transfer; an accepting person for accept, who for a High or Critical risk is **not** its owner. A closed row carries evidence of treatment |
| Incident register | The file exists. Every incident has a severity, summary and owner. Personal data **yes or unknown** has a recorded notification decision, with its reason (GDPR Art. 33(5)). A closed incident has a linked report. An open incident older than 30 days is flagged. A register with no incidents is fine if true: the report asks you to confirm it |
| Unticked boxes | Optional: counts `- [ ]` left in your copy of the controls |

Examples inside fenced code blocks are ignored, so the templates and this documentation never count as evidence.

## What a pass does not tell you

A pass means the evidence is **present, recent, and recorded as passing**. It does not mean the control works. Take a restore-test report that says the database was restored. The audit can see that the report exists, is recent and says pass. It cannot establish that:

- the restored database held all the required data;
- the recovery time met what the business needs;
- the restored system was secure;
- the test reflected production;
- you could recover from a worse disaster than the one you tested.

Likewise a branch rule that exists does not make the whole delivery process secure. Effectiveness is judged by people: by testing, review, exceptions tracked and fixed, and, where it matters, independent assessment (levels 3 and 4 of the [maturity model](../guide/maturity-model.md)).

Treat automated configuration checks (the GitHub layer here, and any cloud-provider checks you add later) as a separate input from the evidence files, and keep them separate from your own judgement of effectiveness.

## Optional: GitHub branch rules (read-only)

```bash
python3 audit/kit-audit.py --evidence ... --github OWNER/REPO --branch main
```

Needs the `gh` CLI, signed in with read access. It makes exactly these calls and prints them in the report: `GET /repos/OWNER/REPO/rulesets` and `GET /repos/OWNER/REPO/rulesets/<id>` once per ruleset. It checks that an active ruleset applies to the branch and requires a pull request, named status checks (at least one), blocks force pushes and deletion, and has no bypass actors. It does not check classic branch protection; use rulesets.

Cloud-provider checks (MFA enforced, audit trail on, backups on, public access blocked) are not included yet. The base layer is provider-neutral on purpose; provider checks will be added one provider at a time and will each list the read-only calls they make.

## Tests

```bash
python3 -I -m unittest discover -s audit/tests -p "test_*.py" -v
```

They also cover the sanitise scanner (`scripts/sanitise_check.py`) and the migration skill's `check_gates.py`. For the audit they run it against an empty repository (all ten controls missing), a filled-in invented example (passes), stale and failing evidence, future dates, overdue risks, and the shipped templates (which must **not** count as evidence).
