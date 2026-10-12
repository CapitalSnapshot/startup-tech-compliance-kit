# Versioning

The kit uses [semantic versioning](https://semver.org/) adapted for guidance and tools. The current version is in [`VERSION`](VERSION); changes are in [`CHANGELOG.md`](CHANGELOG.md).

| Change | Version bump | Examples |
|---|---|---|
| **Major** (X.0.0) | Something users build on changes meaning | A control ID is renamed or removed; the evidence header (`kit-evidence`) format changes; a register template's columns change; a control's "done when" is made stricter so a previously passing setup now fails |
| **Minor** (0.X.0) | Additions that do not break existing use | A new control, template, runbook, verify command or provider file; a new optional audit flag or evidence type; refreshed framework mappings with new references |
| **Patch** (0.0.X) | Fixes and clarifications | Typos; corrected guidance; a bug fix in a script; a corrected command; a mapping fixed against its source |

Rules:

- **Control IDs are stable** (`KIT-BKP-01` and so on). They are never reused for a different control. A retired control is marked retired in the changelog and keeps its ID.
- **Evidence numbers** (`control=05`) follow the same rule.
- **Framework mappings** are data ([`controls/mappings.json`](controls/mappings.json)): each record has its edition, source reference, coverage status and a review block. Re-checking a mapping, or changing the edition it is mapped to, is logged in the changelog even if nothing else changes.
- **Guidance corrections that affect safety or legal accuracy** are released as a patch as soon as they are verified, and named in the changelog.
- **A release that changes compliance content names its sources.** Its changelog entry and release notes must name each source and edition affected (old and new), and list any mappings it leaves stale, unreviewed or incomplete. `python3 scripts/source_impact.py release-notes` produces the lists. The process is in [`MAINTENANCE.md`](MAINTENANCE.md).
- **A change of framework edition** is at least a minor release. It is a major release if it changes the meaning of a control ID, the mapping schema or the evidence header.
- Before 1.0.0 (now), minor versions may change things; the changelog will say so plainly.
- Each release is a Git tag (`vX.Y.Z`) and a changelog entry, and passes the checks in [`RELEASE.md`](RELEASE.md).

To pin the kit in your own repository, record the tag you copied from.
