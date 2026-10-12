# F1. Decommission and evidence

Run in: a coding agent. Phase 4. Only after 14 days with no rollback trigger.

```text
Phase 4, 14 days after cutover with no rollback trigger. Take a final backup of the old system and record its name; ask me to confirm; then delete the old system and its static IP. Delete any local production dumps from my laptop and drives. Record both deletions in infra/evidence/decommission.md. Write infra/RUNBOOK-REBUILD.md so a new production environment can be rebuilt from the pipeline, and run the first rebuild test in the non-production profile. If PATH is full, assemble infra/evidence-pack/ with the plan, access policy export, firewall export, TLS scan results, the pipeline run for the cutover deploy, backup configuration, the restore test and timing results, the rehearsal record and an access review checklist. List the privacy policy and customer or partner agreement sections that describe hosting and security so I can update them.
```

Phase 4 exit criteria: rebuild test passed; full path: evidence pack complete. Check with `python3 scripts/check_gates.py --infra ./infra --phase 4`.
