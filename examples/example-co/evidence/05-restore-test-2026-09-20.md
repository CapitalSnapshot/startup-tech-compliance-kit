# Restore test report , 2026-09-20

<!-- kit-evidence: control=05 date=2026-09-20 result=pass type=effectiveness -->

**Source:** production database **Snapshot:** manual-restoretest-20260920 **Scratch instance:** restoretest-scratch
**Run by:** platform owner **Runbook version:** v0.1.0

## Timings

| Step | Seconds |
|---|---|
| Manual snapshot to available | 95 |
| Restore to a scratch instance, to available | 410 |
| Verification | 30 |
| **Total, snapshot request to verified data** | **535** |

## Verification

| Check | Source | Restored | Match |
|---|---|---|---|
| Tables | 58 | 58 | Yes |
| Rows (sum) | 1,204,331 | 1,204,331 | Yes |
| Migration ledger rows | 37 | 37 | Yes |
| Checksums (named tables) | 9a2e41 | 9a2e41 | Yes |
| Non-database state recovered (objects, state files) | previous version of a test object | recovered | Yes |

## Result

**Pass.** No differences.

## Recovery objectives

RTO measured: about 9 minutes for the database. RPO from backup configuration: 5 minutes (point-in-time recovery). The business requirement is 4 hours, so the margin is large. **Not tested:** loss of the whole region or the cloud account.

## Clean-up

Scratch instance deleted at 09:52 UTC. Snapshot deleted at 09:53 UTC. Confirmed absent at 09:55 UTC.
