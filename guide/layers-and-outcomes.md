# Layers and outcomes

## Security is not compliance

A company can have excellent access controls, encrypted databases and tested backups and still fail its legal or contractual obligations. A company can also hold a certificate and still have weak security. They are different things, and this kit mostly helps with the first.

| Layer | What it establishes | Where this kit helps |
|---|---|---|
| **1. Technical security** | Systems have appropriate safeguards | [`../controls/`](../controls/), [`../environments/`](../environments/), [`../runbooks/`](../runbooks/) |
| **2. Operational governance** | People have defined responsibilities and follow documented processes | [`../policies/`](../policies/), [`../risk/`](../risk/), [`../controls/12-risk-and-governance.md`](../controls/12-risk-and-governance.md) |
| **3. Legal and regulatory compliance** | Applicable legal obligations have been identified and addressed | [`../privacy/`](../privacy/), [`../scoping/applicability-matrix.md`](../scoping/applicability-matrix.md). Legal advice remains yours to get |
| **4. Framework assurance** | A selected framework's requirements are implemented and independently assessed, where that applies | [`roadmap.md`](roadmap.md) for the choice. The assessment itself is done by an independent party, not by this kit |

The kit is strongest on layer 1, covers the basics of layers 2 and 3, and only points at layer 4.

## What is established, and what is not

| If you have... | You have shown... | You have **not** shown... |
|---|---|---|
| The technical controls (1 to 11) and their evidence | Safeguards exist and were exercised on a date | That they are adequate for your risks, or that you meet any framework |
| A SOC 2 style control set | A sound baseline | Your scope, the criteria that apply to you, or the operating history an examination needs |
| ISO 27001 style controls | Many Annex A topics covered | A functioning ISMS: risk assessment and treatment, defined responsibilities, internal audit, management review, continual improvement |
| A privacy notice and processor agreements | Two GDPR building blocks | Lawful bases, retention, data subject rights, transfers and the rest |
| DORA control references | Useful practice | That DORA applies to you, or what kind of obligation it would be. It places duties directly on financial entities; a startup serving one usually meets it through contract terms; designated critical ICT providers face oversight. See [`../scoping/dora-screening.md`](../scoping/dora-screening.md) |

## Choose the outcome first

Be explicit about what you want out of this. The paths differ.

1. **Good security hygiene.** Run Phase 1 and 2 of the [roadmap](roadmap.md). No framework needed.
2. **Answer enterprise security questionnaires.** Add Phase 3: an evidence pack, a vendor register, a privacy position, and a short security overview you can send.
3. **Foundation for SOC 2 or ISO 27001.** Everything above, plus a decision on scope, the governance layer, and an independent assessor. Start only when a customer, contract or commercial plan requires it.

The kit can support all three. Pick one, write it down in [`../scoping/questionnaire.md`](../scoping/questionnaire.md), and revisit it when your customers change.
