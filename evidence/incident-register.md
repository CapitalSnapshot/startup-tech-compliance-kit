# Incident register

One row per incident, **including near misses and breaches you decided not to notify**. Under GDPR Art. 33(5) a personal-data breach must be documented whether or not it is reported. If you have had none, say so with the date you started keeping this register.

| ID | Detected (UTC) | Severity | Summary | Personal data involved | Notification decision (who, decision, time or reason) | Report | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| INC-001 | <YYYY-MM-DD hh:mm> | <SEV1-SEV4> | <one line> | Yes / No / Unknown | <e.g. authority: not notified, data was encrypted and keys not exposed; customers: notified 2026-01-02 10:15> | <link to the incident report> | <role> | Open / Contained / Closed |

## Rules

- Write a pipe character inside a cell as `\|`. An unescaped pipe splits the cell and shifts every column after it.
- Open the row when you **detect** the incident, not when you finish the report. In **Detected (UTC)** record the time the organisation **became aware** (see [`../runbooks/incident-response.md`](../runbooks/incident-response.md)), because statutory clocks count from awareness.
- Personal data = **Yes** or **Unknown** requires a notification decision on the same row. State your **role** (controller or processor) in the decision, and keep contractual deadlines separate from statutory ones.
- A row can be Closed only when the report exists and its actions have owners and dates.
- Never delete a row. Closed rows are the evidence that the process works.
- "No incidents recorded since <YYYY-MM-DD>" is a valid entry if true.
