# Evidence templates

Copy these into your own repository and fill them in. Keep them dated and in version control: the history is part of the evidence.

| Template | Used by |
|---|---|
| [`evidence-file.md`](evidence-file.md) | Any control: a dated record that something was done and how it was checked |
| [`risk-register.md`](risk-register.md) | Scored risks, treatment decisions, owners, who accepted what ([`../risk/methodology.md`](../risk/methodology.md)) |
| [`handling.md`](handling.md) | How to store, redact, hash and share evidence |
| [`vendor-register.md`](vendor-register.md) | [`../controls/07-vendor-management.md`](../controls/07-vendor-management.md) |
| [`access-review.md`](access-review.md) | [`../controls/01-access-control.md`](../controls/01-access-control.md) |
| [`incident-register.md`](incident-register.md) and [`incident-report.md`](incident-report.md) | [`../controls/09-incident-response.md`](../controls/09-incident-response.md), [`../runbooks/incident-response.md`](../runbooks/incident-response.md) |
| [`restore-test-report.md`](restore-test-report.md) | [`../controls/05-backups-and-restore.md`](../controls/05-backups-and-restore.md) |

Rules for evidence: **dated**, **specific** (names, counts, hashes, not "all good"), **reproducible** (say how someone else could check), and **never containing a secret value**. Record the last four characters of a credential at most.

## Four kinds of evidence

Not all evidence says the same thing. Collect the right kind and label it.

| Type | What it shows | Example for backups |
|---|---|---|
| **config** | A setting is enabled | An export of the backup configuration and retention |
| **operational** | A process was carried out | The access review was done; the backup job ran last night |
| **effectiveness** | A test showed the control achieves its outcome | A dated restore test: data came back, row counts matched, the time was measured |
| **assurance** | An independent party assessed it | An external audit or penetration test report |

A backup configuration export proves a policy exists. A restore report proves one restoration was attempted successfully. Neither proves you can recover from every plausible disaster. Collect **both** for controls that matter, and be honest about the limits.

## The header line that `audit/kit-audit.py` reads

Each evidence file carries one comment near the top:

```
<!-- kit-evidence: control=05 date=2026-10-09 result=pass type=effectiveness -->
```

`control` is the control number (01 to 12), `date` is the day the evidence was produced, `result` is `pass`, `partial` or `fail`, and `type` (optional but recommended) is `config`, `operational`, `effectiveness` or `assurance`. The audit reads this line; it does not read the prose. It reports which kinds of current, passing evidence each control has, and lists controls with no effectiveness or assurance evidence. See [`../audit/`](../audit/).
