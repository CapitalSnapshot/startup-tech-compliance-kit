# Verify: any provider (code host and signing)

Read-only commands that produce evidence for each control on any provider (code host and signing). Run them, save the output as a dated evidence file ([`../evidence/evidence-file.md`](../evidence/evidence-file.md)), and the audit will track its freshness.

These do not depend on a cloud provider. Statuses show what has been run.

Rules for every command here: **read-only**, no secret values printed, placeholders in CAPITALS to replace with your own, and a `Status` line saying how far it has been checked. Redact account identifiers before sharing output ([`../evidence/handling.md`](../evidence/handling.md)).

Status values: `TESTED on <date>` (run against a real account, output shape confirmed) · `RAN, NO DATA on <date>` (ran without error but the account had nothing of that kind to show) · `UNTESTED` · `NOT APPLICABLE`.

## 03 Change management

### 03.1 Branch rules on the code host (GitHub rulesets, read-only)

**Status:** TESTED on 2026-10-09

```bash
gh api repos/OWNER/REPO/rulesets
```

**Good looks like:** An active ruleset for your production branch; fetch each one with `gh api repos/OWNER/REPO/rulesets/ID` and check it requires a pull request and named status checks, blocks force pushes and deletion, and has no bypass actors. `audit/kit-audit.py --github OWNER/REPO` does this for you.

## 10 Supply chain and signing

### 10.1 Signature on a deployed image (keyless, pinned to your pipeline identity)

**Status:** TESTED on 2026-10-09

```bash
cosign verify --certificate-identity-regexp 'PIPELINE_IDENTITY_REGEX' --certificate-oidc-issuer https://token.actions.githubusercontent.com REGISTRY/IMAGE@sha256:DIGEST
```

**Good looks like:** Exit status 0 and a signature entry. Also run it against an unsigned image: it must fail. Both results are evidence.

