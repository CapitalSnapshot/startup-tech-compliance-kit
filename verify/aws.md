# Verify: AWS

Read-only commands that produce evidence for each control on AWS. Run them, save the output as a dated evidence file ([`../evidence/evidence-file.md`](../evidence/evidence-file.md)), and the audit will track its freshness.

Commands were run read-only against a real AWS account on the dates shown. Where a status says `UNTESTED` it has not been run yet.

Rules for every command here: **read-only**, no secret values printed, placeholders in CAPITALS to replace with your own, and a `Status` line saying how far it has been checked. Redact account identifiers before sharing output ([`../evidence/handling.md`](../evidence/handling.md)).

Status values: `TESTED on <date>` (run against a real account, output shape confirmed) · `RAN, NO DATA on <date>` (ran without error but the account had nothing of that kind to show) · `UNTESTED` · `NOT APPLICABLE`.

## 01 Access control

### 01.1 Root account MFA and counts of users and MFA devices

**Status:** TESTED on 2026-10-09

```bash
aws iam get-account-summary --query 'SummaryMap.{RootMFA:AccountMFAEnabled,Users:Users,MFADevices:MFADevices}'
```

**Good looks like:** `RootMFA` is 1. `MFADevices` is at least `Users` if people sign in with passwords.

### 01.2 Which users have no MFA device (repeat per user)

**Status:** TESTED on 2026-10-09

```bash
aws iam list-users --query 'Users[].UserName' --output text | tr '\t' '\n' | while read u; do echo "$u $(aws iam list-mfa-devices --user-name "$u" --query 'length(MFADevices)')"; done
```

**Good looks like:** No user prints 0 if they can sign in to the console. Prefer federated sign-in with MFA at the identity provider.

### 01.3 Roles that can be assumed, to confirm production and non-production roles are separate

**Status:** TESTED on 2026-10-09

```bash
aws iam list-roles --query 'Roles[].RoleName'
```

**Good looks like:** Distinct role names for production and non-production, and no shared admin role.

## 02 Secrets management

### 02.1 Secret names, rotation and age (never reads a value)

**Status:** TESTED on 2026-10-09

```bash
aws secretsmanager list-secrets --query 'SecretList[].{Name:Name,Kms:KmsKeyId,Rotation:RotationEnabled,Changed:LastChangedDate}'
```

**Good looks like:** Every secret is listed with an owner you can name, and a key you control. Do **not** run `get-secret-value` to produce evidence.

## 03 Change management

**Status:** NOT APPLICABLE

Change management is enforced at the code host: see [`common.md`](common.md).

## 04 Environment separation

### 04.1 Security groups open to the whole internet

**Status:** RAN, NO DATA on 2026-10-09

```bash
aws ec2 describe-security-groups --filters Name=ip-permission.cidr,Values=0.0.0.0/0 --query 'SecurityGroups[].{Id:GroupId,Name:GroupName}'
```

**Good looks like:** Only groups you intend to be public (for example a web tier on 443). Database and admin ports never appear.

### 04.2 Databases: public or encrypted?

**Status:** TESTED on 2026-10-09

```bash
aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,Public:PubliclyAccessible,Encrypted:StorageEncrypted}'
```

**Good looks like:** `Public` false and `Encrypted` true for every production database.

### 04.3 Which identity you are running as (record it in the evidence)

**Status:** TESTED on 2026-10-09

```bash
aws sts get-caller-identity --query Arn
```

**Good looks like:** The role you meant to use, not a personal user.

## 05 Backups and tested restores

### 05.1 Automated backups on the databases

**Status:** TESTED on 2026-10-09

```bash
aws rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,BackupDays:BackupRetentionPeriod,Encrypted:StorageEncrypted}'
```

**Good looks like:** `BackupDays` is greater than 0 and matches your policy.

### 05.2 Disk snapshots

**Status:** RAN, NO DATA on 2026-10-09

```bash
aws ec2 describe-snapshots --owner-ids self --query 'Snapshots[].{Id:SnapshotId,Started:StartTime,Encrypted:Encrypted}'
```

**Good looks like:** Recent snapshots exist and are encrypted.

### 05.3 Versioning on a storage bucket

**Status:** RAN, NO DATA on 2026-10-09

```bash
aws s3api get-bucket-versioning --bucket BUCKET
```

**Good looks like:** `Status` is `Enabled` for buckets that hold customer data or backups.

## 06 Logging and monitoring

### 06.1 Audit trail on and validated

**Status:** TESTED on 2026-10-09

```bash
aws cloudtrail describe-trails --query 'trailList[].{Name:Name,MultiRegion:IsMultiRegionTrail,Validation:LogFileValidationEnabled}'
```

**Good looks like:** At least one multi-region trail with log file validation enabled.

### 06.2 The trail is actually logging

**Status:** TESTED on 2026-10-09

```bash
aws cloudtrail get-trail-status --name TRAIL_NAME --query '{Logging:IsLogging,LastDelivered:LatestDeliveryTime}'
```

**Good looks like:** `Logging` true and `LastDelivered` recent.

## 07 Vendor management

**Status:** NOT APPLICABLE

Vendor management is a register and a review, not a cloud setting. See [`../controls/07-vendor-management.md`](../controls/07-vendor-management.md).

## 08 Data protection

### 08.1 A bucket blocks public access

**Status:** TESTED on 2026-10-09

```bash
aws s3api get-public-access-block --bucket BUCKET
```

**Good looks like:** All four settings are true for buckets holding personal data.

### 08.2 A bucket is encrypted at rest

**Status:** TESTED on 2026-10-09

```bash
aws s3api get-bucket-encryption --bucket BUCKET --query 'ServerSideEncryptionConfiguration.Rules[].ApplyServerSideEncryptionByDefault'
```

**Good looks like:** An algorithm of `aws:kms` or `AES256` is returned.

## 09 Incident response

**Status:** NOT APPLICABLE

Incident response is a plan and a record, not a cloud setting. See [`../controls/09-incident-response.md`](../controls/09-incident-response.md).

## 10 Supply chain and signing

### 10.1 Container registry: scan on push and immutable tags

**Status:** RAN, NO DATA on 2026-10-09

```bash
aws ecr describe-repositories --query 'repositories[].{Name:repositoryName,ScanOnPush:imageScanningConfiguration.scanOnPush,Tags:imageTagMutability}'
```

**Good looks like:** `ScanOnPush` true and `Tags` `IMMUTABLE` (or you promote only by digest). Skip this if you use another registry.

## 11 Vulnerability management

### 11.1 Vulnerability scanning enabled

**Status:** TESTED on 2026-10-09

```bash
aws inspector2 batch-get-account-status --query 'accounts[].resourceState'
```

**Good looks like:** Scanning is `ENABLED` for the resource types you run. If it is not enabled, record that and how else you scan.

## 12 Risk and governance

**Status:** NOT APPLICABLE

Risk and governance is people and paperwork, not a cloud setting. See [`../controls/12-risk-and-governance.md`](../controls/12-risk-and-governance.md).

