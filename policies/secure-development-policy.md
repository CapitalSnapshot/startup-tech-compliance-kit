# Secure development policy

<!-- kit-evidence: control=12 date=YYYY-MM-DD result=pass type=operational -->

**Owner:** <role> **Approved by:** <role> **Version:** <1.0> **Date:** <YYYY-MM-DD> **Review by:** <YYYY-MM-DD>

How code is written, reviewed, built and released.

Keep it to one page. Write what you actually do, then do it.

## Policy

1. Every change through a reviewed pull request and the pipeline ([`../controls/03-change-management.md`](../controls/03-change-management.md)).
2. Secret and dependency scanning on every change; signed builds verified on the host ([`../controls/10-supply-chain-and-signing.md`](../controls/10-supply-chain-and-signing.md)).
3. Input validation, parameterised queries, authorisation checks on every data endpoint, least-privilege service accounts.
4. No production data in development; generated or scrubbed data only.
5. Security review for changes to authentication, authorisation, payments, or personal data ([`../privacy/privacy-by-design-review.md`](../privacy/privacy-by-design-review.md)).
6. Vulnerabilities handled per [`../controls/11-vulnerability-management.md`](../controls/11-vulnerability-management.md).

## Acknowledgement

People with access confirm in writing (name or role, date) that they have read it.
