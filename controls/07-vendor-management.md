# 7. Vendor management

| | |
|---|---|
| **Control ID** | KIT-VND-01 |
| **Evidence number** | 07 (the `control=` value in evidence headers) |
| **Applies to** | Every third party that receives company or customer data, including free tools |
| **Owner (role)** | Vendor owner per vendor; the privacy contact for processors |
| **Review frequency** | Every 365 days or sooner (yearly); the audit flags evidence older than 365 days |
| **Limitations** | A register and agreements do not show a vendor is secure; a vendor's certificate is not your control |

**Objective:** You know every third party that touches your data, what they hold, what contract covers it, and when you last checked them.

## What to do

- List every vendor and sub-processor: what they do, what data they receive, where it is stored, and the contract or data-processing agreement in force.
- Classify each by the data they hold. Review the critical ones at least yearly, using their security reports or certifications.
- Record how you would leave each vendor: export path, time, cost.
- Keep API credentials for each vendor in the secrets register with an owner and expiry.
- Tell customers who your sub-processors are, if you process their personal data.

## Why a reviewer asks

Reviewers ask for the vendor list and for the data-processing agreement of anyone who handles personal data.

## Done when

- [ ] A vendor register exists and covers every service that receives company or customer data.
- [ ] Each vendor that processes personal data has a signed data-processing agreement on file.
- [ ] Critical vendors have a dated review in the last twelve months.
- [ ] An exit note exists for the vendors you could not replace in a week.

## Evidence to keep

- The vendor register ([`evidence/vendor-register.md`](../evidence/vendor-register.md)).
- Signed agreements.
- Review notes.
- Exit notes.

### Kinds of evidence

- **Configuration:** The vendor register
- **Operational:** Signed agreements and dated reviews
- **Effectiveness:** A test of an exit path for one critical vendor (export and import)
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- Forgetting free tools: analytics, error trackers, AI services, support widgets.
- No agreement with a processor that sees personal data.
- Treating a vendor's badge as your own control.
- No exit path for the one vendor everything depends on.

## Indicative framework references

SOC 2 CC9.2 · ISO 27001:2022 A.5.19, A.5.20, A.5.21, A.5.22 · GDPR Art. 28, 30 · DORA Art. 28, 30

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

This control is a register, a plan or a review rather than a cloud setting, so there is no cloud command. Check the evidence files named above. Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../evidence/vendor-register.md`](../evidence/vendor-register.md)
