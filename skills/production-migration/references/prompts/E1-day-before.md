# E1. The day before cutover

Run in: a coding agent, with you sitting beside it. Phase 3. Every command against production is shown and confirmed. Choose a quiet window and announce it to users and partners about a week ahead.

```text
Phase 3, day before. Use the production profile, show each command and wait for my yes. Create the production managed database (35 day backups where supported, point-in-time recovery, its own encryption key), the production host one size up from current, a static IP and a load balancer with a managed certificate covering every hostname in the inventory (validation records created DNS-only at the edge provider), and attach the host. Deploy the release tag that has soaked. Run the initial full file sync from the old system to the production bucket. Verify the whole stack through a hosts-file override on my laptop against everything on <VERIFICATION LIST>. Do not touch DNS. Record what was created, with ids, in infra/evidence/prod-build.md.
```

Next: [E2. Cutover](E2-cutover.md)
