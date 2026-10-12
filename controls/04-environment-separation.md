# 4. Environment separation

| | |
|---|---|
| **Control ID** | KIT-ENV-01 |
| **Evidence number** | 04 (the `control=` value in evidence headers) |
| **Applies to** | Development, demo and production environments and their data and credentials |
| **Owner (role)** | Platform owner |
| **Review frequency** | Every 365 days or sooner (yearly); the audit flags evidence older than 365 days |
| **Limitations** | A diagram and grants show intent; only a search and a scan show that no real data sits outside production |

**Objective:** Development, demo and production are separate environments with separate data, secrets and access, and production data never flows downhill.

## What to do

- Run dev, demo (if you need one) and production as separate environments, ideally separate cloud accounts or at minimum separate networks, roles and credentials.
- Never copy production data into dev or demo. Seed those environments from a generator or a scrubbed fixture.
- Give each environment its own database users with least privilege. The application's runtime user cannot change the schema; a separate migration user does that.
- Use the same artefact in every environment; only configuration differs.
- Make production reachable only through the front door you intend (for example a CDN with origin authentication), and nothing else.

## Why a reviewer asks

Reviewers ask whether any real customer data exists outside production, and whether a developer's laptop could reach the production database.

## Done when

- [ ] A written statement, enforced by access rules, that production data never leaves production.
- [ ] Dev and demo contain only generated data; a spot check finds no real customer records.
- [ ] The application and migration database users are separate, and the application user has no schema privileges.
- [ ] The production network exposes only what is intended; a port scan confirms it.

## Evidence to keep

- Environment diagram.
- Database user and grant listing for production.
- Seeder or fixture description.
- A dated external port scan of production.

### Kinds of evidence

- **Configuration:** Environment diagram; database grants
- **Operational:** The seeder or fixture description; the external port scan
- **Effectiveness:** A check that the application's database user cannot alter the schema; a search finding no real customer data outside production
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- A "temporary" production dump restored into a test environment.
- The same database password in every environment.
- A demo environment that is publicly reachable and holds real data.
- The runtime user having permission to drop tables.

## Indicative framework references

SOC 2 CC6.1, CC6.6, CC8.1 · ISO 27001:2022 A.8.31, A.8.33, A.8.22 · GDPR Art. 25, 32 · DORA Art. 9

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

Read-only commands for AWS, Google Cloud and Azure, with a status line on each: [`../verify/`](../verify/) (section 04). Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../environments/README.md`](../environments/README.md)
