# Verify: Google Cloud

Read-only commands that produce evidence for each control on Google Cloud. Run them, save the output as a dated evidence file ([`../evidence/evidence-file.md`](../evidence/evidence-file.md)), and the audit will track its freshness.

> **Every command in this file is UNTESTED.** They were written from the provider's documentation and have not been run. Check each one against the current CLI before relying on it, and send a pull request to correct or mark any you have tested.

Rules for every command here: **read-only**, no secret values printed, placeholders in CAPITALS to replace with your own, and a `Status` line saying how far it has been checked. Redact account identifiers before sharing output ([`../evidence/handling.md`](../evidence/handling.md)).

Status values: `TESTED on <date>` (run against a real account, output shape confirmed) · `RAN, NO DATA on <date>` (ran without error but the account had nothing of that kind to show) · `UNTESTED` · `NOT APPLICABLE`.

## 01 Access control

### 01.1 Who has broad roles on the project

**Status:** UNTESTED

```bash
gcloud projects get-iam-policy PROJECT_ID --format=json
```

**Good looks like:** Few members with `roles/owner` or `roles/editor`; groups and service accounts, not personal accounts, where possible.

### 01.2 2-Step Verification enforcement

**Status:** UNTESTED

```bash
(no gcloud command: check Cloud Identity or Workspace admin console, Security, 2-Step Verification, and save a dated screenshot)
```

**Good looks like:** Enforcement is on for all users, not just allowed.

## 02 Secrets management

### 02.1 Secret names, rotation and age (never reads a value)

**Status:** UNTESTED

```bash
gcloud secrets list --format='table(name,createTime,rotation.nextRotationTime)'
```

**Good looks like:** Every secret is listed with an owner you can name. Do **not** run `versions access` to produce evidence.

## 03 Change management

**Status:** NOT APPLICABLE

Change management is enforced at the code host: see [`common.md`](common.md).

## 04 Environment separation

### 04.1 Firewall rules open to the internet

**Status:** UNTESTED

```bash
gcloud compute firewall-rules list --filter='sourceRanges:0.0.0.0/0' --format='table(name,direction,allowed[].map().firewall_rule().list())'
```

**Good looks like:** Only rules you intend to be public. Database and admin ports never appear.

### 04.2 Database: public IP and backups

**Status:** UNTESTED

```bash
gcloud sql instances list --format='table(name,settings.ipConfiguration.ipv4Enabled,settings.backupConfiguration.enabled)'
```

**Good looks like:** Public IP disabled and backups enabled for production.

## 05 Backups and tested restores

### 05.1 Backups and point-in-time recovery

**Status:** UNTESTED

```bash
gcloud sql instances describe INSTANCE --format='value(settings.backupConfiguration.enabled,settings.backupConfiguration.pointInTimeRecoveryEnabled)'
```

**Good looks like:** Both true for production.

### 05.2 Recent backups exist

**Status:** UNTESTED

```bash
gcloud sql backups list --instance INSTANCE --limit 5
```

**Good looks like:** Backups within the last day.

## 06 Logging and monitoring

### 06.1 Log sinks and audit configuration

**Status:** UNTESTED

```bash
gcloud logging sinks list && gcloud projects get-iam-policy PROJECT_ID --format='json(auditConfigs)'
```

**Good looks like:** A sink to a store the application cannot edit, and data-access audit logs enabled for the services that hold sensitive data.

## 07 Vendor management

**Status:** NOT APPLICABLE

Vendor management is a register and a review, not a cloud setting. See [`../controls/07-vendor-management.md`](../controls/07-vendor-management.md).

## 08 Data protection

### 08.1 Bucket blocks public access and uses uniform access

**Status:** UNTESTED

```bash
gcloud storage buckets describe gs://BUCKET --format='value(public_access_prevention,uniform_bucket_level_access)'
```

**Good looks like:** `enforced` and `True` for buckets holding personal data.

## 09 Incident response

**Status:** NOT APPLICABLE

Incident response is a plan and a record, not a cloud setting. See [`../controls/09-incident-response.md`](../controls/09-incident-response.md).

## 10 Supply chain and signing

### 10.1 Registry repositories

**Status:** UNTESTED

```bash
gcloud artifacts repositories list
```

**Good looks like:** Only the repositories you expect, with immutable tags or digest-only promotion.

## 11 Vulnerability management

### 11.1 Vulnerability scanning for images

**Status:** UNTESTED

```bash
(enable and review Artifact Analysis, then export findings: `gcloud artifacts docker images list --show-occurrences IMAGE_PATH`)
```

**Good looks like:** Findings are present and triaged; unfixed ones have exceptions in the risk register.

## 12 Risk and governance

**Status:** NOT APPLICABLE

Risk and governance is people and paperwork, not a cloud setting. See [`../controls/12-risk-and-governance.md`](../controls/12-risk-and-governance.md).

