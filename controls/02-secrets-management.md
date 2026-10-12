# 2. Secrets management

| | |
|---|---|
| **Control ID** | KIT-SEC-01 |
| **Evidence number** | 02 (the `control=` value in evidence headers) |
| **Applies to** | Every credential, key and token the company holds, in any environment |
| **Owner (role)** | The platform owner |
| **Review frequency** | Every 365 days or sooner (yearly); the audit flags evidence older than 365 days |
| **Limitations** | A clean secret scan and a register do not prove no secret exists somewhere unscanned, or that rotation would work in an emergency until you have done one |

**Objective:** Secrets live in a secrets manager, never in code, chat or screenshots; every secret has an owner and a rotation or expiry.

## What to do

- Keep credentials, API keys and tokens in a secrets manager. Build runtime environment files from it at deploy time, root-only, and never commit them.
- Name each secret per environment. Production and non-production never share a secret.
- Record each secret: what it is, where it is used, who owns it, the last four characters, and when it expires or was last rotated. Never record the value.
- Prefer credentials that expire on their own. Where a credential cannot expire, diary a rotation.
- Scan the code and its history for secrets on every change, and again before anyone outside the company gets read access.
- When a secret is exposed, treat it as compromised: rotate first, then investigate. Write down what happened.

## Why a reviewer asks

Reviewers look for secrets in the repository history and ask how you would rotate one in an emergency. They also ask what stops a developer laptop from holding production keys.

## Done when

- [ ] A secret scan runs on every change and blocks a merge on a hit.
- [ ] A register lists every secret by name, owner, last four characters and expiry; it holds no values.
- [ ] Production secrets cannot be read by non-production roles.
- [ ] You have rotated at least one production secret end to end, and the steps are written down.

## Evidence to keep

- The secrets register.
- Secret-scan configuration and a passing run.
- The rotation runbook and a dated record of one rotation.
- An incident note for any exposure, even a small one.

### Kinds of evidence

- **Configuration:** The secrets register; the secret-scan configuration
- **Operational:** A dated rotation record
- **Effectiveness:** A test that a deliberately planted dummy secret is caught by the scan; a rotation completed end to end with no outage
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- A secret committed once and "deleted" in a later commit; it is still in history.
- Pasting a secret into a chat, ticket or AI assistant.
- One API key shared by dev and production.
- A key that expires and nobody knows when.

## Indicative framework references

SOC 2 CC6.1, CC6.7 · ISO 27001:2022 A.5.17, A.8.24, A.8.4 · GDPR Art. 32 · DORA Art. 9

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

Read-only commands for AWS, Google Cloud and Azure, with a status line on each: [`../verify/`](../verify/) (section 02). Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../evidence/evidence-file.md`](../evidence/evidence-file.md) (rotation records)
