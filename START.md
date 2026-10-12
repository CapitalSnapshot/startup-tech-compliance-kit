# Start here (first hour)

Answer five questions. You can do it here, or run `python3 scripts/kit_start.py`, which asks the same questions and writes a plan with links. Neither reads your systems or sends anything anywhere.

| # | Question | Answers |
|---|---|---|
| 1 | Where are you? | Pre-launch · In production · Serving or selling to enterprise customers |
| 2 | Where does your application run? | Managed cloud · A single server · A platform-as-a-service · A legacy environment to move off |
| 3 | What data do you process? | None yet · Business data only · Personal data · Special-category, children's or card data |
| 4 | Does any customer require a framework? | No · Questionnaires only · SOC 2 · ISO 27001 · Regulated financial customers |
| 5 | How many people can reach your systems? | 1 to 3 · 4 to 10 · 11 to 50 · More than 50 |

## Where each profile starts

| Profile | Recommended starting point |
|---|---|
| **Pre-launch, no customer data** | Secure development practices, MFA, secrets management, access control, protected branches ([`controls/01`](controls/01-access-control.md), [`02`](controls/02-secrets-management.md), [`03`](controls/03-change-management.md), [`policies/secure-development-policy.md`](policies/secure-development-policy.md)) |
| **Live SaaS with customer data** | The above, plus backups with a tested restore, logging, incident response, privacy and vendor management ([`05`](controls/05-backups-and-restore.md), [`06`](controls/06-logging-and-monitoring.md), [`09`](controls/09-incident-response.md), [`privacy/`](privacy/), [`07`](controls/07-vendor-management.md)) |
| **Growing B2B SaaS** | The above, plus regular evidence collection, vulnerability management, a risk register and customer due diligence ([`11`](controls/11-vulnerability-management.md), [`12`](controls/12-risk-and-governance.md), [`audit/`](audit/), [`checklists/before-investor-data-room.md`](checklists/before-investor-data-room.md)) |
| **Enterprise-focused SaaS** | The above, plus mapping each customer requirement to your controls and a decision about formal assurance ([`controls/framework-mappings.md`](controls/framework-mappings.md), [`guide/paths/`](guide/paths/)) |
| **Legacy production environment** | Baseline security first, then a separate, carefully controlled migration with a tested restore before anything moves ([`runbooks/restore-test.md`](runbooks/restore-test.md), [`skills/production-migration/`](skills/production-migration/)) |

## Then

Follow the end-to-end workflow in [`workflow/README.md`](workflow/README.md): scope, find gaps, prioritise risk, implement, collect evidence, check completeness, review effectiveness, prepare for due diligence, decide on formal assurance.

Read [`guide/layers-and-outcomes.md`](guide/layers-and-outcomes.md) early: this kit mostly helps with technical security, and passing it does not make you compliant with any framework.
