# Encryption and key management

<!-- kit-evidence: control=12 date=YYYY-MM-DD result=pass type=operational -->

**Owner:** <role> **Approved by:** <role> **Version:** <1.0> **Date:** <YYYY-MM-DD> **Review by:** <YYYY-MM-DD>

What is encrypted, how, and how keys are looked after.

Keep it to one page. Write what you actually do, then do it.

## Policy

1. In transit: TLS everywhere, including between internal services where they cross a network. Current protocol versions only.
2. At rest: databases, object storage, backups and disks encrypted with provider-managed or customer-managed keys.
3. Keys: held in a managed key service, never in code or on disk in the clear; separate keys per environment; access limited and logged.
4. Rotation: schedule per key, and on suspected exposure; rotation tested once.
5. Recovery: the loss of a key must not mean the loss of all data; document how backups are decrypted.
6. Passwords: stored only as salted hashes from a current, slow algorithm.

## Acknowledgement

People with access confirm in writing (name or role, date) that they have read it.
