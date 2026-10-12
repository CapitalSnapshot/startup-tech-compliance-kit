# Evidence: backup configuration , 2026-09-20

<!-- kit-evidence: control=05 date=2026-09-20 result=pass type=config -->

**Control:** KIT-BKP-01 (05 Backups and tested restores) **Done by:** platform owner **Reviewed by:** founder **Date and time (UTC):** 2026-09-20 09:10

## What was done

Exported the backup settings for the production database and the file storage bucket (invented values, for illustration).

## How it was checked

Commands from `verify/aws.md`, section 05. Output saved with account identifiers replaced by `REDACTED`.

| Check | Expected | Result |
|---|---|---|
| Database automated backups | 14 days or more | 14 days |
| Database storage encrypted | true | true |
| Storage bucket versioning | Enabled | Enabled |
| Disk snapshots | Daily, encrypted | Daily, encrypted |

## Result

**Pass.** This shows the backup policy exists. It does not show a restore works: see the restore-test report.

## Links

Raw output (kept in the controlled evidence store, hash below): `sha256 3f1a...e9c2`
