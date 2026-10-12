# 3. Change management

| | |
|---|---|
| **Control ID** | KIT-CHG-01 |
| **Evidence number** | 03 (the `control=` value in evidence headers) |
| **Applies to** | Every change that reaches production: code, configuration and infrastructure |
| **Owner (role)** | Engineering lead |
| **Review frequency** | Every 100 days or sooner (quarterly); the audit flags evidence older than 100 days |
| **Limitations** | Branch rules show a gate exists; they do not show the whole delivery process is secure or that reviews are meaningful |

**Objective:** Every change reaches production through a reviewed pull request and an automated pipeline, with a record of who approved what.

## What to do

- Protect the main branches: require a pull request, require the pipeline's checks to pass by name, and allow no bypass, including for administrators.
- Require at least one reviewer who did not write the change. For a one-person team, require the pipeline checks and record the self-review honestly.
- Deploy only from the pipeline. Nobody edits a running server by hand.
- Keep a record of each production change: what, who, when, which pull request, and how to undo it.
- Make emergency changes follow the same path, faster, and write them up afterwards.

## Why a reviewer asks

Reviewers sample recent production changes and ask for the pull request, the review, the passing checks and the deploy record behind each.

## Done when

- [ ] Branch rules on the production branch require a pull request and every check, with no bypass.
- [ ] A sample of five recent production changes each traces to a reviewed pull request and a green pipeline run.
- [ ] No shell access is used to change production code or configuration, and the host's file system is not a second copy of the code.
- [ ] New pipeline checks are added to the branch rule's required list, because a check that is not listed is not enforced.

## Evidence to keep

- Branch-rule export or screenshot.
- Five sampled changes with links to pull request, review and run.
- The deploy log.
- The post-incident note for any emergency change.

### Kinds of evidence

- **Configuration:** The branch-rule export
- **Operational:** Five sampled changes traced to reviews and green runs
- **Effectiveness:** An attempted merge with a red or missing check is refused
- **Independent assurance:** only where a customer, contract or plan needs it ([`../guide/paths/`](../guide/paths/))

Label each file with its `type` ([`../evidence/README.md`](../evidence/README.md)). Configuration and operational evidence show a control exists and is used; only effectiveness and assurance evidence speak to whether it works.

## Common mistakes

- Required checks listed by an old name, so renamed checks are silently not required.
- Administrators who can bypass the rules "just this once".
- A hand edit on the server that nobody records.
- A pull request merged while a check is red or missing.

## Indicative framework references

SOC 2 CC8.1 · ISO 27001:2022 A.8.32, A.8.25, A.8.31 · GDPR Art. 25, 32 · DORA Art. 9

These are indicative. Why each applies and what more is required: [`framework-mappings.md`](framework-mappings.md). Check them against the current text of each framework.

## How to verify

Provider-neutral commands: [`../verify/common.md`](../verify/common.md). Cloud-provider commands, where they apply: [`../verify/`](../verify/) (section 03). Save the output as a dated evidence file. A command shows a setting; whether it is enough is your judgement.

## Related

- [`../environments/pipeline.md`](../environments/pipeline.md)
