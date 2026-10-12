# E0. Cutover rehearsal

Run in: a coding agent, with you present. Phase 3, before the real cutover. Non-production profile only; nothing here touches production or DNS.

```text
Phase 3, rehearsal. Using the non-production profile and the E2 cutover steps as the script, rehearse the cutover end to end against the demo environment (or a clone of dev if there is no demo): enable maintenance mode, dump and restore a copy of the data, run the delta file sync, run the smoke suite against everything on <VERIFICATION LIST>, practise the rollback steps, and use a hosts-file override in place of DNS. Time every step. Write the steps, timings, anything that failed and what you changed to infra/evidence/rehearsal.md, and update the proposed maintenance window from the Phase 2 restore timing. Do not continue to the real cutover until a rehearsal has completed without manual workarounds.
```

Next: [E1. The day before cutover](E1-day-before.md)
