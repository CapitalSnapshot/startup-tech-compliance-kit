# Controls

Twelve controls to put in place first. Each file has the same shape: **what to do**, **why a reviewer asks**, **done when**, **evidence to keep**, **common mistakes**, **indicative framework references** (SOC 2, ISO 27001:2022, GDPR, DORA), and **related** runbooks and templates.

Controls 1 to 11 are mostly technical; control 12 is the governance that makes them repeatable. Read [`../guide/layers-and-outcomes.md`](../guide/layers-and-outcomes.md) first: these controls are one layer of four, and they do not by themselves establish compliance with any framework.

| # | Control | Objective |
|---|---|---|
| 1 | [Access control](01-access-control.md) | Every person and service has their own identity, the least access that does the job, multi-factor authentication, and a regular review. |
| 2 | [Secrets management](02-secrets-management.md) | Secrets live in a secrets manager, never in code, chat or screenshots; every secret has an owner and a rotation or expiry. |
| 3 | [Change management](03-change-management.md) | Every change reaches production through a reviewed pull request and an automated pipeline, with a record of who approved what. |
| 4 | [Environment separation](04-environment-separation.md) | Development, demo and production are separate environments with separate data, secrets and access, and production data never flows downhill. |
| 5 | [Backups and tested restores](05-backups-and-restore.md) | Production data is backed up automatically, encrypted, kept off the primary system, and restored on a schedule to prove it works. |
| 6 | [Logging and monitoring](06-logging-and-monitoring.md) | Security-relevant events are logged centrally, kept for a stated period, protected from tampering, and someone is told when something is wrong. |
| 7 | [Vendor management](07-vendor-management.md) | You know every third party that touches your data, what they hold, what contract covers it, and when you last checked them. |
| 8 | [Data protection (GDPR)](08-data-protection.md) | You know what personal data you hold, why, where, for how long, and how a person can see it or have it erased. |
| 9 | [Incident response](09-incident-response.md) | You have a short, rehearsed plan for detecting, containing, communicating and learning from an incident. |
| 10 | [Supply chain and signing](10-supply-chain-and-signing.md) | You know what is in your software, who built it, and that what runs in production is exactly what your pipeline produced. |
| 11 | [Vulnerability management](11-vulnerability-management.md) | You find known weaknesses in your software and systems, rank them, fix them within stated deadlines, and record the exceptions. |
| 12 | [Risk and governance](12-risk-and-governance.md) | Security is owned by named people, guided by short written policies, driven by a risk register, and reviewed by management on a schedule. |

See also the [control-to-evidence map](evidence-map.md) and the [framework mappings](framework-mappings.md) (editions, why relevant, what more is required). The mappings are data: [`mappings.json`](mappings.json), validated against [`mapping.schema.json`](mapping.schema.json); the page is generated from it.

## How to work through them

1. Fill in [`../scoping/questionnaire.md`](../scoping/questionnaire.md) first, so you know which frameworks and laws apply.
2. Do the controls in order. Access, secrets and change management come first because everything else depends on them.
3. For each one, make the evidence it names and store it, dated, in a controlled place ([`../evidence/handling.md`](../evidence/handling.md)).
4. Where you cannot meet a control yet, write it in your risk register ([`../evidence/risk-register.md`](../evidence/risk-register.md)) with a treatment, an owner and a review date.
