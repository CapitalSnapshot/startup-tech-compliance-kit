# Incident response: the first hour

**Review label: community draft** for the personal-data notification parts. They are decision support, not legal advice, and they never conclude who must notify whom. **Get specialist advice** for any real breach. Sources used: Regulation (EU) 2016/679 (GDPR), Articles 4(7), 4(8), 4(12), 33 and 34, official text as published in the Official Journal of the European Union, L 119, 4 May 2016.

Keep this to one page that everyone with production access has read. The aim of the first hour is: stop it getting worse, keep the evidence, and know who needs to be told and by when. **Who must be told, and by when, depends on your role for the data affected.**

## 0. Declare (within minutes)

1. Open a row in [`../evidence/incident-register.md`](../evidence/incident-register.md). Record the **time the organisation became aware** of the incident (UTC) and **how that was decided**: who decided, and on what evidence. Statutory clocks count from awareness, so write it down at the time. If it is unclear when you became aware, **route to legal review**.
2. Name the incident lead and the escalation contacts (section 6). Everyone else takes instructions from them.
3. Open one channel for the incident. Keep a timeline there: time, action, role. Keep the **decision log** (section 7) from this moment.

## 1. Contain

- Cut off access first, investigate second: rotate or revoke the exposed credential, disable the account, block the address, take the affected service out of rotation.
- **Preserve evidence before clean-up**: snapshot the host or disk, export the relevant logs off-host, note the state of the system. Do not wipe or rebuild until this is done.
- Prefer reversible actions. Write down every change you make.

## 2. Assess

- What is affected? Which systems, which data, how many people?
- Is **personal data** involved? If it is, or you do not know yet, treat it as yes and go to section 3.
- Is the attacker or fault still active?
- Set the severity (SEV1 customer data exposed or service down, down to SEV4 near miss).

## 3. Decide your role for the affected personal data

A "personal data breach" is a breach of security leading to the accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data (Art. 4(12)). The duties differ by role. Decide the role **per set of data**, from your contracts and your [data inventory](../privacy/data-inventory.md), not from habit.

| Role | Test (Art. 4) |
|---|---|
| **Controller** | You, alone or jointly with others, determine the purposes and means of the processing (Art. 4(7)) |
| **Processor** | You process the data on behalf of a controller, typically a customer (Art. 4(8)) |

1. **We are a processor for the affected data.** Your statutory duty is to **notify the controller without undue delay after becoming aware** (Art. 33(2)). **Article 33 gives the processor no 72-hour deadline**, and the duty to notify the supervisory authority under Art. 33(1) is the **controller's**, not yours. Check each customer's agreement: it may set a **contractual deadline** (for example "24 hours") and a contact. That deadline is a **contract term, not a statutory deadline**, and "without undue delay" still applies: do not wait for a contractual deadline to run out. Go to section 4A.
2. **We are the controller.** The controller's duties are in Articles 33 and 34. Go to section 4B.
3. **We are both** (different data sets in one incident): handle each data set under its own role, separately.
4. **Joint controllers, or the roles are unclear:** **route to legal review.** Do not assume. (Article 26 on joint controllers was not reviewed for this page.)

Record the role for each data set in the incident report.

## 4A. Processor path

| Step | Detail |
|---|---|
| Notify each affected controller | **Without undue delay** after you became aware (Art. 33(2)); inside any shorter **contractual** deadline. Use the contact in the agreement |
| What to tell them | What happened, what data and how many records or people, likely consequences, what you have done. The controller needs it to meet its own duties. Provide further information as you learn it |
| Do not decide for them | Whether the controller notifies its supervisory authority or the people affected is the controller's decision. Do not notify on a customer's behalf unless it instructs you to and you have taken advice |
| Record | Each notification: who, when (UTC), by what channel, and which deadline applied (statute or contract) |

## 4B. Controller path

| Step | Detail |
|---|---|
| **Supervisory authority** | Notify the authority competent under Art. 55 **without undue delay and, where feasible, not later than 72 hours after becoming aware**, **unless** the breach is unlikely to result in a risk to people's rights and freedoms (Art. 33(1)). If you are later than 72 hours, include the **reasons for the delay**. The 72 hours is counted in hours; the text does not say working days |
| What to include | At least: nature of the breach, with categories and approximate numbers of people and records; contact point (DPO or other); likely consequences; measures taken or proposed (Art. 33(3)). If you cannot supply it all at once, provide it **in phases** without undue further delay (Art. 33(4)) |
| **Affected people** | See the assessment below |
| **Document every breach** | Facts, effects and remedial action, enough for the authority to verify compliance (Art. 33(5)). This applies to breaches you decide **not** to notify |

### Assess whether affected people must be told (controller only)

Answer in order and record each answer and reason.

1. Is the breach **likely to result in a high risk** to people's rights and freedoms? If **yes**, you must communicate it to them **without undue delay** (Art. 34(1)), in clear and plain language, with at least the contact point, likely consequences and measures (Art. 34(2)). If **no**, record why. If unsure, take advice.
2. If yes, does an exception apply (Art. 34(3))? (a) Appropriate protection was applied to the affected data that renders it unintelligible to unauthorised persons, such as encryption; (b) subsequent measures ensure the high risk is no longer likely to materialise; (c) it would involve disproportionate effort, in which case a **public communication or similar** equally effective measure is needed instead. An exception needs facts you can show.
3. The supervisory authority can require you to communicate, or decide an exception is met (Art. 34(4)).

## 5. Decide who else to tell (write each decision down)

| Who | When | Where it is recorded |
|---|---|---|
| Affected controllers (if you are a processor) | Section 4A | Notification table in the incident report |
| Supervisory authority and affected people (if you are a controller) | Section 4B | Same |
| Customers under contract | As the contract requires (a contractual deadline) | Same |
| Regulators under other regimes, insurers, investors | As their rules or terms require | Same |

**Other incident reporting regimes may apply** (for example sector or national rules, or security regulations). This runbook does not describe them. See [`../scoping/applicability-matrix.md`](../scoping/applicability-matrix.md) and take advice.

If you decide **not** to notify, record the reason on the same row. That decision is evidence.

## 6. Escalation contacts (fill in before you need them)

| Role | Who (role or name) | How to reach them out of hours | Backup |
|---|---|---|---|
| Incident lead | <...> | <...> | <...> |
| Privacy contact (and DPO, if designated) | <...> | <...> | <...> |
| Legal adviser | <...> | <...> | <...> |
| Senior decision-maker | <...> | <...> | <...> |
| Customer contacts for processor notifications | see the table below | | |

| Customer (controller) | Agreement | Processor notification deadline in the contract | Contact for incidents |
|---|---|---|---|
| <...> | <reference and date> | <e.g. 24 hours, or "without undue delay"> | <...> |

## 7. Decision log (start at declaration)

| Time (UTC) | Decision | Basis (article, contract clause, or reasoning) | Decided by (role) | Evidence |
|---|---|---|---|---|
| <...> | <e.g. "We are the processor for dataset A"> | <Art. 4(8); agreement with Customer X> | <role> | <link> |

## 8. Recover

Restore from known-good artefacts: a signed image by digest, a restored backup, rotated credentials. Check it is clean before reconnecting. Run the smoke tests.

## 9. Learn (within a week)

Complete [`../evidence/incident-report.md`](../evidence/incident-report.md), blameless, with actions that have an owner and a date. Link it in the register. Review the actions at the next review date.

## Rehearse

Run a tabletop exercise at least yearly: use [`tabletop-incident-notification.md`](tabletop-incident-notification.md) or your own scenario, walk this page, time it, and record what you changed. An exercise record counts as evidence for [`../controls/09-incident-response.md`](../controls/09-incident-response.md).
