# Applicability matrix

> **Standing notice.** This is repository based, community maintained guidance. It is not legal advice, a formal compliance assessment, a certification or an independent security audit. Mappings and statements about frameworks are unverified unless their review label says otherwise ([review labels](../docs/review-labels.md)).

What applies to you depends on your business, customers and location. This matrix separates **universal good practice** from **legal obligations** from **commercial or framework requirements**. It is a starting point for a conversation with a qualified adviser, not an answer.

| Item | Obligation type | Applies when | Who decides | What the kit gives you |
|---|---|---|---|---|
| Technical security controls (MFA, secrets, backups, logging...) | Good practice | Always | You | [`../controls/`](../controls/) |
| **GDPR** | Law | Your processing may fall within its territorial scope (Art. 3): it is in the context of an establishment in the Union, **or**, if you are not established there, it relates to offering goods or services to, or monitoring the behaviour of, people in the Union. **The location of the people is not the only test.** Use [`gdpr-territorial-scope.md`](gdpr-territorial-scope.md) (community draft) | You, with legal advice | [`../privacy/`](../privacy/). Needs lawful bases, rights handling, retention, transfers and more |
| Data Protection Officer | Law (conditions) | Only where GDPR Art. 37 applies: public authority, large-scale regular and systematic monitoring, or large-scale special-category data | You, with legal advice | A screening note in [`../privacy/dpo-screening.md`](../privacy/dpo-screening.md). **Most startups do not need one** |
| ePrivacy / cookie rules | Law | You use cookies or similar tracking on a site or app | You, with legal advice | Not covered |
| **SOC 2** | Customer-driven assurance | A customer or investor requires a report | The customer; you choose scope and criteria with an assessor | Technical baseline and evidence. Not scope, criteria, or operating history |
| **ISO/IEC 27001** | Customer- or market-driven certification | A customer or partner requires it, or you choose it | You, with a certification body | Technical controls only. An ISMS also needs risk treatment, internal audit, management review ([`../controls/12-risk-and-governance.md`](../controls/12-risk-and-governance.md)) |
| **DORA: duties of a financial entity** | Direct statutory duty | You are a financial entity within Article 2(1)(a) to (t) of Regulation (EU) 2022/2554 and not excluded by Article 2(3) or (4) | Your regulator, with legal advice | [`dora-screening.md`](dora-screening.md) (community draft). The kit's control references to DORA are indicative practice, not a statement that you owe these duties |
| **DORA: terms passed to ICT providers** | Contractual flow-down | A financial-entity customer uses your service as an ICT service and its contract requires DORA-derived terms (Article 30 sets the minimum contract content) | Your customer's contract, with legal advice | [`dora-screening.md`](dora-screening.md). This is a contract term, **not** a direct duty on you under the financial entity's articles |
| **DORA: oversight of critical ICT providers** | Oversight obligation | You are designated as a critical ICT third-party service provider (Article 31), or have applied to be (Article 31(11)). Article 2(1)(u) also lists ICT third-party service providers in the Regulation's scope, so take advice on any direct duty | The European Supervisory Authorities designate; legal advice | [`dora-screening.md`](dora-screening.md). Not a universal startup requirement |
| **NIS2** | Law (a directive, applied through national law) | You are an entity of a type listed in Annex I or II of Directive (EU) 2022/2555 and are medium-sized or larger (or reach it by a size-independent route), **and** the national law of a Member State where you are established or provide services applies it to you | Your national competent authority, with legal advice | **Not assessed by the kit.** Screening worksheet only: [`extensions/nis2-screening.md`](extensions/nis2-screening.md) (community draft). The kit does not assess NIS2 compliance and does not state any Member State's transposition status |
| PCI DSS | Industry standard | You store, process or transmit payment card data | Your acquirer, processor | Avoid scope: use a payment processor so card data never touches your systems |
| Sector rules (health data, public sector, critical infrastructure) | Law / contract | Your customers or data fall in those sectors | Legal advice | Not covered |
| Customer questionnaires and audit rights | Contract | A customer sends one | The contract | Evidence pack, vendor register, [`../checklists/`](../checklists/) |

## Applicability is not coverage

This matrix records whether an obligation may **apply to you**. [`../docs/review-labels.md`](../docs/review-labels.md) defines how far the **kit covers** a requirement, with six statuses. They are different questions. An item that is **not listed here has not been assessed**: its absence does not mean it does not apply to you. Everything in this matrix is a **community draft**.

## Using it

1. Answer [`questionnaire.md`](questionnaire.md).
2. For each row, mark: **applies**, **does not apply**, **unknown: ask**.
3. Anything marked unknown goes to your risk register with an owner and a date to find out.
4. Do not pursue a framework only because it is on this list. Pursue it because a customer, contract, regulator or plan requires it.

## Reminder

The kit's control files cite SOC 2, ISO 27001, GDPR and DORA references as **indicative**. A reference means the control is relevant to the requirement. It does not mean the control satisfies it.
