# 1. Access control

| | |
|---|---|
| **Control ID** | KIT-ACC-01 |
| **Evidence number** | 01 (the `control=` value in evidence headers) |
| **Applies to** | Any system holding company or customer data, and the accounts that reach it |
| **Owner (role)** | The person accountable for security (and each system owner for their system) |
| **Review frequency** | Every 100 days or sooner (quarterly); the audit flags evidence older than 100 days |
| **Limitations** | Showing MFA is enforced and access was reviewed does not show that a stolen session or an over-broad role would be caught |

**Objective:** Every person and service has their own identity, the least access that does the job, multi-factor authentication, and a regular review.

## What to do

- Give each person a named account. No shared logins, including for cloud consoles, the code host and the database.
- Require multi-factor authentication for every human account on the cloud provider, code host, email and password manager. Prefer hardware keys or an authenticator app over SMS.
- Use roles, not long-lived keys, for cloud access. Separate roles for production and non-production, so a mistake or a stolen session in one cannot touch the other.
- Grant the narrowest permission that works. Start from nothing and add; do not start from admin and remove.
- Remove access on the day someone leaves or changes role. Keep a list of who has access to what.
- Review access on a schedule (at least quarterly) and record the review.

## Why a reviewer asks

Reviewers ask to see the list of people with access to production, how access is granted and removed, and proof that MFA is enforced rather than merely available.

## Done when

- [ ] MFA is enforced (not optional) on every human account in every system that holds company or customer data.
- [ ] Production access is a separate role from non-production, and only the people who need it can assume it.
- [ ] No shared accounts and no personal access tokens with broad scope in daily use.
- [ ] A dated access review exists for the last quarter, with every removal acted on.

## Evidence to keep

- The access list (export or screenshot) with the date.
- MFA enforcement setting, screenshotted or exported.
- The completed access review ([`evidence/access-review.md`](../evidence/access-review.md)).
- The offboarding record for the last person who left.

### Kinds of evidence

- **Configuration:** The access list and the MFA enforcement setting
- **Operational:** The completed access review and the offboarding record
- **Effectiveness:** A test that a removed account really cannot sign in; an attempted sign-in without MFA is refused
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- Treating "MFA available" as "MFA enforced".
- A single admin role used for everything, including day-to-day work.
- Service accounts nobody owns and nobody reviews.
- Leaving the founder's personal account as the only owner of the cloud account.

## Indicative framework references

SOC 2 CC6.1, CC6.2, CC6.3 · ISO 27001:2022 A.5.15, A.5.18, A.8.2, A.8.5 · GDPR Art. 32 · DORA Art. 9

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

Read-only commands for AWS, Google Cloud and Azure, with a status line on each: [`../verify/`](../verify/) (section 01). Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../evidence/access-review.md`](../evidence/access-review.md)
