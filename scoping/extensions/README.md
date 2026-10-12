# Extensions: screening aids for regimes outside the core mappings

Review label: community draft ([`../../docs/review-labels.md`](../../docs/review-labels.md)). Not legal advice.

The kit's core is the twelve controls and their mappings to SOC 2, ISO/IEC 27001, GDPR and DORA. Other regimes (NIS2, PCI DSS, ePrivacy, national law variations) sit here, apart from the core, until the core mappings have been reviewed. They are kept separate so that nobody reads them as part of the mapped baseline.

## Boundaries

- **An extension is a screening aid.** It helps you record a question, the facts, the sources and who decided. It does not give an answer.
- **The kit does not assess compliance with any extension regime.** Nothing here is mapped to controls, nothing here has a coverage status, and the evidence check (`audit/kit-audit.py`) does not look at it.
- **Outcomes are decision support**: "potentially in scope", "not in scope based on a documented assessment", or "requires advice". The second needs a written rationale and a reviewer. None of them is a legal conclusion.
- **National law decides.** A directive binds Member States, and what applies to you is the national law of each Member State involved. The kit does not state the transposition status of any Member State. You record the national law, its status and the date you checked.
- Every extension is a community draft until a maintainer or specialist review is recorded.

## What is here

| Extension | File | Status |
|---|---|---|
| NIS2 (Directive (EU) 2022/2555) | [`nis2-screening.md`](nis2-screening.md) | Community draft |

PCI DSS, ePrivacy and national variations are listed in [`../applicability-matrix.md`](../applicability-matrix.md) and have no worksheet yet.
