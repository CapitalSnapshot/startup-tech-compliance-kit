# Restore test

**When:** at least quarterly, and after any change to the database, storage or backup setup.
**Who:** someone with production read access to snapshots and permission to create and delete scratch resources.

## Before

- A scratch network location with no route to the internet and no route from production data stores to it.
- A written list of every scratch resource you will create, by exact name. You delete only those, by name.

## Steps

1. Note the time. Take a manual snapshot of the production database.
2. Restore it as a new scratch database instance from that snapshot. Note the time it becomes available.
3. From a host inside the network, compare the scratch database with production: table list, row counts per table, migration ledger, and a checksum of a few important tables.
4. Test any non-database state: restore the previous version of a stored object, restore a copy of any state file into a scratch volume, and start a scratch copy of the service on it. Show it recognises a test record you created, then remove the test record from production.
5. Record the timings: snapshot, restore, verification, total.
6. Delete the scratch instance and the snapshot **by exact name**. Confirm they are gone.
7. Fill in [`../evidence/restore-test-report.md`](../evidence/restore-test-report.md).

## Passed when

Row counts and checksums match, the non-database state is recovered, the timings are recorded, and the scratch resources are confirmed deleted.

## Notes

- If production has little data yet, say so in the report: the timings are a floor, not your recovery time. Repeat with real data.
- Never leave a scratch copy of production data in place. It is a copy of your customers' data.
