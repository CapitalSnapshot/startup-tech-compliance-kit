# Release checklist

A release is a tag (`vX.Y.Z`), a changelog entry, and a pass of every item below. Do not announce a release that has not passed.

## Gate

- [ ] **Clean-environment tests pass.** A fresh clone, with nothing installed beyond Python: `python3 -I -m unittest discover -s audit/tests -p "test_*.py"`. Run on every supported version (3.9 to 3.13); CI does this on every pull request.
- [ ] **Supported versions documented** in the README and matched by CI.
- [ ] **Negative cases pass.** Missing evidence, stale evidence, malformed headers, unreadable files, malformed register rows, a risk accepted by its own owner, a missing `gh`, a permission error, a missing folder. The tests in `audit/tests/test_audit.py` cover these; do not remove them.
- [ ] **Cloud commands status is honest.** Every command in `verify/` has a status line. Anything not run is `UNTESTED`. New `TESTED` lines name the date and were run read-only.
- [ ] **No credentials, tokens, personal data, real identifiers or compiled files.** `python3 scripts/sanitise_check.py .` with the maintainers' private denylist, and `git ls-files` shows no binaries.
- [ ] **Generated files are current.** `python3 scripts/controls_index.py --check`, `python3 scripts/validate_mappings.py --check`, `python3 scripts/coverage_reports.py --check` and `python3 scripts/source_impact.py check`.
- [ ] **CI runs on pull requests and is required** on the default branch.
- [ ] **Version, changelog and tag agree:** `VERSION` equals the newest changelog entry.
- [ ] **Sources and editions are named.** If the release changes compliance content, the changelog and release notes name each source and edition affected (old and new), and the output of `python3 scripts/source_impact.py release-notes` is attached, with every mapping left stale, unreviewed or incomplete listed.
- [ ] **Anything unreviewed is labelled** (community draft) and no review is recorded that did not happen.
- [ ] **The README and `privacy/README.md` tell users to get specialist advice**, and say the privacy material has not been reviewed by a specialist (until one has, and the mappings say so).

## After

- Tag, publish release notes from the changelog, and keep the checklist output with the release.
