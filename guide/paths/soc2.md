# Path to SOC 2

> **Standing notice.** This is repository based, community maintained guidance. It is not legal advice, a formal compliance assessment, a certification or an independent security audit. Mappings and statements about frameworks are unverified unless their review label says otherwise ([review labels](../../docs/review-labels.md)).

SOC 2 is an **attestation report** written by an independent CPA firm about your controls, against the AICPA Trust Services Criteria. You do not "get certified". You are examined, and the report says what the auditor found.

**Review label: community draft.** Proposed guidance, not legal advice and not an assessment. **Get specialist advice** from your examiner before you rely on it.

> **The kit cannot issue or guarantee a SOC 2 report.** Completing the kit, in whole or in part, is internal preparation. A SOC 2 report comes only from an examination by an independent CPA firm. Nothing the kit prints, and no checklist in it, means you have been examined, passed, or are "ready".

## What it is, in plain terms

- **Security** (the "common criteria") is always in scope. **Availability, confidentiality, processing integrity and privacy** are optional; include the ones your customers care about.
- **Type I** reports whether controls were suitably designed **at a point in time**. **Type II** reports whether they operated effectively **over a period** (commonly three to twelve months of observation). Enterprise customers usually ask for Type II. A Type I is a common first step.
- **You** define the scope and describe your system. The auditor tests what you claim.

## Type I and Type II are different reports

| | Type I | Type II |
|---|---|---|
| What the examiner reports on | Whether the controls you described were **suitably designed** | Whether they were suitably designed **and operated effectively** |
| Time frame | **A point in time** | **A period** (commonly three to twelve months of observation) |
| What the kit can help with | Having the controls and their evidence in place on a date | Having the controls running and the evidence collected continuously across the whole period |
| What the kit cannot do | Show the design is suitable | Show the controls operated effectively, or create the period: only time and the examiner do |

## Decisions the team must make (the kit cannot make them)

1. **System scope:** which systems, locations, people and vendors are in the description the examiner will test.
2. **The Trust Services Criteria that apply:** Security is always included; whether to add availability, confidentiality, processing integrity and privacy.
3. **The evidence period** (for Type II): when it starts and how long it runs.

Record all three, dated, in the [scoping questionnaire](../../scoping/questionnaire.md) before you start collecting evidence for an examination.

## Prerequisites (do these first)

1. A customer, contract or plan that needs it. If nobody asked, strengthen the baseline instead ([`../roadmap.md`](../roadmap.md)).
2. The [scoping questionnaire](../../scoping/questionnaire.md) answered: what is in scope, which criteria, which systems and people.
3. Controls 1 to 12 working, with dated evidence, long enough to have an operating history.

## Steps

| # | Step | What you produce |
|---|---|---|
| 1 | **Choose scope and criteria.** Systems, locations, people, vendors, and which of the five categories | A written scope and the criteria list |
| 2 | **Describe the system.** Services, infrastructure, software, people, data, and how they fit together | A system description (the auditor will want it) |
| 3 | **Map controls to criteria.** For each criterion you claim, name the control that meets it and the evidence | A control matrix. Start from [`../../controls/evidence-map.md`](../../controls/evidence-map.md) |
| 4 | **Close gaps.** Do a readiness assessment (yourself or with an adviser) and fix what it finds | Fixed controls; entries in the risk register for what remains |
| 5 | **Pick an assessor** (a licensed CPA firm). Ask about experience with companies your size and stack, timeline and what they need from you | An engagement letter |
| 6 | **Start the observation window** (Type II). Run controls as normal and keep evidence continuously | Dated evidence across the whole period |
| 7 | **Support the examination.** The auditor samples events (for example change requests, access reviews, incidents) and tests them | Evidence on request, answers to questions |
| 8 | **Review the report.** Management responses to any exceptions | The report; a plan for exceptions |
| 9 | **Repeat yearly.** Type II reports cover a period; customers want them current | A rolling programme |

## What the kit gives you, and what it does not

| Need | Kit | Still yours |
|---|---|---|
| Technical controls and evidence formats | [`../../controls/`](../../controls/), [`../../evidence/`](../../evidence/) | Operating them for the whole window |
| Governance and policies | [`../../policies/`](../../policies/), [`../../risk/`](../../risk/) | Making them true, and keeping them true |
| Evidence freshness checks | [`../../audit/`](../../audit/) | Judging effectiveness |
| Scope, system description, control matrix | Starting points | Writing them for your system |
| The examination itself | Nothing | An independent assessor |

## Coverage matrix: what the kit covers

"Covers in part" means the kit gives starting material, never that the requirement is met. The mapping records behind this are community drafts, and the SOC 2 records are "needs expert review" because the criteria document could not be read ([coverage report](../../docs/coverage/soc2.md)).

| Area | Kit | What the kit provides | What it does not |
|---|---|---|---|
| Security criteria (the common criteria): technical safeguards | **covers in part** | Controls 1 to 11, with evidence templates and read-only verify commands | A check against the criteria text; whether each criterion is met |
| Governance, risk assessment and policies | **covers in part** | Control 12, the risk method and register, policy templates | An oversight and risk assessment process an examiner accepts; proof people follow the policies |
| Availability category | **covers in part** | Backups, restore tests, continuity template (control 5) | Availability commitments in your system description; capacity and monitoring evidence beyond the templates |
| Confidentiality category | **covers in part** | Access, secrets, data classification template | Confidentiality commitments; disposal evidence |
| Processing integrity category | **does not cover** | Nothing specific | All of it |
| Privacy category | **covers in part** | A GDPR-oriented privacy process | The SOC 2 privacy criteria themselves |
| Choosing scope and categories | **covers in part** | The scoping questionnaire as a starting point | The decision |
| System description | **covers in part** | The environment and pipeline pages as starting points | A description written for your system |
| Control matrix against the criteria | **covers in part** | The control-to-evidence map and the mapping records (drafts) | A verified mapping |
| Evidence over an observation period | **covers in part** | Evidence templates and freshness checks | Collecting it continuously, and the period itself |
| Readiness assessment by an independent party | **does not cover** | Nothing | All of it |
| Choosing and engaging the examiner | **does not cover** | Nothing | All of it |
| The examination and the report | **does not cover** | Nothing | All of it |

## Exit criteria: what completing each shows, and what it does not

| Exit criterion | What it shows | What it does not show |
|---|---|---|
| Scope, categories and evidence period decided and recorded | The team has decided them | That the examiner will agree |
| All twelve controls have current, passing evidence on file (the audit says "internal evidence check complete") | The evidence is present, recent and recorded as passing | That any control is suitably designed or operated effectively |
| Known gaps are in the risk register with owners and dates | Gaps are visible and owned | That the gaps are acceptable to an examiner |
| A readiness assessment by an independent party has been done | What that party found (done outside the kit) | That you will be examined successfully |
| An examiner has been engaged | An engagement exists | Anything about the outcome |
| The examiner has completed the examination and issued a report | **Only here does a SOC 2 report exist** | For Type II, anything outside the period it covers |

**"Internal checklist complete"** means the first three rows are true. It does not mean you have been examined, that you passed, or that you are ready for a report.

## Common mistakes

- Starting the observation window before the controls were working. Exceptions in the window are in the report.
- Claiming more criteria than you need. Every criterion adds evidence and risk of exceptions.
- Writing policies you do not follow. Auditors test behaviour against what you wrote.
- Leaving evidence collection to the last month. Collect continuously.
- Treating "we passed the audit" as proof of security. It is a point-in-time view of the controls you described.
