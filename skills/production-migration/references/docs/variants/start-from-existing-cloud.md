# Starting point: an existing cloud account with unmanaged resources

The product already runs in a cloud account, but resources grew by accident: instances nobody owns, shared credentials, no consistent tagging.

## Phase 0 emphasis

- **Discover everything first.** List every instance, database, bucket, load balancer, key and identity in every region you use. Write it to `infra/inventory/cloud-resources.md` with the owner, purpose, environment and monthly cost of each, and flag anything the plan does not mention.
- **Assign an owner or a retirement date** to every resource. Unowned resources are both a cost and an attack surface.
- **Identity review:** list users, roles and long-lived keys. Remove keys that are unused, require MFA for humans, and replace shared credentials with per-environment identities.
- **Tag as you go:** adopt the environment and stage tags from the guide and apply them to existing resources before building new ones, so the cross-environment deny policies have something to act on.
- **Billing and ownership:** confirm who owns the account, the billing arrangement and any credits, and whether account structure limits what you can create (for example you may be a member of a reseller organisation and unable to create separate accounts).
- **Decide separation deliberately:** separate accounts per environment where allowed, otherwise one account with role separation and deny policies. Record the decision and the trigger to revisit it.

## Then follow the single-VM path

Once the account is understood, the remaining phases are the same. Do not delete discovered resources during the migration unless they are clearly yours and backed up; retire them in Phase 4.
