# Example decision log (fictional)

Keep this in the plan. Each decision names the alternatives you rejected and the event that would make you revisit it.

| Date | Decision | Reason | Alternatives rejected | Revisit when |
| --- | --- | --- | --- | --- |
| Day 2 | Managed database, same engine family, version not below production | Compatibility check found no engine-specific syntax that is costly to change | Switch engine family; self-managed database in a container | A major version upgrade is due, or restore time exceeds the window |
| Day 2 | One account with role separation | Account type cannot create more accounts | Separate accounts per environment | Credits expire or live bank data arrives |
| Day 3 | Keep the existing edge provider | It already handles DNS, TLS and WAF | Move DNS to the cloud provider | The edge account owner changes or costs rise |
| Day 4 | Build images on the runtime version production runs | A different version would change behaviour | Upgrade the runtime during the migration | After cutover, as a separate change |
| Day 5 | Lean path, no demo environment | No external demos planned this quarter | Full path with demo | A partner asks for a sandbox |
| Day 6 | Rollback owner is the CTO; deadline is 2 hours after DNS switch | One accountable person; after that forward-fix only | Shared decision | Team grows beyond two engineers |
