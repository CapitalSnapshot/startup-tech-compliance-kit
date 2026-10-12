# Provider mapping

The prompts name capabilities. This table maps them to common services. Service names and coverage change; check your provider's current documentation before relying on a row. "Compensate" means the provider has no direct equivalent, so add the control yourself.

| Capability | AWS | Google Cloud | Azure | Smaller providers (for example Hetzner, DigitalOcean) |
| --- | --- | --- | --- | --- |
| Per-environment identities with MFA | IAM roles assumed with MFA; CLI user that can only assume them | Separate projects; service accounts and IAM with 2-step verification | Separate subscriptions or resource groups; Entra roles with MFA, privileged access management | Separate projects or teams per environment; 2FA on every member; API tokens scoped per project |
| Environment boundary | Separate accounts (preferred) or tags plus explicit deny policies | Separate projects (preferred), with organisation policy | Separate subscriptions (preferred) or resource groups with RBAC | Separate projects; nothing finer-grained, so keep production tokens off the laptop default |
| Control-plane audit logging | Multi-region trail with log file validation | Cloud Audit Logs (admin activity and data access) with a log sink | Activity Log with diagnostic settings to a storage account | Use the provider activity or audit log where one exists; coverage is thinner, so compensate by recording every agent command in the evidence folder |
| Threat detection | GuardDuty | Security Command Center | Defender for Cloud | Compensate: host intrusion detection and audit tooling, login alerts |
| Customer-managed encryption keys | KMS customer-managed keys | Cloud KMS (CMEK) | Key Vault keys | Provider-managed disk and database encryption; application-level encryption for the most sensitive fields |
| Write-once audit storage | Object storage with Object Lock in compliance mode | Bucket with retention policy and lock | Immutable blob storage | S3-compatible storage with object lock where supported (verify), otherwise ship logs to a separate account you control |
| Managed database, private only | Managed relational database in private subnets, no public access | Cloud SQL with private IP | Managed database with private endpoint | Managed database restricted to a private network or trusted sources; if none, self-manage on a private network with tested backups |
| Private connectivity, app to database | Same VPC, or peering when the host sits outside the database network | Private services access | Private endpoint or VNet integration | Private network (VPC) membership |
| Object storage | S3 | Cloud Storage | Blob Storage | Provider object storage (S3-compatible) |
| Load balancer with managed certificate | Application load balancer with ACM | Cloud load balancing with managed certificates | Application Gateway or Front Door | Provider load balancer with Let's Encrypt certificates |
| Secrets | Secrets Manager | Secret Manager | Key Vault secrets | CI environment secrets; a self-hosted secrets manager if you need rotation |
| Alarms on security events | CloudWatch alarms and notifications | Cloud Monitoring alerting | Azure Monitor alerts | Provider monitoring alerts plus an external uptime and log-alert service |
| Backups and snapshots | Automated backups, snapshots, point-in-time recovery | Automated backups, point-in-time recovery | Automated backups, point-in-time restore | Provider snapshots; test restores more often because features are thinner |

## When the app host sits outside the database network

Some platforms run simple virtual servers outside the private network where managed databases live. Then you need explicit private connectivity (peering or a private endpoint) and a test that the host can reach a throwaway database. If your host and database share a private network already, record that and skip the peering step in B4.
