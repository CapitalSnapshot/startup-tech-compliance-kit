# Business continuity and disaster recovery

<!-- kit-evidence: control=12 date=YYYY-MM-DD result=pass type=operational -->

**Owner:** <role> **Approved by:** <role> **Version:** <1.0> **Date:** <YYYY-MM-DD> **Review by:** <YYYY-MM-DD>

How you keep running, and how you come back, after a serious disruption.

Keep it to one page. Write what you actually do, then do it.

## Policy

1. Critical services and the order to restore them.
2. Recovery time objective (RTO) and recovery point objective (RPO) for each, **from measured restore tests** ([`../runbooks/restore-test.md`](../runbooks/restore-test.md)).
3. Scenarios: loss of the host or region, loss of the database, loss of the cloud account, loss of a key person, a vendor outage.
4. Roles, contacts and the communication plan, including customers.
5. Rebuild path: [`../runbooks/rebuild-from-nothing.md`](../runbooks/rebuild-from-nothing.md).
6. Test: at least yearly, with a dated record and the lessons applied.

## Acknowledgement

People with access confirm in writing (name or role, date) that they have read it.
