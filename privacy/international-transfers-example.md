# International transfers: filled-in example

Review label: community draft ([`../docs/review-labels.md`](../docs/review-labels.md)). **Fictional.** Every party, country and fact below is invented to show how the record in [`international-transfers.md`](international-transfers.md) is filled in. It says nothing about any real vendor or country, and its conclusions must not be copied.

## Register

| ID | Recipient | Country | What data | Route | Assessment record | Approved by | Reassess by |
|---|---|---|---|---|---|---|---|
| T-01 | Example Metrics Inc. | Examplestan (fictional, no adequacy decision) | Product usage events with user ID | Appropriate safeguards (Art. 46(2)(c)), Module Two | below | Head of Engineering | 2027-03-01 |

## Assessment record

**1. Transfer ID and purpose:** T-01. Example Metrics Inc. runs our product analytics dashboard. We send usage events so our team can see which features are used.

**2. Parties and roles**

| | Name | Role | Country | Subject to the GDPR for this processing? |
|---|---|---|---|---|
| Exporter | Sample Software Ltd | Controller | A Member State (fictional establishment) | Yes |
| Importer | Example Metrics Inc. | Processor | Examplestan | No: it has no establishment in the Union and does not itself offer goods or services to, or monitor, people in the Union (checked 2026-02-10, see sources) |

**3. The data:** pseudonymous user ID, event name, timestamp, browser type; about 40,000 people, continuous; no special categories (Art. 9) and no criminal convictions data (Art. 10).

**4. Route**

| Route | Basis | Chosen? | Details |
|---|---|---|---|
| Adequacy decision | Art. 45(3) | No | Examplestan is not on the Commission's published list of adequate countries, territories and sectors (Art. 45(8)); checked 2026-02-10 |
| Appropriate safeguards | Art. 46(2)(c) | **Yes** | Commission standard clauses, Decision (EU) 2021/914, **Module Two** (controller to processor). Signed 2026-02-20 by both parties. Clause 7 (docking) not used; the sub-processor option is general written authorisation (Clause 9, Option 2) with 30 days' notice; Annexes I to III completed |
| Derogation | Art. 49(1) | No | Not needed: a safeguard is available |
| Art. 46(3) contract clauses | | No | Not used |

**Why this route:** there is no adequacy decision for Examplestan, so we need appropriate safeguards. The importer is a processor not subject to the GDPR, which is the situation the Commission clauses are for (Decision (EU) 2021/914, Art. 1(1)); Module Two fits because we are the controller and it processes on our instructions. Derogations are for specific situations and are not available while a safeguard is.

**5. Assessment of the destination**

| Element | Finding | Source |
|---|---|---|
| Circumstances of the transfer | One importer, no onward transfers except the two sub-processors in S7; continuous transfer of pseudonymous events; storage in Examplestan; analytics purpose; low sensitivity | Signed clauses, Annex III; importer questionnaire |
| Laws and practices of the destination | Fictional: our counsel's memo of 2026-02-15 found a statute allowing access by public authorities with a court order and independent oversight, and the importer reported no requests in the last two years | Counsel memo (fictional), importer statement dated 2026-02-12 |
| Conclusion | No reason to believe the laws and practices prevent the importer meeting its obligations, provided the measures in S6 are in place | |

**6. Supplementary measures**

| Measure | Kind | Who implements | Evidence |
|---|---|---|---|
| User IDs are hashed with a key we hold before sending; no names or email addresses are sent | Technical | Platform team | Code review PR link (fictional) |
| Importer must tell us of any disclosure request and challenge unlawful ones | Contractual | Legal | Clause 14(e) and annex |
| Quarterly check that the sub-processor list is unchanged | Organisational | Security lead | Calendar entry |

**7. Onward transfers:** two sub-processors (Sample Hosting Ltd in Examplestan; Sample Support Ltd in a Member State), listed in Annex III. Governed by Clause 8.8 (Module Two). List reviewed 2026-02-18.

**8. Sources used**

| Source | Version or date | Where read |
|---|---|---|
| Commission list of adequate countries (Art. 45(8)) | checked 2026-02-10 | Commission website |
| Signed Module Two clauses and annexes | 2026-02-20 | Contracts folder |
| Counsel memo on Examplestan law (fictional) | 2026-02-15 | Legal folder |
| Importer statement on requests (fictional) | 2026-02-12 | Vendor register |
| Importer sub-processor list | 2026-02-18 | Vendor portal |

**9. Dates and approval**

| Assessment date | Valid as at | Approved by | Approval date | Outcome |
|---|---|---|---|---|
| 2026-02-22 | 2026-02-22 | Head of Engineering (not the author) | 2026-02-25 | Approved with conditions: keep the hashing in S6 in place |

**10. Reassessment triggers:** the importer adds a sub-processor in a new country; an adequacy decision for Examplestan is adopted (the route would then be reviewed) or the clauses are replaced; the importer notifies a disclosure request or a change in law (Clause 14(e)); the data fields change; yearly by 2027-03-01.

**11. Record of processing:** the Art. 30 record row for "product analytics" links to this record.

**12. Reviewer test:** a reviewer with only this page can say who sent what to whom, under which route and module, why that was allowed on 2026-02-25, what sources support it, which measures were added, who approved it and what would reopen it.
