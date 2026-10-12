# Incident report: INC-<number> , <short title> , <YYYY-MM-DD>

<!-- kit-evidence: control=09 date=YYYY-MM-DD result=pass type=operational -->  <!-- date = the day the report was completed; result = pass if the response followed the plan, partial or fail if it did not -->

**Severity:** <SEV1 / SEV2 / SEV3 / SEV4> **Incident lead:** <role> **Status:** Open / Contained / Closed
**Aware (UTC):** <time> **How awareness was decided, and by whom:** <...>
**Contained (UTC):** <time> **Resolved (UTC):** <time>
**Role for the affected personal data:** <controller / processor / both, per dataset / unclear: legal review> (Art. 4(7), 4(8))
**Contractual notification deadlines that applied (per customer, from the agreement):** <...>

Blameless: describe what the system allowed, not who erred. Names go as roles.

## Summary

<Three sentences: what happened, who or what was affected, current state.>

## Timeline (UTC)

| Time | Event | Who (role) |
|---|---|---|
| <time> | <detected how> | <role> |
| <time> | <first action> | <role> |

## Impact

- **Systems and data affected:** <...>
- **Personal data involved?** Yes / No / Unknown. If yes: categories, approximate number of people, and whether it was encrypted.
- **Customers affected:** <number or "none">
- **Duration of impact:** <...>

## Cause

<Direct cause, then the underlying causes (process, tooling, review). Use "five whys" until you reach something you can change.>

## Containment and recovery

<What stopped the damage, what was restored, and how you checked it was safe. Evidence was preserved before clean-up: yes / no, where.>

## Notification decisions

Record the decision even when it is "no". A decision with its reason is evidence; silence is not.

| Who | Role it depends on | Decision (notify / do not notify) | Basis (statute or contract clause) and reason | Time sent (UTC) |
|---|---|---|---|---|
| Affected controllers (each customer) | Processor: Art. 33(2), without undue delay, plus any contractual deadline | <...> | <...> | <...> |
| Supervisory authority | Controller: Art. 33(1), without undue delay and where feasible within 72 hours of awareness, unless unlikely to result in a risk; reasons if late | <...> | <...> | <...> |
| Affected people | Controller: Art. 34(1), if likely high risk; check the Art. 34(3) exceptions | <...> | <...> | <...> |
| Customers under contract (other) | Contract | <...> | <...> | <...> |
| Other regulators, insurers, investors | Their rules or terms (see the applicability matrix) | <...> | <...> | <...> |

Keep contractual deadlines and statutory deadlines in separate rows or columns. Never record a contract term as a statutory deadline.

## What worked, what did not

- Worked: <...>
- Did not: <...>

## Actions

| # | Action | Owner (role) | Due | Done |
|---|---|---|---|---|
| 1 | <...> | <role> | <YYYY-MM-DD> | <YYYY-MM-DD> |

Add the incident to [`incident-register.md`](incident-register.md) and link this report there.
