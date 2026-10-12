# B3. Access control, logging and encryption

Run in: a coding agent. Phase 0, step 2. Use infra/guide/docs/provider-mapping.md for the service names on your provider.

```text
Phase 0, step 2. On <CLOUD PROVIDER>, using the provider mapping, create two least-privilege admin identities with MFA, <PROD ROLE> and <NONPROD ROLE>, and a CLI identity that can only assume them. Record them in infra/evidence/identities.md. Make each identity unable to touch the other environment's resources (separate accounts or projects where my account type allows it, otherwise deny policies keyed on an env tag), deny creating any resource without an env tag, and add a policy on every production storage bucket that denies the non-production identity. Remove every other long-lived access key and confirm MFA on the root or owner account. Enable control-plane audit logging that is tamper evident, threat detection where the provider has it, customer-managed encryption keys for the database, secrets and audit storage where the provider supports it, and write-once audit storage. Where the provider lacks a capability, say so and propose the compensating control from the mapping instead of skipping it. Add alarms for root or owner login, console login without MFA, policy changes, key deletion and audit logging changes, sent to <ALERT EMAIL>. Set a budget alarm. Record what you enabled in infra/evidence/logging.md. Prove the deny works by attempting a production action from the non-production identity and save the refusal in infra/evidence/deny-proof.md. Show every command first.
```

Next: [B4. Database compatibility and private connectivity](B4-database-compat-connectivity.md)
