# Review labels and coverage statuses

One source of truth for two things that must never be confused: **how far a piece of guidance has been reviewed**, and **how far the kit covers a requirement**. Every other page links here.

> The kit is repository-based, community-maintained guidance. It is not legal advice, a compliance assessment, a certification or an independent security audit. Read the label before you rely on any content.

**Current position.** All compliance content in this kit is a **community draft**. At the time of writing no mapping, guide or template carries the label "maintainer reviewed" or "specialist reviewed". Content gets a stronger label only when that review has actually happened and is recorded.

## Review labels (three, exactly)

| Label | What it means | What it does not mean | Who can grant it |
|---|---|---|---|
| **Community draft** | Proposed. Formatting and basic automated checks may have passed. | It does **not** mean substantively verified. | Any contributor, by default. It is the starting label for all new and materially changed compliance content |
| **Maintainer reviewed** | Source and reasoning checked; limitations documented. | It does **not** mean legal or specialist approval. | A maintainer, who should not be the author of the change, after checking the content against the cited source. The reviewer's role, the date and the decision are recorded |
| **Specialist reviewed** | A qualified reviewer examined the material within a recorded scope. | It does **not** mean a guarantee of compliance. Only the reviewed material is covered. | A qualified reviewer for that subject (for example a privacy professional for GDPR content, an assessor for SOC 2 or ISO 27001 content). The scope, date and reviewer's role are recorded and published. Maintainers do not award it to themselves |

Rules:

- **Passing CI, or a maintainer's approval of a pull request, does not imply legal or specialist approval.** CI checks form, not truth.
- **Never record a reviewer, a review date or a stronger label that did not happen.**
- A material change to reviewed content resets its label to **community draft** until it is reviewed again.
- A label applies to the content named in its scope, not to the whole repository.

## Coverage statuses (six, exactly)

A coverage status says how far the kit addresses a specific requirement of a framework, law or standard. **"Covered" is allowed only on a record labelled maintainer reviewed or specialist reviewed**; a community draft cannot claim it, and the validator rejects it. Even then it says how far the kit addresses the requirement, never that you meet it. There is **no seventh status**. A **blank value is not allowed**, and **silence must never be read as a status**: if a requirement or framework is not mentioned, that tells you nothing about coverage or applicability.

| Status | Meaning | Written rationale required? | Example |
|---|---|---|---|
| **covered** | A maintainer or specialist reviewed the record and recorded that the kit addresses what the requirement asks of the kit's scope. It does **not** mean you meet the requirement | The review decision and rationale | A kit control and its evidence template address a narrow requirement in full, and a reviewer recorded that |
| **covered in part** | The kit addresses some of what the requirement asks. List what is covered and what is not | List what is **not** covered | A kit control supports a requirement on access control but the kit does not write the policy that the requirement also expects |
| **not covered** | The requirement is in the framework's scope for the reader, and the kit does not address it | **Yes** | The kit provides no internal audit programme, which an ISMS needs |
| **not applicable** | The requirement does not apply to the stated scope, and the exclusion is deliberate and documented | **Yes** | A requirement about premises, where the stated scope has no premises and says why |
| **not assessed** | No assessment of this requirement has been attempted | No | A clause nobody has looked at yet |
| **needs expert review** | An assessment was attempted but needs a qualified reviewer's judgement | Say what the open question is | Whether a contractual requirement is also a statutory duty |

How to tell a gap from an exclusion:

- **not covered** is an actual gap the reader may need to fill.
- **not applicable** is a deliberate, documented exclusion, with the reason.
- **not assessed** is neither: it means the question has not been asked yet.

## Where these are used

- [`../CONTRIBUTING.md`](../CONTRIBUTING.md): proposals start as community draft.
- Issue and pull request templates in [`../.github/`](../.github/).
- [`../controls/framework-mappings.md`](../controls/framework-mappings.md) and [`../scoping/applicability-matrix.md`](../scoping/applicability-matrix.md).
- [`coverage/README.md`](coverage/README.md): generated counts and lists of what has and has not been assessed, per framework.
