# A completed control: backups and tested restores

What "done" looks like for one control, for an invented company, **Example Co**. Everything here is made up; the files are in [`example-co/`](example-co/) and the audit output below is real output from `kit-audit.py` run over them.

## 1. The control

[`KIT-BKP-01`, backups and tested restores](../controls/05-backups-and-restore.md). Objective: *production data is backed up automatically, encrypted, kept off the primary system, and restored on a schedule to prove it works.*

## 2. What Example Co did

1. Turned on automated database backups (14 days, point-in-time recovery) and daily encrypted disk snapshots.
2. Turned on versioning for the file storage bucket.
3. Ran the read-only commands in [`verify/aws.md`](../verify/aws.md), section 05, and saved the output (with account identifiers redacted) as **configuration evidence**: [`05-backup-configuration-2026-09-20.md`](example-co/evidence/05-backup-configuration-2026-09-20.md).
4. Followed the [restore-test runbook](../runbooks/restore-test.md): snapshot, restore into a scratch instance, compare tables, rows, ledger and checksums, recover a deleted object from its version, time everything, delete the scratch resources. Filled in the [restore-test report](../evidence/restore-test-report.md) as **effectiveness evidence**: [`05-restore-test-2026-09-20.md`](example-co/evidence/05-restore-test-2026-09-20.md).
5. Noticed the test did not cover loss of a whole region, and recorded that as a scored risk with an owner and a date: [`risks.md`](example-co/risks.md).

## 3. The two kinds of evidence, side by side

| | Configuration evidence | Effectiveness evidence |
|---|---|---|
| Header | `result=pass type=config` | `result=pass type=effectiveness` |
| Shows | The backup policy is switched on | One restoration actually worked, in 535 seconds, with matching counts and checksums |
| Does **not** show | That a restore works | That Example Co could recover from every plausible disaster (say, loss of the whole region) |

Neither proves recovery from every disaster. That is why the region risk is in the register.

## 4. What the audit says

```text
$ python3 audit/kit-audit.py --evidence examples/example-co/evidence \
                             --risks examples/example-co/risks.md --today 2026-10-09

| 05 | Backups and tested restores | **PRESENT** | 05-backup-configuration-2026-09-20.md, 19 days old, pass | config, effectiveness |
Risk register: 1 row(s), none overdue, all with an owner.
```

The other eleven controls show **MISSING** because Example Co has only done this one. The audit checks that evidence is present, recent and recorded as passing. It does not say the backups are good enough: a person decides that, using the report's measured recovery time against the business requirement.

## 5. What a reviewer would see

A dated configuration export, a dated restore test with timings and matching counts, a stated recovery time against a stated requirement, a stated limit (region loss not tested), and a risk with an owner and a target date. That is a credible answer to "how do you know you can recover?".

## 6. Your turn

Copy [`evidence/restore-test-report.md`](../evidence/restore-test-report.md) and [`evidence/evidence-file.md`](../evidence/evidence-file.md) into your own repository, fill them in, and run the audit.
