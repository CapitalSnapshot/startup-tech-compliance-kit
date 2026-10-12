# NIS2 screening worksheet

<!-- kit-decision-record: nis2-screening -->

> **Standing notice.** This is repository based, community maintained guidance. It is not legal advice, a formal compliance assessment, a certification or an independent security audit. Mappings and statements about frameworks are unverified unless their review label says otherwise ([review labels](../../docs/review-labels.md)).

Review label: community draft ([`../../docs/review-labels.md`](../../docs/review-labels.md)). Not legal advice. Part of the [extensions](README.md): a screening aid, not an assessment.

**The kit does not assess NIS2 compliance.** This worksheet records whether Directive (EU) 2022/2555 ("NIS2") may apply to you, so that the question is asked, the facts and sources are written down, and a person decides. A directive binds Member States: what applies to an entity is the **national law** of each Member State involved, and it can differ from the Directive. This page does not state the transposition status of any Member State.

Complete every section. Where you do not know, write "unsure". Any "unsure" or blank in sections 1 to 6 means the outcome is **requires advice**.

**Entity:** <legal name> **Completed by (role):** <role> **Date:** <YYYY-MM-DD>

## 1. Sector, subsector and type of entity

NIS2 applies to entities "of a type referred to in Annex I or II" (Art. 2(1)). Annex I is "sectors of high criticality" and Annex II is "other critical sectors". Each sector lists subsectors and types of entity; read the annex text for the exact types, because a sector name alone is not enough.

| Annex I sectors | Annex II sectors |
|---|---|
| Energy; Transport; Banking; Financial market infrastructures; Health; Drinking water; Waste water; Digital infrastructure; ICT service management (business-to-business); Public administration; Space | Postal and courier services; Waste management; Manufacture, production and distribution of chemicals; Production, processing and distribution of food; Manufacturing (medical devices, computer, electronic and optical products, electrical equipment, machinery, motor vehicles, other transport equipment); Digital providers; Research |

**Types a software or online-service company most often needs to check** (Annex I, digital infrastructure and ICT service management; Annex II, digital providers): cloud computing service providers, data centre service providers, content delivery network providers, DNS service providers, TLD name registries, trust service providers, providers of public electronic communications networks or services, managed service providers, managed security service providers, providers of online marketplaces, online search engines and social networking services platforms.

The Directive does not list "software vendor" or "SaaS provider" as a type. Whether your service is a "cloud computing service" (Art. 6(30)), a "managed service provider" (Art. 6(39)) or another listed type depends on the definitions and on how national law and the supervisory authority read them. **If it is not clear, answer "unsure".**

| Field | Entry |
|---|---|
| What your service does, in plain words | <...> |
| Annex and sector | <Annex I / Annex II / neither / unsure, and the sector> |
| Subsector and type of entity | <the type as worded in the annex, or "none matches" with the reason> |
| Definition checked (Art. 6) | <which definitions you compared your service against> |
| Reasoning | <why your service does or does not fit the type> |

## 2. Size

Art. 2(1) applies the Directive to listed entities that qualify as medium-sized enterprises under Art. 2 of the Annex to Recommendation 2003/361/EC, or exceed the ceilings for medium-sized enterprises. That Art. 2 defines the SME category: fewer than 250 persons employed, and annual turnover not exceeding EUR 50 million and/or an annual balance sheet total not exceeding EUR 43 million (Art. 2(1) of the Annex). Within it, a **small** enterprise has fewer than 50 persons and turnover and/or balance sheet total not above EUR 10 million (Art. 2(2)), and a **micro** enterprise fewer than 10 persons and not above EUR 2 million (Art. 2(3)). The Recommendation gives no separate figure for "medium-sized": read it as an SME that is neither small nor micro, and take advice if you sit near a line. The Directive disapplies Art. 3(4) of the Annex (ownership by public bodies) for its purposes (Art. 2(1), second subparagraph).

**Partner and linked enterprises count.** Staff and financial figures are not only your own: Art. 3 of the Annex adds the figures of partner and linked enterprises (for example, an investor or parent holding 25% or more of capital or voting rights), with exceptions for certain investors. Check it before you decide you are below the ceilings.

| Field | Entry |
|---|---|
| Persons employed (your own, and how counted) | <number> |
| Annual turnover (last approved period) | <EUR> |
| Annual balance sheet total | <EUR> |
| Autonomous, partner or linked enterprise (Annex Art. 3), and any figures added | <...> |
| Size result | <micro or small / medium-sized / above the SME ceilings / unsure> |
| Essential or important entity (Art. 3), if it applies | <essential / important / not applicable / unsure> |

## 3. Routes that do not depend on size (Art. 2(2) to (4))

Answer each. "Yes" or "unsure" on any row means the size result in section 2 does not settle the question.

| Route | Yes / no / unsure |
|---|---|
| Public electronic communications networks or services, trust service providers, or top-level domain name registries or DNS service providers (Art. 2(2)(a)) | <...> |
| Sole provider in a Member State of a service essential for critical societal or economic activities (Art. 2(2)(b)) | <...> |
| Disruption could significantly affect public safety, security or health (Art. 2(2)(c)) | <...> |
| Disruption could induce a significant systemic risk, especially with cross-border impact (Art. 2(2)(d)) | <...> |
| Critical because of specific national or regional importance for the sector (Art. 2(2)(e)) | <...> |
| Public administration entity (Art. 2(2)(f)) | <...> |
| Identified as a critical entity under Directive (EU) 2022/2557 (Art. 2(3)) | <...> |
| Provides domain name registration services (Art. 2(4)) | <...> |

## 4. Exceptions and exclusions

| Question | Yes / no / unsure | Notes |
|---|---|---|
| Does the entity act in national security, public security, defence or law enforcement, or serve only public administration of that kind (Art. 2(7) and (8); not for trust service providers, Art. 2(9))? | <...> | <...> |
| Has a Member State exempted the entity from Regulation (EU) 2022/2554 under its Art. 2(4) (Art. 2(10))? | <...> | <...> |
| Has a Member State used its option to extend the Directive to others, such as local public administration or education institutions (Art. 2(5))? | <...> | <...> |

## 5. Jurisdiction and registration

Entities are under the jurisdiction of the Member State in which they are established (Art. 26(1)). For some types (including DNS service providers, TLD name registries, cloud computing service providers, data centre service providers, content delivery network providers, managed service providers, managed security service providers, online marketplaces, online search engines and social networking platforms) it is the Member State of the **main establishment in the Union**: where decisions on cybersecurity risk-management measures are predominantly taken, with fallbacks (Art. 26(1)(b) and (2)). An entity of those types that is not established in the Union but offers services there must designate a representative in the Union (Art. 26(3)). Member States also keep lists and registries of entities (Art. 3(3) and (4), Art. 27).

| Field | Entry |
|---|---|
| Member States where you are established | <...> |
| Main establishment in the Union, and how decided (Art. 26(2)) | <Member State and reasoning, or "not applicable"> |
| Not established in the Union but offering services there: representative designated (Art. 26(3))? | <yes, where / no / not applicable / unsure> |
| Member States where you provide services | <...> |
| Registered or listed with a competent authority (Art. 3(4), Art. 27)? | <yes, date and Member State / no / not asked / unsure> |

## 6. National law for each Member State involved

Complete one row for **every** Member State in section 5. The kit does not say what any of them has done. Look up the national law and the competent authority yourself, record the date you checked, and note where it differs from the Directive (scope, size, extra sectors, exceptions, deadlines).

| Member State | National law (name and reference) | Status as you found it | Date checked | Source (link) | Differences from the Directive | Checked by (role) |
|---|---|---|---|---|---|---|
| <...> | <...> | <...> | <YYYY-MM-DD> | <...> | <...> | <...> |

The Directive required Member States to adopt and publish their measures by 17 October 2024 (Art. 41(1)). That date does not tell you whether a given Member State has done so.

## 7. Outcome

Choose one. The outcome is decision support, not a legal conclusion.

| Outcome | Use it when | What it needs |
|---|---|---|
| **Potentially in scope** | Sections 1 to 3 suggest the Directive, or national law implementing it, may apply to you and no exception in section 4 clearly removes you | Move to a compliance programme with advice. The kit does not provide one. |
| **Not in scope based on a documented assessment** | Every section is complete, **no answer is "unsure"**, section 6 is filled in for **each** Member State involved, and the facts point away from scope | A **written rationale**, a **reviewer** (role and date), and the review date below. Without all three, use "requires advice". |
| **Requires advice** | Any "unsure" or blank, any Member State not yet checked, a type that does not clearly fit, or the reviewer disagrees | Take legal advice. This is the default. |

| Field | Entry |
|---|---|
| Outcome | <potentially in scope / not in scope based on a documented assessment / requires advice> |
| Rationale | <the reasoning, in a few sentences. Required for "not in scope based on a documented assessment"> |
| Reviewer (role) | <who reviewed the facts and sources. Not the person who completed the worksheet> |
| Review date | <YYYY-MM-DD> |
| Legal review outcome | <advice taken: yes / no. If yes, by whom (firm or role), date, and what was decided> |
| Next review | <YYYY-MM-DD. Review yearly, when the service, size, ownership or Member States change, and when national law changes> |

## 8. If a customer is in scope and you are not

Even where the Directive does not apply to you, a customer that is an essential or important entity must take cybersecurity risk-management measures that include **supply chain security**, covering "security-related aspects concerning the relationships between each entity and its direct suppliers or service providers" (Art. 21(2)(d)), and must take into account the vulnerabilities specific to each direct supplier (Art. 21(3)). Expect such a customer to ask you for security terms and evidence by **contract**. That is a contractual request, not a direct duty on you under the Directive. Keep the request and your answer with your evidence, and decide with advice what to accept.

## Sources

- Directive (EU) 2022/2555 (Official Journal text, Publications Office edition): Art. 1, 2, 3, 6 (definitions in points 30 and 39 and the list), 21(2)(d) and (3), 26, 27, 41(1), Annexes I and II.
- Commission Recommendation 2003/361/EC, Annex, Art. 2 and 3 (read as published; Art. 4 to 6 on data and reference periods were not read).
- **Pending:** the Commission's and ENISA's guidance on the Directive's scope and size rules, Commission implementing acts under Art. 21(5), and every Member State's national law were **not read**. No Member State's transposition status is stated.
