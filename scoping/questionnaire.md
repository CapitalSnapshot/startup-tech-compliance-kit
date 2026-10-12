# Scoping questionnaire

Copy this into your own repository, answer it, date it, and review it yearly or when your business changes. Answers drive [`applicability-matrix.md`](applicability-matrix.md).

<!-- kit-evidence: control=12 date=YYYY-MM-DD result=pass type=operational -->

**Completed by:** <role> **Date:** <YYYY-MM-DD> **Review by:** <YYYY-MM-DD>

## 1. Outcome

Which do you want? (tick one or more)

- [ ] Good security hygiene
- [ ] Answer enterprise customer security questionnaires
- [ ] A foundation for SOC 2 or ISO 27001. Which one, and why now? <...>

## 2. The company

| Question | Answer |
|---|---|
| People (employees, contractors) | <number> |
| Countries where you operate or are established | <...> |
| Growth plan for the next 12 months | <...> |

## 3. The product and where it runs

| Question | Answer |
|---|---|
| What does the product do, in one sentence? | <...> |
| Architecture (single host, containers, managed services, serverless) | <...> |
| Hosting provider and regions | <...> |
| Is customer data in more than one region or provider? | <...> |
| Do you run your own authentication, or use an identity provider? | <...> |

## 4. Data

| Question | Answer |
|---|---|
| Do you process personal data? Whose (customers' users, employees, prospects)? | <...> |
| Any special-category data (health, biometric, political, etc.) or children's data? | <...> |
| Do you handle payment card data yourself, or only through a payment processor? | <...> |
| Approximate number of people whose data you hold | <...> |
| Does any personal data leave the EU or EEA (including to vendors)? | <...> |
| Do you use personal data to train or fine-tune models? | <...> |

## 4a. GDPR territorial scope

Feeds [`gdpr-territorial-scope.md`](gdpr-territorial-scope.md). The location of people is not the only test.

| Question | Answer |
|---|---|
| Does any group entity, branch, office or agent have an establishment in the Union? Where? | <...> |
| Do you offer goods or services (paid or free) to people in the Union? What shows that you direct them at the Union (languages, currencies, EU domains, marketing, delivery)? | <...> |
| Do you monitor the behaviour of people in the Union (analytics, cookies, device tracking, profiling)? | <...> |
| For this data, are you a controller, a processor, or both? | <...> |
| Which jurisdictions are relevant to the decision? | <...> |
| If you may be subject to the GDPR without an EU establishment, has an EU representative (Article 27) been considered? | <...> |

## 5. Customers and contracts

| Question | Answer |
|---|---|
| Who buys: individuals, SMEs, enterprises, public sector, financial institutions? | <...> |
| Have any asked for SOC 2, ISO 27001, a questionnaire, a penetration test or an audit right? | <...> |
| Do contracts contain security, breach-notification or data-location clauses? | <...> |
| Are you a processor for customers' personal data, a controller, or both? | <...> |

## 6. Regulation

| Question | Answer |
|---|---|
| Are any customers regulated financial entities? Do you provide ICT services to them? | <...> |
| Any sector-specific regime (health, payments, critical infrastructure)? | <...> |
| Could NIS2 apply (a listed sector or type of entity, size, the Member States involved)? Complete [`extensions/nis2-screening.md`](extensions/nis2-screening.md) and record the outcome: potentially in scope / not in scope based on a documented assessment / requires advice. The kit does not assess NIS2 compliance | <outcome, date, link> |
| Have you taken legal advice on the above? Date and by whom | <...> |

## 7. Result

- Frameworks and laws that apply, per [`applicability-matrix.md`](applicability-matrix.md): <...>
- Frameworks we are **deliberately not pursuing yet**, and why: <...>
- Next review date: <YYYY-MM-DD>
