# B2. Backup, then inventory

Run in: a coding agent. Phase 0, step 1. Read-only on the live system.

```text
Phase 0, step 1. Follow the starting-point note in infra/guide/docs/variants for <STARTING POINT>. Before any other action, take a backup of the production system (for a VM, a provider snapshot of <PROD INSTANCE NAME>; for a platform, a database backup plus an export of the configuration), record its name and id in infra/evidence/snapshot.md, then enable daily automatic backups. Next, using read-only commands, inventory the live system into infra/inventory/host-inventory.md: web server virtual hosts and rewrite rules; every public hostname and its target; runtime and database versions and loaded extensions; scheduled jobs; how every background process starts and whether it survives a reboot; every .env or config file holding credentials (paths and key names only, never values); TLS configuration and who issues the certificates; any dependency on vendor-specific paths; the git remote and branch the deployed code tracks, and whether the code sits inside the publicly served directory. Write every resource in the cloud account (instances, databases, buckets, load balancers, keys, identities) to infra/inventory/cloud-resources.md, with owner, purpose and environment where known, and flag any that the plan does not mention. Write every external system that holds a callback URL, allowlisted IP or credential (payments, email, identity, integrations, DNS and edge provider) to infra/inventory/external-systems.md, with the account that owns each. Make no change to the live system. Finish by writing infra/inventory/differences-from-plan.md listing every place where reality differs from PLAN.md.
```

After this run, update the plan wherever the inventory contradicted it, then continue. See [docs/examples/example-inventory.md](../docs/examples/example-inventory.md) for the expected shape.

Next: [B3. Access control, logging and encryption](B3-access-logging-encryption.md)
