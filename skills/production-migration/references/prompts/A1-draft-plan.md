# A1. Draft the plan

Run in: a normal chat assistant (not a coding agent). Do this before any infrastructure work.

```text
I am the CTO of <COMPANY>, a <SECTOR> startup with <TEAM SIZE> people. Our product is <WORKLOAD, e.g. a web application with an API, a database, file uploads and background jobs>, running on <CURRENT HOSTING>. The starting point is <STARTING POINT: a single VM, a platform-as-a-service, or an existing cloud account with unmanaged resources>. The database is <DB FAMILY AND VERSION> and the target provider is <CLOUD PROVIDER>. I want <PATH: lean (dev and production, minimal evidence) or full (dev, demo and production, full evidence pack)>, with environments deployed by a pipeline, and I want the result to produce evidence that supports <COMPLIANCE TARGETS, e.g. SOC 2, ISO 27001, GDPR, DORA> and for due diligence by partners and banks. Constraints: <CONSTRAINTS, e.g. one cloud account only, team of one developer, cutover before DATE>. Draft a versioned migration plan covering: current and target architecture; environment model; access control and secrets; logging and monitoring; backup and recovery with RPO and RTO; change management; data classification; a phase-by-phase plan with exit criteria; a rollback plan with a named decision owner and deadline; a decision log with a trigger for revisiting each decision; and a table mapping each control to the framework clauses it supports. Mark every assumption about the current system as UNVERIFIED so the inventory phase can confirm or correct it.
```

Next: [A2. External review](A2-external-review.md)
