# International transfers

A transfer of personal data outside the EU or EEA needs a valid mechanism (GDPR Chapter V). Hosting in the EU does not settle transfers made by your vendors, support tools, analytics or AI services.

<!-- kit-evidence: control=08 date=YYYY-MM-DD result=pass type=operational -->

Review label: community draft ([`../docs/review-labels.md`](../docs/review-labels.md)). Not legal advice.

## Register (one row per transfer)

| ID | Recipient | Country | What data | Route (Art. 45 / 46 / 49) | Assessment record | Approved by | Reassess by |
|---|---|---|---|---|---|---|---|
| T-01 | <vendor> | <country> | <categories> | Adequacy decision / Appropriate safeguards / Derogation | <link to the record below> | <role> | <YYYY-MM-DD> |

The register is an index. **The decision lives in the assessment record**, so a later reviewer can see why the transfer was considered permissible when it was approved.

## Transfer assessment record (one per transfer)

Complete one record per recipient and purpose. A filled-in example with fictional parties is in [`international-transfers-example.md`](international-transfers-example.md). Do not copy its conclusions: it describes an invented country and vendor.

**1. Transfer ID and purpose:** <T-01; why the data is sent>

**2. Parties and roles**

| | Name | Role (controller / joint controller / processor / sub-processor) | Country | Subject to the GDPR for this processing? |
|---|---|---|---|---|
| Exporter | <you or your customer-facing entity> | <role> | <country> | <yes / no> |
| Importer | <vendor> | <role> | <country> | <yes / no / needs advice> |

The Commission's standard contractual clauses are for an importer whose processing is **not** subject to the GDPR (Decision (EU) 2021/914, Art. 1(1)). If the importer is already subject to it, take advice before relying on them.

**3. The data:** <categories of personal data; categories of people; volume and frequency; special categories (Art. 9) or criminal convictions data (Art. 10): yes / no>

**4. Route.** Chapter V is a ladder: a transfer needs one of the following, and a derogation is available only in the absence of the first two (Art. 49(1)).

| Route | Basis | Chosen? | Details to record |
|---|---|---|---|
| **Adequacy decision** | Art. 45(3) | <yes / no> | <the Commission decision, the territory or sector it covers (it can be narrower than the whole country), date checked on the Commission's published list (Art. 45(8)), whether the recipient is covered> |
| **Appropriate safeguards** | Art. 46(2) | <yes / no> | <instrument: Commission standard clauses (Art. 46(2)(c)), supervisory-authority clauses (Art. 46(2)(d)), binding corporate rules (Art. 47), approved code of conduct, approved certification. **Module** where standard clauses are used: One (controller to controller), Two (controller to processor), Three (processor to processor), Four (processor to controller). Date signed, which options and annexes were completed, who signed> |
| **Derogation** | Art. 49(1) | <yes / no> | <which condition (a) to (g), or the second subparagraph. Derogations are for specific situations; record why neither of the first two routes was available. For the second subparagraph, record each condition and the notice to the supervisory authority and to people (Art. 49(1))> |
| Contract clauses needing authorisation, or administrative arrangements | Art. 46(3) | <yes / no> | <needs the competent supervisory authority's authorisation. Take advice> |

**Why this route:** <one paragraph: why this route and why a route higher up the ladder was not available>

**5. Assessment of the destination** (for the appropriate-safeguards route). The standard clauses require the parties to take due account of, and document, (i) the specific circumstances of the transfer (length of the processing chain, actors, channels, onward transfers, recipient type, purpose, data categories and format, sector, storage location), (ii) the laws and practices of the destination, including rules on disclosure to public authorities and access by them, and (iii) any safeguards added to supplement the clauses (Decision (EU) 2021/914, Clause 14(a) to (d)).

| Element | Finding | Source |
|---|---|---|
| Circumstances of the transfer | <...> | <...> |
| Laws and practices of the destination | <...> | <...> |
| Conclusion | <no reason to believe the laws and practices prevent the importer meeting its obligations / reason to believe they might / needs advice> | |

**6. Supplementary measures** (those that make the safeguard work in practice; Clause 14(b)(iii))

| Measure | Kind (technical / contractual / organisational) | Who implements | Evidence |
|---|---|---|---|
| <for example encryption with keys held by the exporter> | <kind> | <role> | <link> |

If none are needed, say why. If you conclude no appropriate safeguards can be ensured, the transfer is suspended (Clause 14(f)).

**7. Onward transfers:** <the importer's own recipients, sub-processors and their locations; the clause that governs them (Module One: Clause 8.7; Modules Two and Three: Clause 8.8); date the sub-processor list was reviewed; link>

**8. Sources used**

| Source | Version or date | Where read |
|---|---|---|
| <for example the Commission's adequacy decision, the signed clauses, the vendor's sub-processor list, your destination-law analysis> | <date> | <link or file> |

**9. Dates and approval**

| Assessment date | Valid as at | Approved by (role) | Approval date | Outcome |
|---|---|---|---|---|
| <YYYY-MM-DD> | <YYYY-MM-DD> | <role, not the author> | <YYYY-MM-DD> | <approved / approved with conditions / not approved / needs advice> |

**10. Reassessment triggers.** Reassess when any of these happens, and at least yearly:

- the vendor moves processing or storage to a new country, or adds a sub-processor in a new country;
- the adequacy decision is amended, suspended or repealed (Art. 45(5)), or the standard clauses are replaced;
- the importer tells you of a law, or a disclosure request, that is not in line with its obligations (Clause 14(e)), or the destination's laws change;
- the data, the purpose or the volume changes;
- a supervisory authority or court decision affects the route you rely on.

**11. Record in your Art. 30 record.** Transfers, and for the Art. 49(1) second-subparagraph derogation the assessment and suitable safeguards, go into the record of processing (Art. 30(1)(e), Art. 49(6)): link this record from [`record-of-processing.md`](record-of-processing.md).

**12. Reviewer test.** A reviewer who has only this record should be able to say: who sent what to whom, under which route and (where relevant) module, why that was allowed on the approval date, what sources supported it, what measures were added, who approved it, and what would make it need doing again. If any of those answers is missing, the record is incomplete.

Sources for this page: GDPR Chapter V, Art. 44 to 49, and Art. 30(1)(e) (Regulation (EU) 2016/679, Official Journal text); Commission Implementing Decision (EU) 2021/914 of 4 June 2021, Art. 1, Clause 8.7, 8.8 and 14 (Official Journal text). **Pending: the EDPB's Recommendations 01/2020 on measures that supplement transfer tools (final version, 18 June 2021) exist and are the usual reference for supplementary measures, but their content was not read for this page. No case law was read. No country's adequacy status or law is stated here.**

## Steps

1. List every recipient outside the EEA from [`data-inventory.md`](data-inventory.md) and the vendor register, including sub-processors your vendors use. One register row and one assessment record for each.
2. Choose the route in order: adequacy decision first, then appropriate safeguards, and a derogation only where neither is available. An adequacy decision covers the territory or sector it names, which can be narrower than a country: check the current decision.
3. Where you rely on standard contractual clauses, record the module and complete the destination assessment and supplementary measures. Write the assessment down; the clauses expect it to be documented and available to the supervisory authority on request.
4. Have someone other than the author approve it, and record the date and the reassessment triggers.
5. Tell people in your privacy notice that transfers occur and how they are protected.
6. Reassess when a trigger in the record happens, and at least yearly.

Take legal advice for anything unclear: this area changes.
