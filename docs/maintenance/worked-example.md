# Worked example: tracing a source change to a release

**This example is fictional.** No such edition exists, no review is recorded, and nothing here is in the real data. It shows how a change moves from the source to a reviewed release, using the real tools. The output blocks are real output from the current repository (the release notes snippet uses the date 2026-10-12).

**The scenario.** The publisher of the SOC 2 criteria announces a (fictional) "2027 Trust Services Criteria" that renames and renumbers some criteria.

## 1. A source change is noticed

The source watcher sees the announcement. They record it in [`sources.json`](sources.json) by updating `last_checked` and `checked_what` for the `soc2-tsc` entry, saying what was actually looked at ("announcement page only; the new criteria document was not read"). They do not change the edition yet.

## 2. Open an impact issue

From the **Framework, law or guidance update** template. Title: `[update] AICPA 2027 Trust Services Criteria (fictional)`. Fill in the old edition (as mapped now), the new edition with an authoritative link and date, and what changed.

## 3. Find what is affected

```text
$ python3 scripts/source_impact.py list --framework "SOC 2"
Sources:
  soc2-tsc: AICPA Trust Services Criteria (edition mapped: 2017 Trust Services Criteria (With Revised Points of Focus - 2022); last checked: 2026-10-09)
Mapping records (12): review each, update its fields and review block:
  KIT-ACC-01.SOC2.1  [CC6.1 to CC6.3]  needs expert review  (community draft)
  KIT-SEC-01.SOC2.1  [CC6.1, CC6.7]  needs expert review  (community draft)
  KIT-CHG-01.SOC2.1  [CC8.1]  needs expert review  (community draft)
  ...
Control files that carry these records:
  controls/01-access-control.md
  ...
Documents that rely on the source:
  guide/paths/soc2.md
```

That is every mapping record (12 here), the control files that carry them, and the documents that rely on the source. Attach the output to the issue.

## 4. Review each affected record

The impact analyst opens each record in [`controls/mappings.json`](../../controls/mappings.json), reads the changed text, and updates the edition, references, rationale, what is covered and excluded, and the coverage status. A changed record goes **back to community draft with null reviewer fields**. The example records no reviewer, because no review happened. They set `data_date` to the day of the change.

## 5. What the checks catch while you work

Suppose the analyst changes the edition on the mapping records but forgets the watch list. The check refuses, and says where the two disagree:

```text
SOC 2: mapping records use edition(s) ['2027 Trust Services Criteria (fictional)'] but the watch list says ['2017 Trust Services Criteria (With Revised Points of Focus - 2022)']
```

They then update the watch list entry (`edition_mapped`, `last_checked`, `checked_what`) so the two agree. (Had they updated the watch list but not the records, the same check fails the other way.)

## 6. Regenerate and test

```text
python3 scripts/validate_mappings.py --build
python3 scripts/coverage_reports.py --build
python3 scripts/source_impact.py build
python3 -I -m unittest discover -s audit/tests -p "test_*.py"
```

CI runs the matching `--check` commands and fails if a generated page is stale.

## 7. The changelog names the source and both editions

> Updated the SOC 2 mappings from the 2017 Trust Services Criteria (With Revised Points of Focus - 2022) to the (fictional) 2027 Trust Services Criteria. Twelve records changed and are community drafts again.

## 8. Release notes

```text
$ python3 scripts/source_impact.py release-notes
## Sources and editions

| Source | Edition mapped | Last checked | Status |
|---|---|---|---|
| AICPA Trust Services Criteria | 2017 Trust Services Criteria (With Revised Points of Focus - 2022) | 2026-10-09 | current |
| ISO/IEC 27001 information security management systems | 2022 | never | never checked |
...
- Community drafts (no maintainer or specialist review recorded): 60 of 60 records.
Sources stale or never checked: ISO/IEC 27001 information security management systems (never checked), Google Cloud CLI (never checked), Microsoft Azure CLI (never checked).
```

The release manager then completes the last two lines of that output: which sources and editions changed (the fictional SOC 2 edition, old and new), and which mappings the release leaves stale, unreviewed or incomplete.

## 9. Release

The release manager runs [`RELEASE.md`](../../RELEASE.md). Because this release changes compliance content, the checklist needs the sources named and the release notes attached.

## If nobody could review in step 4

The twelve records would be set to `needs expert review`, each `limitations` would begin "The source changed on <date> and this record has not been reviewed since", and the release notes would say so. Readers then see that the mappings are unreviewed instead of finding old text that looks current.
