# Updating review metadata after a real review

Follow this only when a qualified reviewer has actually completed a review and returned the deliverable. **Nothing here is automated, on purpose.** The script lists and previews; a person makes each edit.

## Before you start

1. The reviewer's role is not a maintainer or an author of the content (`docs/review-labels.md`: maintainers do not award specialist reviewed to themselves).
2. You have, from the reviewer: a decision for each record and document in the scope, a rationale for each, the limitations, the reviewer's role and the review date.
3. The scope file named by the reviewer matches the material they actually reviewed. If they narrowed it, narrow the file first.

## Steps

1. **Complete the scope file.** Copy the proposed scope to a new file or edit it: set `status` to `completed`, fill `reviewer_role`, `review_date` and `limitations`, and add one entry under `decisions` for every record id and document path. Each entry has a `decision` (`accepted`, `accepted with changes`, `not accepted` or `not reviewed`) and a `rationale`. Optionally add `coverage_status` if the reviewer changed it.
2. **Check it.** `python3 scripts/review_scope.py check <file>`. It fails on a missing decision, a missing role, date or limitations, a future date, a reviewer role that names a maintainer or an author, and an item outside the scope.
3. **Preview.** `python3 scripts/review_scope.py preview <file>` prints the review block each record would receive and the label line each document would carry. Only `accepted` and `accepted with changes` raise a label. `not accepted` and `not reviewed` change nothing.
4. **Edit the records.** In `controls/mappings.json`, for each granted record set `review.label` to `specialist reviewed`, and set `reviewer_role`, `review_date`, `decision` and `rationale` from the scope file. Set `coverage_status` only as the reviewer decided; `covered` is allowed on a specialist reviewed record and nowhere else. Update `limitations` if the reviewer changed them. Set `next_review_trigger` from the review record. Update `data_date`.
5. **Edit the documents.** For each granted document, change its `**Review label: ...**` line to `specialist reviewed`, name the scope id and the date, and add the review record link. If a document has no label line, add one first and make the change in a separate commit.
6. **Regenerate and validate.** `python3 scripts/validate_mappings.py --build`, then `python3 scripts/coverage_reports.py --build`, then `python3 scripts/validate_mappings.py --check` and `python3 scripts/coverage_reports.py --check`. Run the full test suite.
7. **Publish the review record.** Add the filled-in [`review-record-template.md`](review-record-template.md) and the completed scope file to this directory, and list them in [`README.md`](README.md).
8. **Add a CHANGELOG entry** that names the scope, the date and the reviewer role, and says which items were accepted and which were not.

## Things that must not happen

- Do not raise the label of anything the scope does not name.
- Do not record a reviewer, a date or a decision that was not given.
- Do not change a record's wording to match the review without resetting its label: a material change to reviewed content resets it to community draft until it is reviewed again. If the reviewer required changes, make them, send the changed text back for confirmation, and record the confirmation as the decision `accepted with changes`.
- Do not describe a specialist reviewed record as proof that anyone meets a requirement.
