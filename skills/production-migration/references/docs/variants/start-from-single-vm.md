# Starting point: a single virtual machine

The default assumption of the guide: one hand-built host runs the web server, application, database and background jobs.

## Phase 0 notes

- **Backup first:** take a provider snapshot of the instance before anything else and record it. Then enable automatic daily snapshots.
- **Inventory by SSH, read-only:** web server virtual hosts and rewrite rules, every public hostname, runtime and database versions, loaded extensions, cron entries for all users, how each background process starts and whether it survives a reboot, credential files (paths and key names only), TLS issuer, vendor-specific paths in code, and the git remote and branch the checkout tracks.
- **Check where the checkout sits:** a repository inside the web root can be served publicly. If you find that, contain it with a web server deny rule the same day and plan its removal from the served tree at cutover.
- **Check the checkout's remote:** confirm it tracks the repository your migration work lives in before you deploy from it.
- **Do not change the host:** no firewall, SSH or configuration changes until it is decommissioned.

## Cutover notes

Keep the old host running but not serving after the DNS switch. Use a maintenance page at the web server if you hold a no-firewall-changes rule, the firewall otherwise.
