# Verify: Microsoft Azure

Read-only commands that produce evidence for each control on Microsoft Azure. Run them, save the output as a dated evidence file ([`../evidence/evidence-file.md`](../evidence/evidence-file.md)), and the audit will track its freshness.

> **Every command in this file is UNTESTED.** They were written from the provider's documentation and have not been run. Check each one against the current CLI before relying on it, and send a pull request to correct or mark any you have tested.

Rules for every command here: **read-only**, no secret values printed, placeholders in CAPITALS to replace with your own, and a `Status` line saying how far it has been checked. Redact account identifiers before sharing output ([`../evidence/handling.md`](../evidence/handling.md)).

Status values: `TESTED on <date>` (run against a real account, output shape confirmed) · `RAN, NO DATA on <date>` (ran without error but the account had nothing of that kind to show) · `UNTESTED` · `NOT APPLICABLE`.

## 01 Access control

### 01.1 Who holds Owner

**Status:** UNTESTED

```bash
az role assignment list --all --query "[?roleDefinitionName=='Owner'].{who:principalName,scope:scope}"
```

**Good looks like:** Few owners, and not personal accounts where groups can be used.

### 01.2 MFA enforcement

**Status:** UNTESTED

```bash
(no az command: check Microsoft Entra admin centre, Protection, Conditional Access, and save a dated screenshot)
```

**Good looks like:** A policy requiring MFA for all users, with no broad exclusions.

## 02 Secrets management

### 02.1 Key Vault secrets: names and expiry (never reads a value)

**Status:** UNTESTED

```bash
az keyvault secret list --vault-name VAULT --query '[].{name:name,expires:attributes.expires}'
```

**Good looks like:** Every secret has an owner and, where possible, an expiry. Do **not** run `secret show` to produce evidence.

## 03 Change management

**Status:** NOT APPLICABLE

Change management is enforced at the code host: see [`common.md`](common.md).

## 04 Environment separation

### 04.1 Network rules open to any source

**Status:** UNTESTED

```bash
az network nsg list --query "[].{nsg:name,open:securityRules[?sourceAddressPrefix=='*'].name}"
```

**Good looks like:** Only rules you intend to be public. Database and admin ports never appear.

### 04.2 SQL server public access

**Status:** UNTESTED

```bash
az sql server list --query '[].{name:name,public:publicNetworkAccess}'
```

**Good looks like:** `Disabled` for production.

## 05 Backups and tested restores

### 05.1 Backup vaults

**Status:** UNTESTED

```bash
az backup vault list --query '[].{name:name,location:location}'
```

**Good looks like:** A vault for each protected workload.

### 05.2 SQL long-term retention

**Status:** UNTESTED

```bash
az sql db long-term-retention-policy show --server SERVER --database DB --resource-group RG
```

**Good looks like:** A retention period that matches your policy.

## 06 Logging and monitoring

### 06.1 Diagnostic settings send logs somewhere durable

**Status:** UNTESTED

```bash
az monitor diagnostic-settings list --resource RESOURCE_ID
```

**Good looks like:** A setting that sends logs to a workspace or store the application cannot edit.

### 06.2 Activity log alerts

**Status:** UNTESTED

```bash
az monitor activity-log alert list --query '[].{name:name,enabled:enabled}'
```

**Good looks like:** Alerts exist for administrative changes and are enabled.

## 07 Vendor management

**Status:** NOT APPLICABLE

Vendor management is a register and a review, not a cloud setting. See [`../controls/07-vendor-management.md`](../controls/07-vendor-management.md).

## 08 Data protection

### 08.1 Storage account blocks public blob access and requires HTTPS

**Status:** UNTESTED

```bash
az storage account show --name ACCOUNT --query '{publicBlob:allowBlobPublicAccess,https:enableHttpsTrafficOnly}'
```

**Good looks like:** `publicBlob` false and `https` true for accounts holding personal data.

## 09 Incident response

**Status:** NOT APPLICABLE

Incident response is a plan and a record, not a cloud setting. See [`../controls/09-incident-response.md`](../controls/09-incident-response.md).

## 10 Supply chain and signing

### 10.1 Registry settings

**Status:** UNTESTED

```bash
az acr list --query '[].{name:name,adminEnabled:adminUserEnabled}'
```

**Good looks like:** The admin user disabled; promote by digest.

## 11 Vulnerability management

### 11.1 Defender for Cloud / vulnerability assessment status

**Status:** UNTESTED

```bash
(review Microsoft Defender for Cloud recommendations and export them; there is no single stable read-only command)
```

**Good looks like:** Findings are present and triaged; unfixed ones have exceptions in the risk register.

## 12 Risk and governance

**Status:** NOT APPLICABLE

Risk and governance is people and paperwork, not a cloud setting. See [`../controls/12-risk-and-governance.md`](../controls/12-risk-and-governance.md).

