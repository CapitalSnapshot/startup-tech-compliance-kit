# Specialist reviews

**Current position: no specialist review has been recorded.** Every mapping record and every compliance document in this kit is a community draft. This page is where a real review will be published, with its scope, date, reviewer role and exclusions.

> A specialist review is a qualified person's judgement of named material at a point in time. It is not a guarantee of compliance, a certification or legal advice for any organisation. Read [`../review-labels.md`](../review-labels.md) for what each label means.

## The rule

**Only the material named in a published review scope becomes "specialist reviewed". Nothing else changes.** A record or document that is not named keeps its label. A reviewer who looked at the whole kit but signed off a narrower scope has reviewed the narrower scope only.

## What is published for each review

| Item | Where |
|---|---|
| The scope: records, documents, source editions, exclusions | A scope file in [`scopes/`](scopes/), checked by `scripts/review_scope.py` |
| Date and reviewer role | The completed scope file and the review record |
| The decision for each record and document, with a rationale | The completed scope file |
| What the review did not cover | The exclusions and the limitations in the scope file |
| The review record | A copy of [`review-record-template.md`](review-record-template.md), filled in |

The reviewer is named by **role** (for example "privacy professional, CIPP/E holder" or "independent assessor with a current accreditation"), not by name, unless the reviewer asks to be named.

## Proposed scopes

These four scopes are proposals only. Each lists every record of its framework and the documents that carry the kit's guidance for it. A reviewer can narrow a scope before starting. They have no reviewer and no date, and `scripts/review_scope.py check` rejects a proposed scope that has either.

| Scope file | Subject |
|---|---|
| [`scopes/gdpr-privacy.json`](scopes/gdpr-privacy.json) | GDPR and privacy content |
| [`scopes/iso27001.json`](scopes/iso27001.json) | ISO/IEC 27001:2022 mappings |
| [`scopes/soc2.json`](scopes/soc2.json) | SOC 2 mappings |
| [`scopes/dora.json`](scopes/dora.json) | DORA module |

## Commands

```text
python3 scripts/review_scope.py list    docs/specialist-reviews/scopes/dora.json     # what the scope covers
python3 scripts/review_scope.py check   --all                                          # every scope file is valid
python3 scripts/review_scope.py preview docs/specialist-reviews/scopes/<completed>.json   # what would change; writes nothing
```

## Offering a review

See "Offering a specialist review" in [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md). After a review is complete, the maintainers follow [`update-procedure.md`](update-procedure.md).
