# Maintenance

**Status:** actively maintained by CapitalSnapshot, on a best-effort basis. There is **no support commitment or service level agreement**. Use of the kit is at your own risk under the Apache License 2.0.

**Contact:** compliance@capitalsnapshot.com is the role mailbox, not a person, and the point of contact for source updates and offers to review the material.

## How to judge whether it is still maintained

- The date and version at the top of [`CHANGELOG.md`](CHANGELOG.md).
- The "data as of" date and the status counts in the [coverage reports](docs/coverage/README.md), and the "last checked" dates in the [source watch list](docs/maintenance/source-watch-list.md). If a source was last checked more than a year ago, check it yourself.
- Open and recently closed issues and pull requests.

## What we do

- Watch the sources the kit relies on, on the cadence in the [source watch list](docs/maintenance/source-watch-list.md), and act on a change by the process below.
- Re-run the verify commands against a real account when a provider CLI changes, and update their status lines.
- Keep the tests and CI green on supported Python versions.
- Respond to reports as time allows; security reports first ([`SECURITY.md`](SECURITY.md)).

## What we do not do

- Give legal, audit or compliance advice, or review your programme.
- Guarantee the guidance is current for every country, sector or provider.

## When a law, standard, criteria set or guidance changes

Stale mappings are the main risk of a compliance kit: the repository keeps looking authoritative after the source has moved. This process traces a change from the source to a reviewed release. One person can hold several roles; if so, someone else should still check the work.

| Role | Does |
|---|---|
| **Source watcher** | Checks each source on its cadence, or acts on a report, and records what was checked |
| **Impact analyst** | Finds everything the change touches and updates it |
| **Reviewer** (not the author) | Checks the updated records and wording against the changed source |
| **Release manager** | Names the change in the release notes and runs the release checklist |

**Steps**

1. **Notice.** The source watcher checks a source on its cadence, or hears of a change (an issue, a notice from the publisher). They update `last_checked` and `checked_what` in [`docs/maintenance/sources.json`](docs/maintenance/sources.json), saying what was really looked at, not just that a page loaded.
2. **Open an impact issue** from the **Framework, law or guidance update** template. Name the source, the old and the new edition, and the date.
3. **Find what is affected:** `python3 scripts/source_impact.py list --framework "<name>" [--edition "<text>"]`. It lists every mapping record, the control files that carry them, and the documents that rely on the source.
4. **Review each affected mapping record** in [`controls/mappings.json`](controls/mappings.json). Read the changed text. Update the edition, references, rationale, what is covered and excluded, and the coverage status. **A changed record goes back to community draft, with null reviewer fields, until a real review happens.** Never record a reviewer, date or decision that did not happen ([`docs/review-labels.md`](docs/review-labels.md)). Set `data_date` to the day you changed a record.
5. **Update the documents** the impact list names, and the watch list entry: new `edition_mapped`, new `last_checked`.
6. **Regenerate and test:** `python3 scripts/validate_mappings.py --build`, `python3 scripts/coverage_reports.py --build`, `python3 scripts/source_impact.py build`, then the test suite. CI fails if a generated page is stale, or if the mappings use an edition the watch list does not name.
7. **Update the changelog.** Name the source and the editions (old and new).
8. **Prepare the release notes:** `python3 scripts/source_impact.py release-notes`. It shows which sources are current, stale or never checked, and how many mappings are still unreviewed or unresolved. Complete the two lines at its end.
9. **Release** with the checklist in [`RELEASE.md`](RELEASE.md).

A worked example, with a fictional edition change, is in [`docs/maintenance/worked-example.md`](docs/maintenance/worked-example.md).

**If nobody can review in time.** Do not let old text look current. For each affected record: set `coverage_status` to `needs expert review`, begin `limitations` with "The source changed on <date> and this record has not been reviewed since", keep the label as community draft, say so in the release notes, and open the impact issue anyway. A mapping flagged as unreviewed is better than one that looks current.

**If no maintainer is available at all.** The changelog, the "data as of" date in the coverage reports and the "last checked" dates in the watch list tell readers how old the content is. The licence lets you fork the kit.

## If it stops being maintained

The changelog will say if maintenance has ended.
