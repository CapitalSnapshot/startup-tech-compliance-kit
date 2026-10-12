# Risk register (example)

| ID | Date | Asset or process | Threat and impact | Likelihood (1-5) | Impact (1-5) | Rating | Existing safeguards | Treatment | Accepted by | Owner | Target date | Review by | Status | Evidence of treatment |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R-001 | 2026-09-01 | Cloud account | Single owner account lost; no recovery | 2 | 4 | Medium | MFA on the account | Mitigate | n/a | Engineer | 2026-12-01 | 2027-03-01 | Open |  |
| R-002 | 2026-06-01 | Old tool | Stale read access | 2 | 2 | Low | Read-only | Mitigate | n/a | Engineer | 2026-07-01 | 2026-07-01 | Closed | Access removed 2026-06-20, see access review |
| R-003 | 2026-09-10 | Reporting database | Analyst can read personal data they do not need | 3 | 4 | High | Role limits columns | Accept | Founder | Engineer | n/a | 2026-12-10 | Accepted |  |
