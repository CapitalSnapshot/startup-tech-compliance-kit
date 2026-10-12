## What does this change?

<!-- One or two sentences. Link the issue if there is one. -->

## Type

- [ ] Documentation correction (cite the authoritative source below)
- [ ] New or changed control, template or runbook
- [ ] Verify commands (state which provider, and whether you ran them)
- [ ] Framework mapping (state the edition and the reference)
- [ ] Script or test
- [ ] Other

## Review label

This change is a **community draft** by default (see [`docs/review-labels.md`](../docs/review-labels.md)). **Passing CI or a maintainer's approval does not imply legal or specialist approval.** Do not claim a stronger label unless a recorded review has happened.

## Checklist

- [ ] No real hostnames, IP addresses, account IDs, names, credentials or customer data (examples are invented).
- [ ] Commands are read-only and print no secret values.
- [ ] Any command I did not run is marked `UNTESTED`.
- [ ] Tests pass: `python3 -I -m unittest discover -s audit/tests -p "test_*.py"`.
- [ ] I updated `CHANGELOG.md` if users would notice, ran `python3 scripts/controls_index.py` if I changed a control, and ran `python3 scripts/validate_mappings.py --build` and `python3 scripts/coverage_reports.py --build` if I changed a mapping (edit `controls/mappings.json`, not the generated pages).

## Source

<!-- For guidance or mapping changes: the authoritative source (law, standard, provider documentation) and the edition. -->
