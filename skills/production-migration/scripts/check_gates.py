#!/usr/bin/env python3
"""Check that the evidence files a migration phase must produce exist and are not empty.

This checks presence only. It cannot judge whether the evidence is correct:
read the files before you advance to the next phase.

Usage:
    python3 check_gates.py --infra ./infra --phase 0
    python3 check_gates.py --infra ./infra --phase 2 --no-demo
    python3 check_gates.py --infra ./infra --phase 4 --lean

Exit status is 0 when every required item is present, 1 otherwise.
Keep PHASES in step with docs/evidence-files.md.
"""

import argparse
import sys
from pathlib import Path

# Each entry: (path relative to the infra folder, tag). A tag of "demo" marks
# files skipped with --no-demo or --lean; "pack" marks a directory skipped with --lean.
PHASES = {
    0: [
        ("evidence/snapshot.md", None),
        ("inventory/host-inventory.md", None),
        ("inventory/cloud-resources.md", None),
        ("inventory/external-systems.md", None),
        ("inventory/differences-from-plan.md", None),
        ("inventory/db-compat.md", None),
        ("evidence/identities.md", None),
        ("evidence/logging.md", None),
        ("evidence/deny-proof.md", None),
        ("evidence/db-connectivity.md", None),
    ],
    1: [
        ("evidence/dev-build.md", None),
    ],
    2: [
        ("inventory/phase2/compat-findings.md", None),
        ("inventory/phase2/scratch-destroyed.md", None),
        ("evidence/restore-timing.md", None),
        ("evidence/restore-test.md", None),
        ("evidence/file-sync-test.md", None),
        ("evidence/demo-promotions.md", "demo"),
    ],
    3: [
        ("evidence/rehearsal.md", None),
        ("evidence/prod-build.md", None),
        ("evidence/cutover.md", None),
    ],
    4: [
        ("evidence/decommission.md", None),
        ("RUNBOOK-REBUILD.md", None),
        ("evidence-pack/", "pack"),
    ],
}


def check(infra: Path, phase: int, skip_demo: bool, lean: bool):
    results = []
    for rel, tag in PHASES[phase]:
        if tag == "demo" and (skip_demo or lean):
            results.append((rel, "SKIPPED", "demo not in scope"))
            continue
        if tag == "pack" and lean:
            results.append((rel, "SKIPPED", "lean path"))
            continue
        path = infra / rel
        if rel.endswith("/"):
            if not path.is_dir():
                results.append((rel, "MISSING", "folder not found"))
            elif not any(p.is_file() and p.stat().st_size > 0 for p in path.rglob("*")):
                results.append((rel, "EMPTY", "folder has no non-empty files"))
            else:
                results.append((rel, "OK", ""))
            continue
        if not path.is_file():
            results.append((rel, "MISSING", "file not found"))
        elif path.stat().st_size == 0:
            results.append((rel, "EMPTY", "file is empty"))
        else:
            results.append((rel, "OK", ""))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--infra", required=True, help="path to the infra folder")
    parser.add_argument("--phase", required=True, type=int, choices=sorted(PHASES), help="phase number 0 to 4")
    parser.add_argument("--no-demo", action="store_true", help="demo environment is out of scope")
    parser.add_argument("--lean", action="store_true", help="lean path (implies --no-demo, skips the evidence pack)")
    args = parser.parse_args()

    infra = Path(args.infra)
    if not infra.is_dir():
        print(f"infra folder not found: {infra}", file=sys.stderr)
        return 2

    results = check(infra, args.phase, args.no_demo, args.lean)
    width = max(len(r[0]) for r in results)
    failed = 0
    for rel, status, note in results:
        if status in ("MISSING", "EMPTY"):
            failed += 1
        print(f"{status:8} {rel:<{width}}  {note}".rstrip())

    if failed:
        print(f"\nPhase {args.phase} gate NOT met: {failed} item(s) missing or empty.")
        return 1
    print(f"\nPhase {args.phase} gate files present. Read them before you advance: this checks presence, not correctness.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
