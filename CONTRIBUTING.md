# Contributing

Thank you. You do not need a large change: a corrected sentence with a source is a real contribution. Please read [`SECURITY.md`](SECURITY.md) first if you have found a vulnerability, and [`MAINTENANCE.md`](MAINTENANCE.md) for what to expect.

## The rules that matter most

1. **Keep it generic.** No real hostnames, IP addresses, cloud account IDs, bucket or secret names, people's names, customer details or credentials. Examples are invented ("Example Co"). The scan (`scripts/sanitise_check.py`) fails a pull request that contains a pattern from the maintainers' private denylist or the built-in patterns, or that commits compiled files, key files or environment files.
2. **Cite a source for guidance.** Compliance content improves through verifiable contributions. For a legal, standard or provider claim, name the authoritative source and its edition or date.
3. **Say how you would prove it.** Every control names the evidence that shows it works, and its limits.
4. **Honest status.** Mark any command you did not run `UNTESTED`.
5. By contributing you agree your contribution is licensed under the Apache License, Version 2.0.

## Review labels: what your contribution is called

Everything you propose starts as a **community draft**: proposed, with form and basic checks passed, but not substantively verified. Two stronger labels exist, **maintainer reviewed** and **specialist reviewed**, and they are granted only after that review has actually happened and is recorded. **Passing CI, or a maintainer approving your pull request, does not imply legal or specialist approval.** The full definitions, who can grant each label, and the six coverage statuses (covered, covered in part, not covered, not applicable, not assessed, needs expert review) are in [`docs/review-labels.md`](docs/review-labels.md). Please do not describe your contribution as reviewed or verified unless it has been.

## Ways to help

| You want to... | Do this |
|---|---|
| Report a documentation error | Open a **Documentation correction** issue with the source. Or send a pull request that fixes it |
| Propose a new control | Open a **New control proposal** issue first. Follow the shape in [`controls/README.md`](controls/README.md): objective, applicability, owner, review frequency, limitations, done-when, evidence kinds, references, how to verify |
| Add cloud verification commands | Add or edit a file in [`verify/`](verify/). Copy [`verify/_template.md`](verify/_template.md) for a new provider. Read-only only; a status line on every command. EU-native and regional providers are very welcome |
| Improve framework mappings | Edit [`controls/mappings.json`](controls/mappings.json), **not** the Markdown page, which is generated from it. Each record needs the framework and edition, the exact source reference and URL, the rationale, what it covers and excludes, a coverage status and a review block ([`controls/mapping.schema.json`](controls/mapping.schema.json)). Set `data_date` in the file to the day you changed a record. Then run `python3 scripts/validate_mappings.py --build` and `python3 scripts/coverage_reports.py --build` and commit the changed files. New records are community drafts with null reviewer fields. See [`docs/review-labels.md`](docs/review-labels.md) |
| Contribute tests | Add to `audit/tests/`. Negative cases (missing, stale, malformed, unreadable) are especially valuable |
| Review the privacy guidance | If you are a privacy professional, review [`privacy/`](privacy/) and open issues or pull requests with sources. For a formal review that can earn the specialist reviewed label, see "Offering a specialist review" below |

## Offering a specialist review

If you are a qualified practitioner (for example a privacy professional for GDPR content, or an assessor for SOC 2, ISO/IEC 27001 or DORA content), you can review part of the kit and have it recorded. Nothing is awarded by default and nobody is asked to review more than they choose.

1. **Pick a scope.** The proposed scopes are in [`docs/specialist-reviews/scopes/`](docs/specialist-reviews/scopes/): GDPR and privacy, ISO/IEC 27001, SOC 2 and DORA. Run `python3 scripts/review_scope.py list <scope file>` to see the records and documents each covers. You may narrow a scope. You may not widen it after you start without saying so.
2. **Open an issue** offering the review. Say the scope, your role and qualification (a name only if you agree to it), any link to the kit's authors or maintainers, and the source editions you will use. For ISO and AICPA material, say whether you hold a licensed copy. The kit cites identifiers only and must not contain standard or criteria text, so please do not paste it.
3. **Return a decision for each item.** Use [`docs/specialist-reviews/review-record-template.md`](docs/specialist-reviews/review-record-template.md): a decision per record and document, a rationale citing the article, clause or criterion, the limitations, the date and your role.
4. **What happens next.** A maintainer checks the scope file, then updates the labels by hand following [`docs/specialist-reviews/update-procedure.md`](docs/specialist-reviews/update-procedure.md). Only the material named in the scope becomes specialist reviewed. Nothing else changes, and a partial review is recorded as partial.

A review is a qualified person's judgement of named material at a point in time. It is not a guarantee that anyone complies, and the kit does not state otherwise. Maintainers do not award specialist reviewed to themselves.

## Working on the code

- Python 3.9 or later, standard library only. No dependencies, please.
- Run the tests: `python3 -I -m unittest discover -s audit/tests -p "test_*.py"`.
- If you change a control file, regenerate the index: `python3 scripts/controls_index.py`. A test fails if `controls/controls.json` is out of date.
- If you change a mapping, edit `controls/mappings.json` and regenerate the page: `python3 scripts/validate_mappings.py --build`. CI fails on missing metadata, an invalid status, or a page or coverage report that differs from a fresh build.
- Run the scan: `python3 scripts/sanitise_check.py .`.
- Do not commit compiled files, editor files, key files or environment files. `.gitignore` covers them.
- Update [`CHANGELOG.md`](CHANGELOG.md) if users would notice, and follow [`VERSIONING.md`](VERSIONING.md).

## Pull requests

Describe what changed and why, tick the checklist in the template, and keep the change focused. A maintainer will review it as time allows.
