# Rollback

Going back to the old system after a cutover.

## Preconditions

- The old system has been kept running, patched, and firewalled but not deleted, for a stated rollback window.
- You know how much data was written to the new system since the switch, and how to bring it back.

## Steps

1. Declare the rollback and who decided. Note the time.
2. Put the new system into maintenance mode so it stops accepting writes.
3. Export the data written since the switch.
4. Reopen the old system's firewall and apply the export to it.
5. Switch DNS records back, one at a time, each confirmed by a person.
6. Run the smoke tests against the old system.
7. End maintenance mode. Announce.
8. Write a blameless note: why, what happened, what changes before the next attempt.

## After the rollback window closes

Take a last backup of the old system, record where it is kept, and only then retire it. Revoke any credentials created for the cutover (for example a DNS token).
