# Starting point: a platform-as-a-service

You deploy to a managed platform (for example a Heroku-style or container platform) and are moving to infrastructure you control, or consolidating onto a different provider.

## Differences from the single-VM path

- **There is no host to snapshot.** In Phase 0, take a database backup and export the platform configuration instead, and record both in `infra/evidence/snapshot.md`.
- **There is no SSH inventory.** Inventory what the platform holds: configuration variables (names only, never values), add-ons and their plans, scheduled jobs, release or build commands, buildpacks or base images, process types and scale, domains and certificates, and log drains. Write it to `infra/inventory/host-inventory.md`.
- **Hidden dependencies:** platforms provide things you may not have noticed: routing, TLS, an ephemeral filesystem, environment injection, add-on credentials. List each and decide how the target replaces it.
- **Containers may already exist.** If the app already builds a container image, Phase 1 shrinks to the pipeline, deploy and provisioning work.
- **Data move:** use the platform's backup or export tooling for the final dump. Time the export and import in Phase 2.
- **Cutover:** switch DNS or the platform's domain to the new load balancer. Keep the old app running, scaled down but not serving, until the 14-day soak ends.
- **Cost:** account for the old platform bill during the soak.

## Prompt adjustments

Where a prompt says "SSH to the old host", read "the platform's CLI or dashboard export". Where it says "snapshot the host", read "back up the database and export the configuration".
