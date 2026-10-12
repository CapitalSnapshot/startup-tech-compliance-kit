# E2. Cutover

Run in: a coding agent, with you sitting beside it. Phase 3. The window is the one sized in the Phase 2 timing and confirmed in the rehearsal.

Name one rollback decision owner and a rollback deadline before you start (for example 2 hours after the DNS switch; after that, forward-fix only).

```text
Phase 3, cutover. Production profile, one step at a time, waiting for my yes: (1) enable maintenance mode on the old system; (2) take a final production dump, restore it into the managed database and compare row counts on the key tables with the source; (3) run the final delta file sync; (4) rotate every credential listed in the Phase 0 credential inventory and load the new values into the CI system's environment-scoped secrets; (5) run the smoke suite through the hosts-file override; (6) update every callback URL and allowlist listed in infra/inventory/external-systems.md; (7) switch the DNS records to the load balancer; (8) verify from outside every item on <VERIFICATION LIST> and confirm <ENDPOINTS TO KEEP> still work; (9) close the maintenance window and make the old system stop serving traffic without stopping it. Log each step with a timestamp in infra/evidence/cutover.md. If any verification fails, stop and propose the rollback; I decide.
```

For step 9, use a maintenance page at the web server if you hold a no-firewall-changes rule on the old system; use the firewall otherwise.

Rollback: point DNS back at the old system and reopen it. Writes made to the new database during the window must be reversed by hand, which is why the window is short and announced.

Phase 3 exit criteria: every journey on the verification list passes from outside. Check with `python3 scripts/check_gates.py --infra ./infra --phase 3`.

Next: [F1. Decommission and evidence](F1-decommission-evidence.md)
