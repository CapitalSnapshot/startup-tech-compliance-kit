# Restore test report , <YYYY-MM-DD>

<!-- kit-evidence: control=05 date=YYYY-MM-DD result=pass type=effectiveness -->

**Source:** <database instance, by role> **Snapshot:** <name> **Scratch instance:** <name>
**Run by:** <role> **Runbook version:** <commit>

## Timings

| Step | Seconds |
|---|---|
| Manual snapshot to available | <...> |
| Restore to a scratch instance, to available | <...> |
| Verification | <...> |
| **Total, snapshot request to verified data** | **<...>** |

## Verification

| Check | Source | Restored | Match |
|---|---|---|---|
| Tables | <n> | <n> | Yes / No |
| Rows (sum) | <n> | <n> | Yes / No |
| Migration ledger rows | <n> | <n> | Yes / No |
| Checksums (named tables) | <hash> | <hash> | Yes / No |
| Non-database state recovered (objects, state files) | <...> | <...> | Yes / No |

## Result

**Pass / Fail.** <Differences, if any.>

## Recovery objectives

RTO measured: <...>. RPO from backup configuration: <...>. If production held little data, say so: these are a floor.

## Clean-up

Scratch instance <name> deleted at <time>. Snapshot <name> deleted at <time>. Confirmed absent at <time>.
