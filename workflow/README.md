# End-to-end workflow

One path through the kit, from "where do we stand?" to "do we need a formal framework?". Each step names what to do, what you produce, and which part of the kit helps. Start with [`../START.md`](../START.md) if you have not.

| # | Step | What to do | You produce | Kit |
|---|---|---|---|---|
| 1 | **Scope the business** | Answer the questionnaire: outcome, product, data, customers, regulation. Mark what applies, what does not, and what is unknown | A dated, completed questionnaire; an applicability list | [`../scoping/`](../scoping/) |
| 2 | **Identify the gaps** | Compare your actual environment and practices with the twelve controls, one by one, and write the gap | A completed gap assessment | [`../scoping/gap-assessment.md`](../scoping/gap-assessment.md), [`../controls/`](../controls/) |
| 3 | **Prioritise the risks** | Put every gap into the risk register: score it, choose a treatment, assign an owner and a date | A scored register with owners and review dates | [`../risk/methodology.md`](../risk/methodology.md), [`../evidence/risk-register.md`](../evidence/risk-register.md) |
| 4 | **Implement the controls** | Work the highest risks first, using the control guides and runbooks | Changed systems and practices | [`../controls/`](../controls/), [`../runbooks/`](../runbooks/), [`../environments/`](../environments/), [`../privacy/`](../privacy/) |
| 5 | **Collect evidence** | For each control, produce dated evidence of the right kind (configuration, operational, effectiveness) using the templates and read-only verify commands | Evidence files, stored safely | [`../evidence/`](../evidence/), [`../verify/`](../verify/), [`../evidence/handling.md`](../evidence/handling.md) |
| 6 | **Check completeness** | Run the audit to find missing, stale, failing or overdue items | An audit report | [`../audit/`](../audit/) |
| 7 | **Review effectiveness** | Have the right people judge whether the controls actually work: test, investigate exceptions, track corrective actions | Review notes, corrective actions, updated risks | [`../controls/12-risk-and-governance.md`](../controls/12-risk-and-governance.md), [`../guide/maturity-model.md`](../guide/maturity-model.md) |
| 8 | **Prepare for due diligence** | Summarise what is implemented, what is open, evidence coverage, and the next actions | A short due diligence summary | [`../evidence/due-diligence-summary.md`](../evidence/due-diligence-summary.md), [`../checklists/before-investor-data-room.md`](../checklists/before-investor-data-room.md) |
| 9 | **Decide on formal assurance** | Use your actual commercial and regulatory requirements to decide whether to pursue SOC 2, ISO 27001 or another route, or none | A written decision with the reason and a review date | [`../guide/paths/`](../guide/paths/), [`../guide/roadmap.md`](../guide/roadmap.md) |

Repeat steps 5 to 8 on a schedule (the audit's freshness limits are a guide), and steps 1 and 9 when your customers or products change.

## What each step does not do

- Step 6 checks that evidence is present and recent. It does not judge whether a control works: that is step 7, and it is done by people.
- Step 8 summarises. It does not certify anything.
- Step 9 is a business decision, not a compliance one.
