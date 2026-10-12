# Environments

A small, defensible layout for a team of one to ten.

| Environment | Purpose | Data | Who can change it |
|---|---|---|---|
| **dev** | Integration. Deploys itself from the main development branch. | Generated only | Developers, through the pipeline |
| **demo** | Optional. Sales demos and the soak (a period of running a release before it goes to production). | Generated only, seeded by a script | Developers, through the pipeline |
| **production** | Customers. | Real | A named few, with a second pair of eyes for every step |

## Rules

1. **Separate everything**: accounts or at least roles, networks, databases, secrets and credentials.
2. **Production data never leaves production.** Dev and demo are seeded from a generator.
3. **One artefact.** The pipeline builds once; dev, demo and production run the same signed artefact, referenced by digest. See [`pipeline.md`](pipeline.md).
4. **Soak before production.** A release runs on demo for a stated period (for example two days) with no errors before it is promoted. Promoting during a soak restarts the clock.
5. **Production changes need an explicit approval** in writing for every step that changes it, and read-only access otherwise.
6. **Nothing is edited on a host by hand.** If a host needs a change, change the repository and redeploy.

## What each environment needs

- A secrets manager entry per secret, per environment ([`../controls/02-secrets-management.md`](../controls/02-secrets-management.md)).
- A database with separate users for the application and for migrations ([`../controls/04-environment-separation.md`](../controls/04-environment-separation.md)).
- A status record for each deploy: which digest, when, result.
- Backups and a tested restore for production ([`../controls/05-backups-and-restore.md`](../controls/05-backups-and-restore.md)).
