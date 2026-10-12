# 12. Risk and governance

| | |
|---|---|
| **Control ID** | KIT-GOV-01 |
| **Evidence number** | 12 (the `control=` value in evidence headers) |
| **Applies to** | The whole programme: roles, policies, risk decisions, training and management review |
| **Owner (role)** | Founder or director responsible for security |
| **Review frequency** | Every 365 days or sooner (yearly); the audit flags evidence older than 365 days |
| **Limitations** | Policies and a register show governance exists; they do not show people follow them or that decisions are good |

**Objective:** Security is owned by named people, guided by short written policies, driven by a risk register, and reviewed by management on a schedule.

## What to do

- Name who is accountable for information security, and write down the other roles: system owners, the person who approves access, the incident lead, the privacy contact. One person may hold several roles; say so.
- Keep a **risk register** and use the scoring and acceptance rules in [`../risk/methodology.md`](../risk/methodology.md). Do not let the owner of a serious risk be the only one who can accept it.
- Keep a small set of **short policies** that match what you actually do ([`../policies/`](../policies/)). A policy nobody follows is worse than none.
- Onboard and offboard people the same way every time: accounts, training, device, agreements; and removal on the last day.
- Give everyone with access a brief **security awareness** session at joining and yearly, and record it.
- Hold a **management review** at least yearly (more often if you are pursuing a certification): review risks, incidents, audit results, changes in the business and the scoping answers; decide actions with owners and dates.
- Revisit your scoping ([`../scoping/questionnaire.md`](../scoping/questionnaire.md)) when your customers, data or products change.
- If you pursue ISO 27001, an ISMS also needs internal audit and continual improvement. These policies and reviews are the start of that.

## Why a reviewer asks

Reviewers ask who is responsible, how you decide what to fix first, and whether anyone senior looks at the programme and acts on what they find.

## Done when

- [ ] Roles and responsibilities are written down and people know theirs.
- [ ] The risk register exists, is scored, and has owners and review dates.
- [ ] The core policies exist, are dated, and are acknowledged by staff.
- [ ] Onboarding and offboarding follow a checklist and the last leaver's record exists.
- [ ] Training records exist for everyone with access.
- [ ] A dated management review exists for the last twelve months, with actions.
- [ ] The scoping questionnaire is current.

## Evidence to keep

- The roles document and the policy set with dates.
- The risk register and last review.
- Onboarding and offboarding checklists, with the last example.
- Training records.
- The management review minutes and action list.
- The completed scoping questionnaire.

### Kinds of evidence

- **Configuration:** The policies and roles documents
- **Operational:** Training records; management review minutes
- **Effectiveness:** An internal review that found and fixed a gap; an independent assessment where required
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- Policies copied from the internet that do not describe what you do.
- A risk register nobody reviews.
- Governance owned by one person who is also the person being governed.
- Treating the policies as the control. The behaviour and the evidence are the control.

## Indicative framework references

SOC 2 CC1.1 to CC1.5, CC3.1 to CC3.4, CC5.3 · ISO 27001:2022 clauses 4 to 10, A.5.1, A.5.2, A.5.4, A.6.1 to A.6.8 · GDPR Art. 24, 5(2) · DORA Art. 5, 6

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

This control is a register, a plan or a review rather than a cloud setting, so there is no cloud command. Check the evidence files named above. Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../risk/methodology.md`](../risk/methodology.md)
- [`../policies/README.md`](../policies/README.md)
- [`../evidence/risk-register.md`](../evidence/risk-register.md)
- [`../scoping/questionnaire.md`](../scoping/questionnaire.md)
