# Control-to-evidence map

What evidence supports each control, which template to start from, how fresh `kit-audit` expects it to be, and which requirements it is indicatively relevant to. The framework column is **indicative**: relevant to, not sufficient for.

| Control | Evidence to hold | Template | Freshness limit in the audit | Indicative references |
|---|---|---|---|---|
| 01 Access control | Access list, MFA setting, access review, offboarding record | [`access-review.md`](../evidence/access-review.md) | 100 days | SOC 2 CC6.1-6.3; ISO A.5.15, A.5.18, A.8.2, A.8.5 |
| 02 Secrets management | Secrets register, secret-scan run, a rotation record | [`evidence-file.md`](../evidence/evidence-file.md) | 365 days | SOC 2 CC6.1, CC6.7; ISO A.5.17, A.8.24 |
| 03 Change management | Branch-rule export, five sampled changes, deploy log | [`evidence-file.md`](../evidence/evidence-file.md) | 100 days | SOC 2 CC8.1; ISO A.8.32, A.8.31 |
| 04 Environment separation | Environment diagram, database grants, port scan | [`evidence-file.md`](../evidence/evidence-file.md) | 365 days | SOC 2 CC6.6, CC8.1; ISO A.8.31, A.8.33 |
| 05 Backups and tested restores | Backup configuration, restore-test report, RTO and RPO | [`restore-test-report.md`](../evidence/restore-test-report.md) | 100 days | SOC 2 A1.2, A1.3; ISO A.8.13, A.8.14, A.5.30 |
| 06 Logging and monitoring | Logging config, alert list with recipients, test alert | [`evidence-file.md`](../evidence/evidence-file.md) | 365 days | SOC 2 CC7.1, CC7.2; ISO A.8.15, A.8.16 |
| 07 Vendor management | Vendor register, signed agreements, vendor reviews | [`vendor-register.md`](../evidence/vendor-register.md) | 365 days | SOC 2 CC9.2; ISO A.5.19-5.22; GDPR Art. 28 |
| 08 Data protection (GDPR) | Data inventory, record of processing, deletion rehearsal, transfers, DPIA screening, privacy notice | [`privacy/`](../privacy/) | 365 days | GDPR Art. 5, 6, 25, 28, 30, 32, 35, Ch. V |
| 09 Incident response | Plan, incident register, reports, tabletop record | [`incident-register.md`](../evidence/incident-register.md), [`incident-report.md`](../evidence/incident-report.md) | 365 days | SOC 2 CC7.3-7.5; ISO A.5.24-5.28; GDPR Art. 33, 34 |
| 10 Supply chain and signing | Signature verification and negative test, scan reports, digest-to-PR trace | [`evidence-file.md`](../evidence/evidence-file.md) | 100 days | SOC 2 CC7.1, CC8.1; ISO A.8.8, A.8.25, A.8.28 |
| 11 Vulnerability management | Scan reports, remediation policy, exceptions, five-finding sample | [`evidence-file.md`](../evidence/evidence-file.md) | 100 days | SOC 2 CC7.1; ISO A.8.8, A.8.9 |
| 12 Risk and governance | Roles, policies, risk register, training, management review, scoping answers | [`risk-register.md`](../evidence/risk-register.md), [`policies/`](../policies/), [`questionnaire.md`](../scoping/questionnaire.md) | 365 days | SOC 2 CC1, CC3, CC5.3; ISO clauses 4-10, A.5.1-5.4, A.6; GDPR Art. 24 |

The framework column is a summary. The authoritative mapping records, with their sources, coverage statuses and review labels, are in [`mappings.json`](mappings.json) and the generated [`framework-mappings.md`](framework-mappings.md); where the two differ, the records govern. Freshness limits are defaults in `audit/kit-audit.py`. Change them to fit your risk. Evidence of effectiveness (that the control actually works) comes from testing and review by people; the audit checks completeness and freshness only. See [`../audit/README.md`](../audit/README.md).
