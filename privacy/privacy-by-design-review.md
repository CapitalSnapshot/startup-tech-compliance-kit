# Privacy by design review

**Review label: community draft.** Proposed guidance. It has not been reviewed by a maintainer or by a specialist, and it is decision support, not legal advice. **Get specialist advice** before you rely on it ([review labels](../docs/review-labels.md)).

Run this for every new feature, data source, vendor or change in how data is used, before it ships. It takes ten minutes for most changes. Attach the answers to the pull request or ticket.

<!-- kit-evidence: control=08 date=YYYY-MM-DD result=pass type=operational -->

**Feature / change:** <...> **Reviewer:** <role> **Date:** <YYYY-MM-DD>

| Question | Answer |
|---|---|
| What personal data does it collect or use that we did not before? | <...> |
| Is each field necessary for the purpose? Can we do it with less, pseudonymised or aggregated? | <...> |
| What is the lawful basis, and is it in the record of processing? | <...> |
| Does a new vendor, sub-processor or country come into play? (vendor register, transfers) | <...> |
| How long is it kept, and how is it deleted? | <...> |
| Who can access it, and is that the minimum? | <...> |
| Is it on by default only for what is needed? Are privacy-protective defaults used? | <...> |
| Can we answer an access, correction and deletion request for it? | <...> |
| What was the DPIA screening outcome, and when was it decided? ([`dpia-screening.md`](dpia-screening.md); a preliminary screening, not a legal threshold) | <outcome and date> |

**Outcome:** Approve / Approve with changes / Do not ship until assessed. Changes: <...>
