# Retention and deletion

<!-- kit-evidence: control=08 date=YYYY-MM-DD result=pass type=operational -->

**Review label: community draft.** Proposed guidance. It has not been reviewed by a maintainer or by a specialist, and it is decision support, not legal advice. **Get specialist advice** before you rely on it ([review labels](../docs/review-labels.md)).

Keep personal data no longer than the purpose needs. Write the period, build the deletion, and test it.

| Data set | Retention period | Trigger (when the clock starts) | Why that long | Deletion method | Backups | Vendors holding a copy | Last tested |
|---|---|---|---|---|---|---|---|
| <e.g. account data> | <account life + 30 days> | <account closure> | <contract, tax, security> | <scheduled job, hard delete> | <expires after 35 days> | <email provider: delete via API> | <YYYY-MM-DD> |

## Rules

- A retention period of "forever" or "until needed" is not a period.
- Deletion covers backups (let them expire, and say how long that takes), logs, search indexes, analytics, support tools and vendors.
- Where law requires you to keep something (for example tax records), keep only that, and say which law.
- Test deletion end to end at least yearly, and time it. The result goes in the evidence for control 08.
