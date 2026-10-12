# B4. Database compatibility and private connectivity

Run in: a coding agent. Phase 0, step 3. Read infra/guide/docs/variants for your database family (MySQL family or PostgreSQL) first.

```text
Phase 0, step 3. Dump the production schema only (structure, no data) and, following the variant note for <DB FAMILY>, list every feature that needs attention on <TARGET DB ENGINE>. List the engine versions the managed service offers and target the highest one that is not older than production; never downgrade. Write the findings to infra/inventory/db-compat.md. Then, using the non-production identity, work out whether the app hosts and the managed database will share a private network on <CLOUD PROVIDER>. If they do not, set up private connectivity (peering or a private endpoint). Create a throwaway managed database tagged env=nonprod with no public access, prove it is reachable from the dev host, record the proof in infra/evidence/db-connectivity.md, then delete it and record the deletion. Update CHECKLIST.md.
```

Phase 0 exit criteria: backup exists; inventory committed; both identities usable with MFA and the cross-environment deny proven; logging on and delivering; connectivity proven; external systems list committed. Check with `python3 scripts/check_gates.py --infra ./infra --phase 0`.

Next: [C1. Containerise the application](C1-containerise-application.md)
