# Verify

For each control, how to **produce the evidence** with read-only commands, by provider. The kit does not run these for you and holds no credentials: you run them, save the output, and the audit ([`../audit/`](../audit/)) tracks that the evidence is recent.

| File | What it covers | Status |
|---|---|---|
| [`aws.md`](aws.md) | AWS CLI | Run read-only against a real account; each command has its own status line |
| [`gcp.md`](gcp.md) | Google Cloud CLI | **Untested** |
| [`azure.md`](azure.md) | Azure CLI | **Untested** |
| [`common.md`](common.md) | Code host and image signing, any provider | See each command |
| [`_template.md`](_template.md) | Start a new provider | |

## By control

| # | Control | AWS | Google Cloud | Azure |
|---|---|---|---|---|
| 01 | Access control | [aws](aws.md#01-access-control) | [gcp](gcp.md#01-access-control) | [azure](azure.md#01-access-control) |
| 02 | Secrets management | [aws](aws.md#02-secrets-management) | [gcp](gcp.md#02-secrets-management) | [azure](azure.md#02-secrets-management) |
| 03 | Change management | [aws](aws.md#03-change-management) | [gcp](gcp.md#03-change-management) | [azure](azure.md#03-change-management) |
| 04 | Environment separation | [aws](aws.md#04-environment-separation) | [gcp](gcp.md#04-environment-separation) | [azure](azure.md#04-environment-separation) |
| 05 | Backups and tested restores | [aws](aws.md#05-backups-and-tested-restores) | [gcp](gcp.md#05-backups-and-tested-restores) | [azure](azure.md#05-backups-and-tested-restores) |
| 06 | Logging and monitoring | [aws](aws.md#06-logging-and-monitoring) | [gcp](gcp.md#06-logging-and-monitoring) | [azure](azure.md#06-logging-and-monitoring) |
| 07 | Vendor management | [aws](aws.md#07-vendor-management) | [gcp](gcp.md#07-vendor-management) | [azure](azure.md#07-vendor-management) |
| 08 | Data protection | [aws](aws.md#08-data-protection) | [gcp](gcp.md#08-data-protection) | [azure](azure.md#08-data-protection) |
| 09 | Incident response | [aws](aws.md#09-incident-response) | [gcp](gcp.md#09-incident-response) | [azure](azure.md#09-incident-response) |
| 10 | Supply chain and signing | [aws](aws.md#10-supply-chain-and-signing) | [gcp](gcp.md#10-supply-chain-and-signing) | [azure](azure.md#10-supply-chain-and-signing) |
| 11 | Vulnerability management | [aws](aws.md#11-vulnerability-management) | [gcp](gcp.md#11-vulnerability-management) | [azure](azure.md#11-vulnerability-management) |
| 12 | Risk and governance | [aws](aws.md#12-risk-and-governance) | [gcp](gcp.md#12-risk-and-governance) | [azure](azure.md#12-risk-and-governance) |

Code host and signing checks (controls 03 and 10) are in [`common.md`](common.md).

## Rules

- **Read-only.** Never include a command that changes anything, or that prints a secret value.
- **Placeholders** in CAPITALS. No real names, accounts, addresses or buckets.
- **A status for every command.** `UNTESTED` is honest and fine. Claiming `TESTED` without running it is not.
- **Evidence, not proof of effectiveness.** A command shows a setting. Whether the setting is *enough* is a human judgement ([`../audit/README.md`](../audit/README.md)).
- **Save output safely.** Redact identifiers, and keep it in a controlled place ([`../evidence/handling.md`](../evidence/handling.md)).

## Adding a provider

Regional and EU-native cloud providers are welcome to add their own file. Copy [`_template.md`](_template.md) to `verify/<provider>.md`, fill in what you have run, leave the rest `UNTESTED`, and open a pull request. A test checks that every control has a section and that every command has a valid status line. See [`../CONTRIBUTING.md`](../CONTRIBUTING.md).
