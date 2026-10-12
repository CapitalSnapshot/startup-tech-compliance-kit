# Evidence files per phase

Each phase writes these files under `infra/` in your application repo. `scripts/check_gates.py` verifies they exist and are not empty; it does not judge their content, so read them.

| Phase | Files |
| --- | --- |
| 0 | `infra/evidence/snapshot.md`, `infra/inventory/host-inventory.md`, `infra/inventory/cloud-resources.md`, `infra/inventory/external-systems.md`, `infra/inventory/differences-from-plan.md`, `infra/inventory/db-compat.md`, `infra/evidence/identities.md`, `infra/evidence/logging.md`, `infra/evidence/deny-proof.md`, `infra/evidence/db-connectivity.md` |
| 1 | `infra/evidence/dev-build.md` |
| 2 | `infra/inventory/phase2/compat-findings.md`, `infra/inventory/phase2/scratch-destroyed.md`, `infra/evidence/restore-timing.md`, `infra/evidence/restore-test.md`, `infra/evidence/file-sync-test.md`; demo only: `infra/evidence/demo-promotions.md` |
| 3 | `infra/evidence/rehearsal.md`, `infra/evidence/prod-build.md`, `infra/evidence/cutover.md` |
| 4 | `infra/evidence/decommission.md`, `infra/RUNBOOK-REBUILD.md`; full path: a non-empty `infra/evidence-pack/` |

Usage:

```text
python3 scripts/check_gates.py --infra ./infra --phase 0
python3 scripts/check_gates.py --infra ./infra --phase 2 --no-demo
python3 scripts/check_gates.py --infra ./infra --phase 4 --lean
```

`--no-demo` skips the demo file. `--lean` implies `--no-demo` and also skips the evidence pack.
