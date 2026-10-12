# Data inventory

<!-- kit-evidence: control=08 date=YYYY-MM-DD result=pass type=operational -->

**Review label: community draft.** Proposed guidance. It has not been reviewed by a maintainer or by a specialist, and it is decision support, not legal advice. **Get specialist advice** before you rely on it ([review labels](../docs/review-labels.md)).

Map personal data from collection to deletion. One row per data set. Review at least yearly and whenever you add a feature, a vendor or a data source.

**Completed by:** <role> **Date:** <YYYY-MM-DD>

| Data set | Whose data | Fields (categories) | Special category? | Source (how collected) | Where stored (system, region) | Who can access (roles) | Shared with (processors, others) | Leaves EEA? | Retention | Deletion method |
|---|---|---|---|---|---|---|---|---|---|---|
| <e.g. user accounts> | <customers' users> | <name, email, password hash> | No | <sign-up form> | <primary database, region> | <engineering on-call, support lead> | <email provider> | <Yes: email provider, USA> | <account life + 30 days> | <delete job + backup expiry> |

## Checks

- [ ] Every system in your architecture appears in "Where stored", including logs, analytics, support tools, backups and AI services.
- [ ] Every vendor in "Shared with" is in the vendor register.
- [ ] Every "Leaves EEA? Yes" row has an entry in [`international-transfers.md`](international-transfers.md).
- [ ] Every row has a retention period and a way to delete.
