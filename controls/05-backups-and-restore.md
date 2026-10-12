# 5. Backups and tested restores

| | |
|---|---|
| **Control ID** | KIT-BKP-01 |
| **Evidence number** | 05 (the `control=` value in evidence headers) |
| **Applies to** | Systems that hold business-critical data, including state outside the database |
| **Owner (role)** | The owner of each system; a named restore-test owner |
| **Review frequency** | Every 100 days or sooner (quarterly); the audit flags evidence older than 100 days |
| **Limitations** | Backup configuration shows a policy exists. A restore test shows one restoration worked. Neither proves you could recover from every plausible disaster, or meet your business's recovery needs |

**Objective:** Production data is backed up automatically, encrypted, kept off the primary system, and restored on a schedule to prove it works.

## What to do

- Turn on automated database backups with point-in-time recovery, and automatic snapshots of the host disk.
- Back up object storage with versioning, and back up any state held outside the database (for example an OAuth client store).
- Encrypt backups at rest and keep them in a place the production host's credentials cannot delete. A host that can write a backup should not be able to read or erase old ones.
- Restore into a scratch environment on a schedule, compare row counts and checksums with the source, time it, and delete the scratch resources.
- Write down your recovery time and recovery point objectives from the measured restore, not from a guess.

## Why a reviewer asks

Reviewers ask for the last restore test and its timings. A backup policy without a restore test is treated as a gap.

## Done when

- [ ] Automated backups are on, encrypted, and retained for a stated period.
- [ ] A restore test has been run in the last quarter, with timings and a pass or fail result.
- [ ] Backups of non-database state exist and have been restored at least once.
- [ ] The host's credentials can write backups but cannot read or delete them.

## Evidence to keep

- The backup configuration.
- The completed restore-test report ([`evidence/restore-test-report.md`](../evidence/restore-test-report.md)).
- The measured RTO and RPO.
- Proof the scratch resources were deleted.

### Kinds of evidence

- **Configuration:** Backup configuration and retention
- **Operational:** The backup job log
- **Effectiveness:** A dated restore test with timings, row counts and checksums ([`../evidence/restore-test-report.md`](../evidence/restore-test-report.md))
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- Never restoring, then discovering during an incident that the backup is empty or encrypted with a lost key.
- Backups kept beside the data they protect.
- Testing the restore only against an empty database.
- Forgetting files and state that live outside the database.

## Indicative framework references

SOC 2 A1.2, A1.3 · ISO 27001:2022 A.8.13, A.8.14, A.5.30 · GDPR Art. 32(1)(c) · DORA Art. 11, 12

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

Read-only commands for AWS, Google Cloud and Azure, with a status line on each: [`../verify/`](../verify/) (section 05). Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../runbooks/restore-test.md`](../runbooks/restore-test.md)
- [`../runbooks/rebuild-from-nothing.md`](../runbooks/rebuild-from-nothing.md)
- [`../evidence/restore-test-report.md`](../evidence/restore-test-report.md)
