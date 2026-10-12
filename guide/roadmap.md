# Roadmap

Four phases. Do them in order; do not polish policies while production credentials are exposed or backups are untested.

## Phase 1: secure baseline (days)

Reduce the immediate technical risks. Implement and **test** them.

- MFA on critical accounts. Restricted production access. Secrets in a secrets manager.
- Protected branches. Dependency and secret scanning.
- Automated backups and a successful restore test. Cloud audit logging.
- A named incident owner. A first risk register.

Use [`../checklists/first-week.md`](../checklists/first-week.md).

## Phase 2: operational accountability (weeks)

Make security repeatable instead of depending on the founder remembering.

- An inventory of systems, services and data ([`../privacy/data-inventory.md`](../privacy/data-inventory.md)).
- A vendor register, an access-review schedule, a vulnerability process with deadlines ([`../controls/11-vulnerability-management.md`](../controls/11-vulnerability-management.md)).
- A documented incident escalation, a retention and deletion process, short policies ([`../policies/`](../policies/)).
- A risk register with owners and treatment decisions ([`../risk/`](../risk/)).

Keep it proportionate. A three-person startup does not need a 500-person approval structure. It does need to know who can reach production, where customer data lives, and what happens when something goes wrong.

## Phase 3: customers and due diligence (weeks to months)

Be able to **show** your controls work. Build on [`../evidence/`](../evidence/) and the [control-to-evidence map](../controls/evidence-map.md). Store evidence in a controlled place ([`../evidence/handling.md`](../evidence/handling.md)). Use [`../checklists/before-investor-data-room.md`](../checklists/before-investor-data-room.md).

## Phase 4: choose a formal destination

Decide whether you need a formal framework or a strong baseline. **Do not pursue SOC 2 or ISO 27001 because the kit mentions them.** First establish what customers, contracts, regulators and commercial plans actually require.

| Your situation | Suggested direction |
|---|---|
| Very early SaaS, no enterprise customers | Security fundamentals and basic privacy governance |
| Selling to SMEs | Keep the baseline; prepare a clear questionnaire answer set and an evidence pack |
| Selling to larger enterprises | Map customer requirements to your controls; identify contractual, assurance and audit expectations |
| An enterprise explicitly asks for SOC 2 | Assess the applicable Trust Services Criteria, define scope, plan the examination with an assessor |
| A customer or partner requires ISO 27001 | Build an ISMS; map applicable requirements and Annex A controls; plan internal audit and management review |
| Your processing may fall within the GDPR's territorial scope (see [`../scoping/gdpr-territorial-scope.md`](../scoping/gdpr-territorial-scope.md)) | Assess GDPR obligations independently of SOC 2 or ISO 27001 |
| You serve regulated financial services customers | Assess sector obligations, including whether DORA-related requirements reach you directly or through contract |

The general steps for the two common frameworks are in [`paths/`](paths/). Details of what applies when: [`../scoping/applicability-matrix.md`](../scoping/applicability-matrix.md).
