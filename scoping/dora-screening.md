# DORA screening: three kinds of obligation

> **Standing notice.** This is repository based, community maintained guidance. It is not legal advice, a formal compliance assessment, a certification or an independent security audit. Mappings and statements about frameworks are unverified unless their review label says otherwise ([review labels](../docs/review-labels.md)).

**Review label: community draft.** Proposed guidance. It has not been reviewed by a maintainer or by a specialist. It is decision support, not legal advice, and it never concludes that DORA does or does not apply to you. **Get specialist advice** before relying on it.

Source used: Regulation (EU) 2022/2554 (DORA), articles cited below, official text as published in the Official Journal of the European Union (Publications Office edition, English). Provisions read for this page: Article 2 (paragraphs 1 to 4), Article 3 (definitions of ICT third-party service provider, critical ICT third-party service provider, ICT third-party risk and critical or important function), Article 4 (paragraphs 1 and 2), Article 28(1), Article 30(1) to (4), Article 31(1), (2) and (11) to (13), and Article 33(1). **Articles 5, 6, 9 to 12 and 17 to 19 were checked by title only; the kit does not describe their content (source verification pending for anything more specific).**

<!-- kit-evidence: control=12 date=YYYY-MM-DD result=pass type=operational -->

## Why three kinds

A startup that serves a regulated financial entity may meet significant requirements **without** being directly subject to every duty the Regulation places on that financial entity. The requirement may come from a contract. Separately, there is an oversight framework for ICT providers designated as critical. Mixing these up leads to the wrong question ("does DORA apply to us?") and the wrong answer.

| Obligation type | Who owes it | Where it comes from | What it can look like for a startup |
|---|---|---|---|
| **Direct statutory duty** | A **financial entity** within Article 2 | The Regulation itself: for example governance (Art. 5), the ICT risk management framework (Art. 6), protection and prevention (Art. 9), detection (Art. 10), response and recovery (Art. 11), backup and recovery (Art. 12), incident management and reporting (Arts. 17 to 19), and managing ICT third-party risk (Art. 28) | Usually none directly, unless **you are** a financial entity. Your customer owes it |
| **Contractual flow-down** | The ICT provider, **by contract** | The financial entity remains "fully responsible" for its obligations even when it uses ICT services (Art. 28(1)(a)), and must set out the rights and obligations in writing with at least the elements in Article 30(2), and more for services supporting critical or important functions (Art. 30(3)) | Contract terms a financial-entity customer asks you to accept: service levels, data locations, data return, incident assistance, audit and access rights, termination rights |
| **Oversight obligation** | An ICT third-party service provider **designated as critical** | Article 31 (designation by the European Supervisory Authorities) and the oversight framework that follows (for example the Lead Overseer's tasks in Article 33) | Only if designated. A provider not on the list may apply to be designated (Art. 31(11)) |

## What the text says about scope (read for this page)

- **Article 2(1)** lists the entities the Regulation applies to. Points (a) to (t) are financial entities such as credit institutions, payment institutions, e-money institutions, investment firms, insurers and others. **Point (u) is "ICT third-party service providers".**
- **Article 2(2)** defines "financial entities" as the entities in points (a) to (t), so ICT third-party service providers are in the Regulation's scope list but are not "financial entities".
- **Articles 2(3) and 2(4)** exclude some entities and let Member States exclude others. Whether one applies to a particular financial entity is a legal question.
- **Article 3** defines an "ICT third-party service provider" as an undertaking providing ICT services, and a "critical ICT third-party service provider" as one designated as critical under Article 31.
- **Article 4** requires a financial entity to apply parts of the Regulation proportionately to its size, risk profile and the nature, scale and complexity of what it does.

**Do not assume.** The obligations this page identifies for providers are the contractual ones (from the financial entity's Articles 28 and 30) and the oversight framework for designated critical providers. This page does not identify any other direct duty on a provider that has not been designated. That is not a finding that there is none: take advice.

## Screening path for a startup

Record the facts, then take the questions in order. Every outcome is decision support.

1. **Are you a financial entity?** Check Article 2(1)(a) to (t) against what you do and are authorised to do (for example payment, e-money, investment, crypto-asset services, insurance distribution).
   - **Yes or possibly:** **DORA may apply to you directly** (direct statutory duties). Check the exclusions in Article 2(3) and (4). **Route to legal review.**
   - **No:** go to 2.
2. **Do you provide ICT services to a financial entity?** An ICT service here means a service you provide that the financial entity uses to run its operations. List each such customer and service.
   - **Yes:** **contract terms are likely.** Read each customer's contract against Article 30(2) and, where the service supports a critical or important function of the customer, Article 30(3). Record what each customer requires. Go to 3.
   - **No:** record that on the facts, and set a review date. Go to the outcomes.
   - **Unsure whether your service counts:** **needs advice.**
3. **Any sign of designation as critical?** Are you used by many financial entities, by systemically important ones, or for critical or important functions of many (Article 31(2) sets the criteria the authorities use)? Have you been notified, listed, or considered applying (Art. 31(11))?
   - **Yes or possibly:** **oversight obligation possible: route to legal review.**
   - **No:** record the facts, and set a review date.

## Outcomes

| Outcome | Meaning | Next |
|---|---|---|
| **Direct statutory duties may apply (financial entity)** | You may be within Article 2(1)(a) to (t) | Legal review; map the kit's controls as supporting practice only |
| **Contractual flow-down likely** | A financial-entity customer may require DORA-derived terms | Review each contract against Article 30; record accepted terms; use the kit's controls as evidence you can offer |
| **Oversight obligation possible** | Designation as critical is possible | Legal review |
| **Needs advice** | Facts or law unclear | Legal review |
| **No route identified on the facts recorded** | **Not a finding that DORA is irrelevant to you.** | Record facts and reasoning; recheck when you take a financial-entity customer, change services, or grow |

## What a financial-entity customer may ask you to accept (paraphrase of Article 30(2) and (3))

Always, for any ICT service contract (Art. 30(2)): a clear description of the services and any permitted subcontracting; the locations where services are provided and data is processed, with advance notice of changes; provisions on availability, authenticity, integrity and confidentiality of data; access to, recovery and return of data on insolvency, discontinuation or termination; service level descriptions; assistance with ICT incidents at no additional or a pre-agreed cost; cooperation with the customer's authorities; termination rights and notice periods; and participation in the customer's security awareness and resilience training.

Additionally, where the service supports a critical or important function (Art. 30(3)): full service levels with quantitative targets; notice and reporting obligations on material developments; implementing and testing business contingency plans and appropriate ICT security; participation in the customer's threat-led penetration testing; and ongoing monitoring rights, including access, inspection and audit.

The list is a summary for orientation. Use the Regulation's text and your customer's actual contract.

## Record the decision

| Item | Entry |
|---|---|
| Obligation types considered | <direct / contractual / oversight> |
| Facts relied on (customers, services, authorisations) | <...> |
| Outcome | <...> |
| Advice taken (who, date) | <...> |
| Decision owner (role) and date | <role>, <YYYY-MM-DD> |
| Review date and triggers | <YYYY-MM-DD>, and on any change in the facts above |

Related: [`applicability-matrix.md`](applicability-matrix.md), [`../controls/framework-mappings.md`](../controls/framework-mappings.md).
