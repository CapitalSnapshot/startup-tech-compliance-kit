# Skills

## production-migration

A Claude skill and prompt pack for moving a product off a single legacy host, a platform-as-a-service or an unmanaged cloud account onto separate dev, demo and production environments with a pipeline, a managed database and controls that produce evidence for later review. It works one action at a time, with written exit criteria and named evidence files at each phase.

**To use it:** copy the `production-migration` folder into your Claude skills directory (for example `~/.claude/skills/`), then ask your coding agent to plan a production migration. Read every command before approving it; run against non-production first.

It pairs with the rest of this kit: the skill does the migration; [`../controls/`](../controls/), [`../runbooks/`](../runbooks/) and [`../evidence/`](../evidence/) say what good looks like and how to prove it.

Licensed under the Apache License, Version 2.0, like everything here. See `production-migration/references/README.md` for its own contents and limitations.
