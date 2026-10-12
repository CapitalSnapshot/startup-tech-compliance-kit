# Risk register

<!-- Method: ../risk/methodology.md. Score = likelihood x impact (1 to 5 each): 1-4 Low, 5-9 Medium, 10-15 High, 16-25 Critical. -->

| ID | Date | Asset or process | Threat and impact | Likelihood (1-5) | Impact (1-5) | Rating | Existing safeguards | Treatment | Accepted by | Owner | Target date | Review by | Status | Evidence of treatment |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R-001 | <YYYY-MM-DD> | <e.g. cloud account> | <e.g. the single owner account is lost; we cannot recover access> | 2 | 4 | Medium | <e.g. MFA on the account> | Mitigate | n/a | <role> | <YYYY-MM-DD> | <YYYY-MM-DD> | Open | <link when done> |

## Treatment values

Mitigate · Avoid · Transfer · Accept. See [`../risk/methodology.md`](../risk/methodology.md).

## Status values

Open · Treating · Accepted · Closed (a Closed row must carry evidence of treatment).

## Rules

- Every open row has an owner, a treatment, and a review date. "Accepted" is never permanent: it lasts until the review date.
- The rating must match likelihood times impact.
- A **High** or **Critical** risk that is accepted must be accepted by someone other than its owner.
- Do not delete rows; close them. The history is the evidence.
- Write a pipe character inside a cell as `\|`. An unescaped pipe splits the cell and shifts every column after it.
