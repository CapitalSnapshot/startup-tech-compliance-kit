# Risk methodology

Small enough to use, structured enough to be consistent.

## What to record per risk

A unique ID; the affected **asset, system or process**; the **threat** and its **business impact**; **likelihood** and **impact** ratings; the overall **rating**; **existing safeguards**; the chosen **treatment**; the **accountable owner**; the **target date**; the **review date**; and **evidence the treatment was implemented**. For an accepted risk, also **who accepted it**.

## Scoring

**Likelihood (1 to 5):** 1 rare (not expected in 3 years) · 2 unlikely · 3 possible (could happen in a year) · 4 likely (expected within months) · 5 almost certain (already happening or about to).

**Impact (1 to 5):** 1 negligible · 2 minor (small, recoverable, no customers affected) · 3 moderate (some customers affected, or data exposed with limited harm) · 4 major (many customers, significant personal data, contract or legal consequences) · 5 severe (company-threatening, or serious harm to people).

**Score = likelihood × impact.**

| Score | Rating |
|---|---|
| 1 to 4 | Low |
| 5 to 9 | Medium |
| 10 to 15 | High |
| 16 to 25 | Critical |

Rate the risk **with existing safeguards in place**. Re-rate after treatment.

## Treatment

| Treatment | Meaning | What to record |
|---|---|---|
| **Mitigate** | Reduce likelihood or impact with a control | The action, owner, target date, and later the evidence |
| **Avoid** | Stop doing the risky thing | What stops, and when |
| **Transfer** | Share the risk (insurance, a contract, a vendor) | What is transferred, to whom, the document |
| **Accept** | Live with it, knowingly | Who accepted it and why, and the review date |

## Who may accept what

Write your own version of this table. The principle: **the person who owns a risk should not be the only one who can accept a serious one**, and accepting is never permanent.

| Rating | May be accepted by | Review at least |
|---|---|---|
| Low | The risk owner | Yearly |
| Medium | The owner's manager or the technical lead | Every 6 months |
| High | A founder or director who is **not** the owner, in writing | Every 3 months |
| Critical | Not accepted by default. Treat it, or have the most senior decision-maker accept it in writing with a dated plan and an end date | Monthly |

A developer must not be able to accept a critical production risk because fixing it is inconvenient.

## Process

1. **Identify**: after an incident, a change, a vendor review, an audit finding, a scan result, or the yearly review.
2. **Assess**: score it. Write the threat and impact in one sentence each.
3. **Decide the treatment** and who owns it.
4. **Track**: review on the stated date. Overdue reviews are a finding.
5. **Close** only with evidence of treatment, or a dated acceptance that has expired and been renewed or removed.

The evidence check in [`../audit/`](../audit/) tests that the rating matches the scores, that each open risk has a treatment, an owner and a review date, that accepted serious risks were accepted by someone other than the owner, and that closed risks carry evidence.

## Yearly

Review the whole register, the scales (do they still fit?), and the acceptance table. Record the review as evidence for [`../controls/12-risk-and-governance.md`](../controls/12-risk-and-governance.md).
