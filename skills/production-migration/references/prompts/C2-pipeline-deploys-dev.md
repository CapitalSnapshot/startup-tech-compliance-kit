# C2. Pipeline, deploys and dev environment

Run in: a coding agent. Phase 1, step 2.

```text
Phase 1, step 2. Write: <CI SYSTEM> workflows that build, test, scan for secrets and push images to the container registry on every push, and that promote a tag to an environment using environment-scoped secrets; a pull-based deploy on each host (a timer resolves the tag's image digest, starts a candidate stack, runs the smoke checks, switches traffic, and reverts to the previous digest on failure); a provisioning script that creates a host, static IP, firewall and tags for an environment, enforces instance size limits, and refuses to run against production unless I pass an explicit flag; and a smoke suite covering the items on <VERIFICATION LIST>, an email send in sandbox mode and a health check. Build the dev environment from the script, not by hand, and record the run in infra/evidence/dev-build.md.
```

Phase 1 exit criteria: dev rebuilt from the pipeline, not by hand; smoke suite green. Check with `python3 scripts/check_gates.py --infra ./infra --phase 1`.

Next: [D1. Scratch restore and timing](D1-scratch-restore.md)
