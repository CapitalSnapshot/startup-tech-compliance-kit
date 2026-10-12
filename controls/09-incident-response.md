# 9. Incident response

| | |
|---|---|
| **Control ID** | KIT-INC-01 |
| **Evidence number** | 09 (the `control=` value in evidence headers) |
| **Applies to** | Any event that may compromise security or personal data, including near misses |
| **Owner (role)** | The incident lead |
| **Review frequency** | Every 365 days or sooner (yearly); the audit flags evidence older than 365 days |
| **Limitations** | A plan and a register show readiness and record-keeping; only a rehearsal or a real incident shows the response works |

**Objective:** You have a short, rehearsed plan for detecting, containing, communicating and learning from an incident.

## What to do

- Name an incident lead and a backup. Write down how to reach them out of hours.
- Define severity levels and the first three actions for each: contain, preserve evidence, communicate.
- Write down who must be told, and when, **by role**: as a **processor**, the controller (each customer) without undue delay and inside any contractual deadline; as a **controller**, the supervisory authority (within 72 hours of awareness where feasible, unless the breach is unlikely to result in a risk) and the people affected where the risk is high. Keep contractual deadlines separate from statutory ones. Note the other regimes that may apply to you ([`../scoping/applicability-matrix.md`](../scoping/applicability-matrix.md)).
- Keep an **incident register** ([`../evidence/incident-register.md`](../evidence/incident-register.md)): open a row when you detect an incident, including near misses and breaches you decide not to notify. Record the notification decision and its reason on the row. GDPR Art. 33(5) requires you to document every personal-data breach, notified or not.
- Follow the first-hour runbook: [`../runbooks/incident-response.md`](../runbooks/incident-response.md).
- Run a tabletop exercise at least yearly and record what you changed afterwards.
- After every incident, write a blameless note: timeline, cause, what worked, what will change, and who owns each change.

## Why a reviewer asks

Reviewers ask for your last incident or exercise and what it changed.

## Done when

- [ ] The plan is one page, current, and known to everyone with production access.
- [ ] A tabletop exercise has been run in the last twelve months, with recorded actions.
- [ ] Every incident since you started is in the register and has a written report, including near misses. If there have been none, the register says so with a start date.
- [ ] Every register row involving personal data (or unknown) has a recorded notification decision with its reason.
- [ ] Notification duties and contacts are listed by role, with each customer's contractual deadline kept separate from the statutory duties.
- [ ] A tabletop exercise has shown that staff can tell contractual notification requirements from statutory controller deadlines ([`../runbooks/tabletop-incident-notification.md`](../runbooks/tabletop-incident-notification.md)).

## Evidence to keep

- The incident plan.
- The exercise record.
- The incident register ([`../evidence/incident-register.md`](../evidence/incident-register.md)) and a report for each incident ([`../evidence/incident-report.md`](../evidence/incident-report.md)).
- The contact list with a date.

### Kinds of evidence

- **Configuration:** The incident plan
- **Operational:** The incident register and reports
- **Effectiveness:** A tabletop exercise with recorded actions that were then done
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- A plan that lives only in one person's head.
- Cleaning up before preserving evidence.
- Blaming a person instead of fixing the system.
- No rehearsal until the first real incident.

## Indicative framework references

SOC 2 CC7.3, CC7.4, CC7.5 · ISO 27001:2022 A.5.24, A.5.25, A.5.26, A.5.27, A.5.28 · GDPR Art. 33, 34 · DORA Art. 17, 18, 19

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

This control is a register, a plan or a review rather than a cloud setting, so there is no cloud command. Check the evidence files named above. Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../runbooks/incident-response.md`](../runbooks/incident-response.md)
- [`../evidence/incident-register.md`](../evidence/incident-register.md)
- [`../evidence/incident-report.md`](../evidence/incident-report.md)
