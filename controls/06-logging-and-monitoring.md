# 6. Logging and monitoring

| | |
|---|---|
| **Control ID** | KIT-LOG-01 |
| **Evidence number** | 06 (the `control=` value in evidence headers) |
| **Applies to** | Authentication, administrative and deploy events, and the alerts built on them |
| **Owner (role)** | Platform owner |
| **Review frequency** | Every 365 days or sooner (yearly); the audit flags evidence older than 365 days |
| **Limitations** | Logging being on does not show anyone reads it, or that an attack would be noticed |

**Objective:** Security-relevant events are logged centrally, kept for a stated period, protected from tampering, and someone is told when something is wrong.

## What to do

- Log authentication events, administrative actions, access to sensitive data, and deploys. Do not log passwords, tokens or full payment details.
- Send logs off the host to a store the host cannot edit. Keep them for a stated period.
- Alert on the few things that matter: failed deploys, repeated failed logins, errors above a threshold, certificate and credential expiry, backup failures.
- Know who receives each alert and what they do. An alert nobody reads is not a control.
- Turn on access logging for object storage and the cloud provider's audit trail, in every account.

## Why a reviewer asks

Reviewers ask what you would see if an account were abused, and how long you could look back.

## Done when

- [ ] The cloud audit trail is on in every account and kept for the stated period.
- [ ] Application, authentication and deploy logs are collected off-host.
- [ ] Alerts exist for the events above and each has a named recipient.
- [ ] A test alert has fired and been acknowledged.

## Evidence to keep

- Logging configuration and retention setting.
- The alert list with recipients.
- A dated test alert.
- A sample log line for each event class, with sensitive fields absent.

### Kinds of evidence

- **Configuration:** Logging configuration and retention
- **Operational:** The alert list with recipients
- **Effectiveness:** A test alert that fired and was acknowledged; a sample investigation from the logs
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- Logs on the same host an attacker would control.
- Secrets or personal data in log lines.
- Alerts sent to an inbox nobody watches.
- No log of who changed what in the cloud account.

## Indicative framework references

SOC 2 CC7.1, CC7.2 · ISO 27001:2022 A.8.15, A.8.16, A.8.17 · GDPR Art. 32 · DORA Art. 10

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

Read-only commands for AWS, Google Cloud and Azure, with a status line on each: [`../verify/`](../verify/) (section 06). Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../evidence/evidence-file.md`](../evidence/evidence-file.md) (alert test records)
