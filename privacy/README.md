# Privacy operating process (GDPR)

> **Standing notice.** This is repository based, community maintained guidance. It is not legal advice, a formal compliance assessment, a certification or an independent security audit. Mappings and statements about frameworks are unverified unless their review label says otherwise ([review labels](../docs/review-labels.md)).

A connected process, not a list of documents. It is for teams whose processing may fall within the GDPR's territorial scope (Article 3). Being established in the Union is one route; offering goods or services to, or monitoring the behaviour of, people in the Union without being established there is another. Decide which applies with [`../scoping/gdpr-territorial-scope.md`](../scoping/gdpr-territorial-scope.md); the location of the people is not the only test.

> **Get specialist advice.** This folder is a practical starting point written by engineers, **not legal advice**, and it has **not been reviewed by a privacy specialist**. Lawful bases, transfer mechanisms, breach notification, DPIA and DPO decisions, and your obligations depend on your facts. Have a privacy or data-protection professional review your approach before you rely on it. [`accountability.md`](accountability.md) lists when to ask.

```
 collect --> record --> decide basis --> store (retention) --> share (processors, transfers)
    |           |             |                  |                        |
    |      data inventory  lawful basis     deletion schedule        Art. 28 agreements
    |                                                                  transfer assessment
    v
 privacy by design review (new features)  -->  DPIA screening (high risk?)
                                                      |
 people exercise rights ------------------> data subject request process
 something goes wrong --------------------> breach assessment and notification decision
```

| Step | Template | Control it supports |
|---|---|---|
| 1. Map the data | [`data-inventory.md`](data-inventory.md) | [08](../controls/08-data-protection.md) |
| 2. Record purposes, lawful basis, retention | [`record-of-processing.md`](record-of-processing.md) | 08 |
| 3. Retention and deletion | [`retention-and-deletion.md`](retention-and-deletion.md) | 08 |
| 4. Answer rights requests | [`data-subject-requests.md`](data-subject-requests.md) | 08 |
| 5. Transfers outside the EEA | [`international-transfers.md`](international-transfers.md) | 08, 07 |
| 6. Processors (Art. 28) | [`../evidence/vendor-register.md`](../evidence/vendor-register.md) | 07 |
| 7. New features | [`privacy-by-design-review.md`](privacy-by-design-review.md) | 08, 03 |
| 8. High-risk processing (preliminary screening, not a legal threshold) | [`dpia-screening.md`](dpia-screening.md) | 08 |
| 9. Breaches | [`../runbooks/incident-response.md`](../runbooks/incident-response.md), [`../evidence/incident-register.md`](../evidence/incident-register.md) | 09 |
| 10. Accountability and advice | [`accountability.md`](accountability.md), [`dpo-screening.md`](dpo-screening.md) | 12 |

## Points that are easy to get wrong

- **Breach duties depend on your role.** A **controller** must notify the supervisory authority without undue delay and, where feasible, within **72 hours of becoming aware** (Art. 33(1)), unless the breach is unlikely to result in a risk to people's rights and freedoms, and must tell the people affected without undue delay if it is likely to result in a high risk (Art. 34). A **processor** must notify the controller without undue delay after becoming aware (Art. 33(2)); the 72-hour period is not the processor's. A customer contract may set a different, **contractual** deadline. Controllers must **document every breach**, notified or not (Art. 33(5)). Use the role-based walkthrough in [`../runbooks/incident-response.md`](../runbooks/incident-response.md).
- **A Data Protection Officer is not required of every startup.** It depends on the conditions in Art. 37. See [`dpo-screening.md`](dpo-screening.md).
- **A privacy notice and a processor agreement are two parts of a bigger set.** They do not replace lawful bases, retention rules or rights handling.
- **A record of processing (Art. 30)** has an exemption for organisations employing fewer than 250 persons (Art. 30(5)), but it is conditional and it lifts **only that record-keeping duty, not the GDPR**. It is lost if the processing is likely to result in a risk to people's rights and freedoms, is not occasional, or includes special categories or criminal convictions data. Ongoing processing of customer or employee data is often "not occasional", so check that condition carefully. Record your decision in the applicability record at the top of [`record-of-processing.md`](record-of-processing.md); if unsure, keep the record.
