# 8. Data protection (GDPR)

| | |
|---|---|
| **Control ID** | KIT-PRV-01 |
| **Evidence number** | 08 (the `control=` value in evidence headers) |
| **Applies to** | Processing of personal data that may fall within the GDPR's territorial scope (Article 3; see `scoping/gdpr-territorial-scope.md`), and anywhere else you choose to apply it |
| **Owner (role)** | The accountable privacy contact (a DPO only if one is required) |
| **Review frequency** | Every 365 days or sooner (yearly); the audit flags evidence older than 365 days |
| **Limitations** | The kit's privacy templates are a start, not legal advice or full GDPR compliance: lawful bases, rights handling and transfers need judgement and often a specialist |

**Objective:** You know what personal data you hold, why, where, for how long, and how a person can see it or have it erased.

## What to do

- Map personal data from collection to deletion ([`../privacy/data-inventory.md`](../privacy/data-inventory.md)).
- Write a record of processing with the **lawful basis for each purpose** ([`../privacy/record-of-processing.md`](../privacy/record-of-processing.md)).
- Define retention periods and build and test the deletion ([`../privacy/retention-and-deletion.md`](../privacy/retention-and-deletion.md)).
- Collect the minimum. Do not keep data you have no purpose for.
- Encrypt personal data in transit and at rest. Restrict who can read it.
- Build a way to answer data subject requests (access, correction, erasure, restriction, portability, objection) within one month, and test it ([`../privacy/data-subject-requests.md`](../privacy/data-subject-requests.md)).
- Identify transfers outside the EU or EEA and record the mechanism and assessment ([`../privacy/international-transfers.md`](../privacy/international-transfers.md)).
- Have an Art. 28 agreement with every processor ([`../evidence/vendor-register.md`](../evidence/vendor-register.md)).
- Review new features for privacy before they ship ([`../privacy/privacy-by-design-review.md`](../privacy/privacy-by-design-review.md)).
- Name who is accountable for privacy, and decide whether a DPO is required: most startups do not need one ([`../privacy/dpo-screening.md`](../privacy/dpo-screening.md)).
- Know your breach duty **by role**: a controller notifies the supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware, unless the breach is unlikely to result in a risk; a processor notifies the controller without undue delay, and a customer contract may add its own deadline. Not every breach must be notified, but a controller must document the assessment and the reason either way ([`../runbooks/incident-response.md`](../runbooks/incident-response.md)).
- Screen new processing for the need for a data protection impact assessment, and keep the screening ([`../privacy/dpia-screening.md`](../privacy/dpia-screening.md)).

## Why a reviewer asks

Reviewers ask for the record of processing, how you handle a deletion request, and where personal data goes outside the EU or EEA.

## Done when

- [ ] A current data inventory and record of processing exist, with a lawful basis per purpose.
- [ ] Retention periods are set and a deletion has been tested.
- [ ] A deletion request has been rehearsed end to end, including backups and vendors, with the time it took.
- [ ] A privacy notice states the real purposes, retention and processors.
- [ ] Transfers outside the EU or EEA have a recorded mechanism and assessment.
- [ ] Every processor has an Art. 28 agreement.
- [ ] A person is accountable for privacy, and the DPO question is answered in writing.

## Evidence to keep

- The data inventory and record of processing.
- The rehearsed deletion request with timings.
- The privacy notice.
- Any impact assessment.

### Kinds of evidence

- **Configuration:** Encryption and public-access settings on stores of personal data
- **Operational:** The data inventory, record of processing, retention schedule
- **Effectiveness:** A rehearsed deletion request across systems, backups and vendors, with the time it took
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- A privacy notice that describes what you wish you did.
- Deletion that leaves the data in backups or a vendor with no plan.
- No named person responsible.
- Assuming that hosting in the EU settles transfers made by your vendors.

## Indicative framework references

SOC 2 P-series, C1 · ISO 27001:2022 A.5.34 · GDPR Art. 5, 25, 30, 32, 33, 34, 35 · DORA Art. 9

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

Read-only commands for AWS, Google Cloud and Azure, with a status line on each: [`../verify/`](../verify/) (section 08). Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../evidence/evidence-file.md`](../evidence/evidence-file.md) (record of processing, deletion rehearsal)

## Related

- [`../privacy/README.md`](../privacy/README.md) (the connected operating process)
- [`../evidence/evidence-file.md`](../evidence/evidence-file.md)
