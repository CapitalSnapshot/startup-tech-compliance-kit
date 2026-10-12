# D1. Scratch restore and timing

Run in: a coding agent. Phase 2, step 1. This briefly puts production data in a scratch database, so delete it afterwards and record the deletion. Follow the variant note for your database family.

```text
Phase 2, step 1. Create a scratch managed database in the non-production profile. Stream a full production dump straight into it without writing it to my laptop's disk, and time each stage: dump, transfer, restore, post-restore checks (row counts per table and checksums on key tables against the source). Write the timings and the size of the data to infra/evidence/restore-timing.md, then state an estimated production restore time and a proposed maintenance window with a margin. Run the full smoke suite against the scratch database from the dev host. Write every SQL mode, charset, collation, extension or syntax issue to infra/inventory/phase2/compat-findings.md. Fix findings in the application code, not by relaxing database strictness. Then delete the scratch instance and its snapshots and record the deletion with a timestamp in infra/inventory/phase2/scratch-destroyed.md. Do not continue until that file exists. If the proposed window is longer than I can accept, propose a lower-downtime option (such as logical replication) and stop for my decision.
```

Next: [D2. Storage, recovery test and demo](D2-storage-and-demo.md)
