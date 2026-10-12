# D2. Storage, recovery test and demo

Run in: a coding agent. Phase 2, step 2. The demo part applies only if DEMO IN SCOPE is yes (full path).

```text
Phase 2, step 2. Create object storage buckets for each environment in scope (production versioned, private, encrypted) and write scripts/migrate-files.sh that syncs the old system's upload directories to a bucket idempotently, with a manifest and checksum verification; test it against dev with synthetic files and record the result in infra/evidence/file-sync-test.md. Restore a non-production database from a backup into a new instance to prove recovery, record it in infra/evidence/restore-test.md, then delete the restored instance. If DEMO IN SCOPE is yes, also build the demo environment: host, static IP, managed database, bucket, cache if used, hostnames, provisioning script, a curated dataset from the seeder, a scheduled reset, a robots disallow and a visible demo banner; promote the current release candidate from dev to demo through the pipeline twice and record both runs in infra/evidence/demo-promotions.md. Move remaining secrets into the CI system's environment-scoped secrets and delete every env file on the old test host. Commit "Phase 2 complete" with the evidence.
```

Phase 2 exit criteria: restore timed and window estimated; recovery from backup tested; file sync proven; full path: demo live and a release promoted dev to demo twice. Check with `python3 scripts/check_gates.py --infra ./infra --phase 2` (add `--no-demo` if demo is out of scope).

Next: [E0. Cutover rehearsal](E0-rehearsal.md)
