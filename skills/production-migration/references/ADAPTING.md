# Adapting the guide to your project

Expect about five weeks from start to cutover for one developer working on it alongside other duties (the lean path is shorter). Replace the values below in the prompts before you run them.

| Variable | What to put |
| --- | --- |
| COMPANY, SECTOR, TEAM SIZE | Your own |
| WORKLOAD | What the product is, for example a web application with an API, a database, file uploads and background jobs |
| CURRENT HOSTING | What you run today |
| STARTING POINT | Single VM, platform-as-a-service, or existing cloud account with unmanaged resources |
| CLOUD PROVIDER | Where the target setup will live (see docs/provider-mapping.md) |
| TARGET STACK | Compute, database, storage and edge provider |
| DB FAMILY | MySQL family or PostgreSQL, with the production version |
| TARGET DB ENGINE | Same engine and version as production at minimum |
| RUNTIME IMAGE | The version production actually runs, not the one the docs claim |
| CI SYSTEM | Your pipeline provider, for example GitHub Actions or GitLab CI |
| PATH | Lean or full (see README) |
| DEMO IN SCOPE | Yes or no; full path usually yes |
| COMPLIANCE TARGETS | Frameworks your customers will ask about |
| CONSTRAINTS | Account limits, credits, team size, deadline |
| NONPROD PROFILE, PROD PROFILE, PROD ROLE, NONPROD ROLE | CLI profile and identity names you choose; non-production is the default |
| VERIFICATION LIST | The user journeys that must pass from outside after cutover: sign in, your core transaction, each API or partner integration, an email send |
| ENDPOINTS TO KEEP | Public endpoints that must keep working through cutover |
| ALERT EMAIL | A shared mailbox, not one person |
| PROD INSTANCE NAME | The production host or app as named at your provider |
| AGENT INSTRUCTIONS FILE | AGENTS.md by default; CLAUDE.md can point to it |

## Decisions to make before Phase 0 ends

Record each in the plan's decision log with the event that would make you revisit it (see [docs/examples/example-decision-log.md](docs/examples/example-decision-log.md)).

- Managed database service, chosen by the Phase 0 compatibility check rather than preference.
- One account with role separation, or one account or project per environment. Separate accounts are cleaner if your account type allows them.
- Lean or full path, and whether you need a demo environment.
- Which hostname users will see after cutover, and whether the old one stays as a redirect.
- Who owns each external account (edge provider, payments, email, source control), and a second administrator for each.
- The rollback decision owner and the rollback deadline.

## Other providers

The prompts use capability terms (managed database, write-once audit storage, audit logging). [docs/provider-mapping.md](docs/provider-mapping.md) maps them to specific services. Where a provider lacks a capability, the mapping says what to compensate with. The phases, exit criteria, environment separation, scratch restore, hosts-file verification and 14-day soak are provider independent.
