# Cutover

Moving live traffic from an old system to a new one. Adapt the names; keep the order.

## Preconditions (all must be true)

- The new environment has passed its tests, and a **rehearsal** has run end to end with timings.
- A restore test has passed and the cutover window is sized from the measured restore, not a guess.
- Customers have been told the window, with the notice period you promised.
- The rollback runbook is current and its first step has been tried.
- Secrets for the new environment are in the secrets manager and have been rebuilt on the host after the last rotation.
- The state that must start empty (for example a client or token store) has been read back and confirmed empty.
- The edge (CDN or proxy) is configured and the origin authenticates the edge.

## Steps

1. Announce the start. Put the old system into maintenance mode.
2. Take a final full dump from the old system.
3. Load it into the new database. Verify row counts on the main tables against the source.
4. Do the final delta sync of files and verify with a manifest.
5. Run the smoke tests against the new system without changing DNS (hosts override or loopback).
6. Update every external registration to the new hostnames: payment webhook, identity provider redirects, email domain.
7. Rotate every credential in the old inventory. Load new values into the secrets manager, rebuild the environment files, redeploy, and re-run the smoke tests.
8. Switch the DNS records, one at a time, each confirmed by a person.
9. Run the post-switch verification, every line, before the window closes.
10. End maintenance mode. Announce completion.
11. Firewall the old system so it serves nothing, but keep it running for the rollback window.

## Rollback trigger

Decide in advance: a named condition (for example, error rate above a threshold for ten minutes, or a failed verification line) that triggers [`rollback.md`](rollback.md). The person who decides is named before you start.
