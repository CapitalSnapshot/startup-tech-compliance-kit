# Startup Tech Compliance Kit

**Build a security and compliance foundation for your startup without starting from a blank page.**

An open-source toolkit of practical controls, runbooks, templates and evidence checks, written for small teams with no compliance specialist. Published by CapitalSnapshot under the Apache License 2.0.

> **Standing notice.** This is repository based, community maintained guidance. It is not legal advice, a formal compliance assessment, a certification or an independent security audit. Mappings and statements about frameworks are unverified unless their review label says otherwise ([review labels](docs/review-labels.md)). All content is a community draft until a review is recorded.

> **What this is, and is not.** The kit provides implementation guidance, operational templates and evidence checks to help startups establish security and compliance foundations. **It does not guarantee compliance with any law, regulation, contractual obligation or certification framework.** It does not replace legal advice, an independent audit, or a framework-specific assessment. Framework references are indicative: check them against the current text, and have a qualified person review your result.
>
> **Privacy and legal material (`privacy/`, `scoping/applicability-matrix.md`, and the GDPR references) was written by engineers, not lawyers. Get specialist advice before you rely on it.** That means a privacy or data-protection professional for lawful bases, transfers, breach notification, DPO and DPIA decisions, and a qualified adviser for which laws and frameworks apply to you.

## What problem does it solve?

Security and compliance work usually starts late, in a hurry, when a customer sends a questionnaire or an investor asks for diligence. By then the evidence does not exist. This kit gives you a sensible order of work, and the habit of leaving dated evidence as you go.

## Who is it for?

Founders, CTOs and small engineering teams, typically pre-launch to a few dozen people, building a SaaS product, often serving customers in the EU. You do not need a compliance background.

## What will you have when you finish?

- A **security baseline**: twelve controls, each with what to do, what proves it, and its limits.
- A **scoped view** of which laws and frameworks apply to you, and which you are deliberately not pursuing.
- A **risk register** with owners, scores and treatment decisions, and short **policies** that match what you do.
- A **privacy process** (GDPR) from data inventory to deletion, and an **incident register** and runbook.
- **Dated evidence** for each control, and a script that checks it is present and recent.
- A **due diligence summary** you can send, and a clear view of whether SOC 2 or ISO 27001 is worth pursuing.

## How do I start?

1. Run `python3 scripts/kit_start.py` (or read [`START.md`](START.md)). Five questions give you a prioritised list.
2. Fill in the [scoping questionnaire](scoping/questionnaire.md).
3. Do the [first-week checklist](checklists/first-week.md) and implement the highest-priority [controls](controls/).
4. Keep the evidence, review outstanding risks, and run `python3 audit/kit-audit.py` to see what is missing or stale.

The full path is in the [end-to-end workflow](workflow/README.md). To see what a finished control looks like before you begin, read the [worked example](examples/completed-control-backups.md).

## What this project does not do

- It does not certify or assess your compliance, and passing its checks does not mean you comply with anything.
- It does not judge whether a control **works**. Its audit checks that evidence is present, recent and recorded as passing. People judge effectiveness.
- It does not give legal advice. Lawful bases, transfers, breach notification and what applies to you need judgement. **Get specialist advice**; the privacy material has not been reviewed by a specialist.
- It does not configure or inspect your cloud accounts. It gives read-only commands you run yourself.
- It does not cover every framework, sector or country. See the [applicability matrix](scoping/applicability-matrix.md).

How far content has been reviewed, and how far the kit covers a requirement, are defined in [`docs/review-labels.md`](docs/review-labels.md). **All compliance content is currently a community draft.** What has and has not been assessed, per framework, is in the generated [coverage reports](docs/coverage/README.md): counts and lists only, not a measure of anyone's compliance.

Requirements: Python 3.9 or later (standard library only) for the scripts. The scripts are tested on 3.9, 3.10, 3.11, 3.12 and 3.13. See [`VERSIONING.md`](VERSIONING.md), [`CHANGELOG.md`](CHANGELOG.md), [`SECURITY.md`](SECURITY.md) and [`MAINTENANCE.md`](MAINTENANCE.md).

## The order of reading

**First hour:** run `python3 scripts/kit_start.py` (or read [`START.md`](START.md)). Five questions give you a prioritised list of what to do first, with links. Then follow the [end-to-end workflow](workflow/README.md).

1. Read [`guide/layers-and-outcomes.md`](guide/layers-and-outcomes.md). **Security is one of four layers; this kit mostly helps with the first.** A passing control set does not make you compliant with SOC 2, ISO 27001, GDPR or DORA.
2. Fill in [`scoping/questionnaire.md`](scoping/questionnaire.md) and read [`scoping/applicability-matrix.md`](scoping/applicability-matrix.md), so you know what applies to you and do not chase frameworks you do not need.
3. Follow [`guide/roadmap.md`](guide/roadmap.md): secure baseline, operational accountability, customers and due diligence, then a formal destination if you need one.

## What is in it

| Folder | What it gives you |
|---|---|
| [`START.md`](START.md), [`workflow/`](workflow/) | A five-question first hour, and a nine-step workflow from scoping to the decision on formal assurance |
| [`guide/`](guide/) | The four layers (security, governance, legal, assurance), a four-level maturity model, a phased roadmap, and general paths to SOC 2 and ISO 27001 |
| [`scoping/`](scoping/) | A scoping questionnaire and an applicability matrix: what applies, to whom, and who decides |
| [`controls/`](controls/) | Twelve controls with stable IDs and a generated `controls.json`, each as: what to do, why a reviewer asks, "done when", the evidence to keep, common mistakes, and indicative framework references (SOC 2, ISO 27001, GDPR, DORA) |
| [`privacy/`](privacy/) | A connected GDPR operating process: data inventory, lawful basis, retention, requests, transfers, DPIA screening, privacy by design, accountability |
| [`risk/`](risk/) | A scoring method, treatment options and rules for who may accept which risk |
| [`policies/`](policies/) | Short templates for the governance layer: security, acceptable use, joiners and leavers, training, data classification, continuity, secure development, keys, roles |
| [`examples/`](examples/) | A worked example of one completed control, with the real audit output |
| [`verify/`](verify/) | Read-only commands that produce evidence for each control, for AWS, Google Cloud and Azure, with a status line on every command. Regional and EU-native providers can add their own |
| [`environments/`](environments/) | A dev / demo / production layout, and a build-once, promote-by-digest pipeline with signing and branch rules |
| [`runbooks/`](runbooks/) | Incident response, cutover, rollback, restore test, and rebuild-from-nothing |
| [`evidence/`](evidence/) | Fill-in templates: evidence file, risk register, vendor register, access review, restore-test report, incident report and incident register |
| [`checklists/`](checklists/) | First week, before the first customer, before an investor sees your data room |
| [`audit/`](audit/) | `kit-audit.py`: reads your evidence and registers and reports, per control, whether dated evidence exists, is fresh and passed. An evidence check, not a compliance assessment |
| [`skills/production-migration/`](skills/production-migration/) | A Claude skill and prompt pack that walks a coding agent through a phased migration, one action at a time |

## How to use it

1. Do the **start here** steps above. They take an hour and decide what the rest is for.
2. Read [`checklists/first-week.md`](checklists/first-week.md) and do the items that cost an hour or less.
3. Work through [`controls/`](controls/) in order. For each control, write the evidence file it asks for into your own repository, using the templates in [`evidence/`](evidence/) and the [control-to-evidence map](controls/evidence-map.md).
4. Put your decisions in the [risk register](evidence/risk-register.md), scored with [`risk/methodology.md`](risk/methodology.md). A written, dated "we accept this, because" by someone with the authority to accept it is worth more to a reviewer than a silent gap.
5. Finish with [`audit/`](audit/): run `kit-audit.py` over your evidence and fix what it reports as missing or stale. It checks that evidence is complete and fresh. It does not judge whether your controls work.
6. If you are moving off a legacy host or platform, use [`skills/production-migration/`](skills/production-migration/).

## Principles

- **Evidence over assertion.** A control is done when you can show a dated file, log or screenshot, not when
  you believe it is done.
- **One artefact, promoted.** Build once; promote the same signed artefact through environments.
- **Tested restores.** A backup you have not restored is a hope.
- **Written decisions.** Record who decided, when, and why.
- **Least privilege, no shared secrets.** Separate roles per environment; secrets live in a secrets manager.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Keep everything generic: no real hostnames, account IDs, names or
credentials. A CI scan enforces this.

## Licence

Apache License, Version 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
