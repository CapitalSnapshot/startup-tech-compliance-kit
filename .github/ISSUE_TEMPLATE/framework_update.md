---
name: Framework, law or guidance update
about: A law, standard, criteria set, regulator guidance or tool that the kit relies on has changed
title: "[update] "
labels: framework-update
---

**Review label:** a proposal starts as a **community draft** (see `docs/review-labels.md`). Passing CI or maintainer approval does not imply legal or specialist approval.

**Source** (see `docs/maintenance/source-watch-list.md`):

**Old edition (as mapped now):**

**New edition, amendment or notice, with date and an authoritative link:**

**What changed, in your own words, with the article, clause or criterion:**

## Impact analysis checklist

- [ ] Ran `python3 scripts/source_impact.py list --framework "<name>"` and attached the output
- [ ] Reviewed every listed mapping record against the changed text (edition, references, rationale, covered and excluded, coverage status)
- [ ] Records that changed are back to **community draft** with null reviewer fields (no reviewer, date or decision invented)
- [ ] Updated the documents the impact list names
- [ ] Updated the watch list entry (`edition_mapped`, `last_checked`, `checked_what`)
- [ ] Set `data_date` in `controls/mappings.json`
- [ ] Ran the generators and tests (`validate_mappings.py --build`, `coverage_reports.py --build`, `source_impact.py build`, the test suite)
- [ ] Added a changelog entry naming the source and both editions
- [ ] Release notes will name the source and edition and list any mappings left stale, unreviewed or incomplete (`python3 scripts/source_impact.py release-notes`)

**If nobody can review before the next release:** flag the affected records `needs expert review` with "The source changed on <date> and this record has not been reviewed since" in their limitations, and say so in the release notes.
