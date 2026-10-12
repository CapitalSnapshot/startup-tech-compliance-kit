# DPIA screening: preliminary, not a legal threshold

**Review label: community draft.** Proposed guidance. It has not been reviewed by a maintainer or by a specialist. It is decision support, not legal advice. **Get specialist advice** for anything that matters.

This page is a **preliminary screening**. It is **not a legal threshold**. Whether a data protection impact assessment (DPIA) is required turns on an assessment of the actual processing and its risks, not on a count of answers.

Sources used: Regulation (EU) 2016/679 (GDPR), Article 35 (data protection impact assessment) and Article 36(1) (prior consultation), official text as published in the Official Journal of the European Union, L 119, 4 May 2016. **Source verification pending:** the extra risk factors in section 3 are not in Article 35; they are commonly drawn from the Article 29 Working Party guidelines on DPIA (wp248rev.01), whose title and a 13 October 2017 listing were checked but whose content was not reviewed. Also pending: the content of your own supervisory authority's lists.

<!-- kit-evidence: control=08 date=YYYY-MM-DD result=pass type=operational -->

## What Article 35 says (summary)

- **Art. 35(1):** where a type of processing, in particular using new technologies, and taking into account its **nature, scope, context and purposes**, is **likely to result in a high risk** to people's rights and freedoms, the controller must carry out an assessment **before** the processing. One assessment may cover a set of similar operations with similar high risks.
- **Art. 35(3):** a DPIA is **in particular required** for (a) a systematic and extensive evaluation of personal aspects based on automated processing, including profiling, on which decisions are based that produce legal effects or similarly significantly affect people; (b) large-scale processing of special categories of data (Art. 9(1)) or of data on criminal convictions and offences (Art. 10); (c) systematic monitoring of a publicly accessible area on a large scale.
- **Art. 35(4) and (5):** each supervisory authority must publish a list of processing that **requires** a DPIA, and may publish a list for which none is required.

## 1. Record the context (all fields are required)

| Field | Entry |
|---|---|
| Processing activity | <...> |
| Context (who, where, relationship with the people, their reasonable expectations) | <...> |
| Nature (what is done to the data, how, with what technology) | <...> |
| Scope (volume, categories of data, number of people, geography, duration) | <...> |
| Purposes | <...> |
| Affected people | <...> |
| Severity of potential harm to them | <...> |
| Likelihood of that harm | <...> |
| Supervisory authority consulted, list name, and date checked (the list of processing that requires a DPIA, and any list of processing that does not) | <authority>, <list>, <YYYY-MM-DD> |

## 2. Serious indicators

**Any one** of these answered "yes" or "unsure" means the outcome is **"DPIA likely required or seek advice"**, whatever the rest of the screening shows.

| Serious indicator | Source | Yes / No / Unsure |
|---|---|---|
| Systematic and extensive evaluation of personal aspects based on automated processing, including profiling, on which decisions are based that produce legal effects or similarly significantly affect people | Art. 35(3)(a) | <...> |
| Large-scale processing of special categories of data or of data on criminal convictions and offences | Art. 35(3)(b) | <...> |
| Systematic monitoring of a publicly accessible area on a large scale | Art. 35(3)(c) | <...> |
| The kind of processing is on your supervisory authority's published list of processing that needs a DPIA | Art. 35(4) | <...> |

## 3. Further risk factors (a screening aid; not from Article 35 itself)

These help you judge whether a DPIA is advisable. They are **not** serious indicators and **never** make a DPIA mandatory on their own count. **Maintainer review needed:** their source is the guidelines named above and has not been verified.

| Risk factor | Yes / No / Unsure |
|---|---|
| Vulnerable people (for example children, patients, employees in some settings) | <...> |
| Innovative technology, or a new use of existing technology (including some AI uses) | <...> |
| Matching or combining data sets from different sources | <...> |
| Processing that may stop people exercising a right or using a service | <...> |

## 4. Outcome

| Outcome | When | What it means |
|---|---|---|
| **DPIA likely required or seek advice** | Any serious indicator is "yes" or "unsure" | Do a DPIA, or take advice first. **A low score never overrides a serious indicator.** This outcome is returned even if the record is incomplete |
| **DPIA recommended; document your reasoning** | No serious indicator; two or more further risk factors ("yes" or "unsure") | Do a DPIA unless you can write down why the processing is not likely to result in a high risk |
| **DPIA may not be required; record the reasons and review** | No serious indicator; fewer than two further risk factors; **every field complete, including the authority list consulted** | A reasoned record, not a conclusion. Art. 35(1) still turns on the nature, scope, context and purposes. Review when anything changes |
| **Cannot decide: complete the missing fields** | Any field or answer is missing and no serious indicator applies | Fill in the missing items. The tool never returns "may not be required" on an incomplete record |

The number of further risk factors is shown for information only. It is **not** a legal test.

## 5. The decision is a reviewable record

| Item | Entry |
|---|---|
| Outcome | <...> |
| Rationale (the facts and reasoning, including why any "no" is supportable) | <...> |
| Decision owner (role) | <...> |
| Decision date | <YYYY-MM-DD> |
| Review date, and the changes that trigger an earlier review (Art. 35(11): at least when the risk changes) | <YYYY-MM-DD> |

Run the same logic from a file of answers: `python3 scripts/dpia_screen.py privacy/dpia-answers.example.json --markdown` (copy the example and fill it in).

## If a DPIA is required or advised

Article 35(7) says the assessment must contain **at least**: (a) a systematic description of the envisaged processing and its purposes, including where applicable the controller's legitimate interest; (b) an assessment of necessity and proportionality in relation to the purposes; (c) an assessment of the risks to people's rights and freedoms; and (d) the measures envisaged to address the risks, including safeguards, security measures and mechanisms to protect personal data and demonstrate compliance.

Also: seek the advice of the **data protection officer** where one has been designated (Art. 35(2)); where appropriate, seek the **views of the people affected** or their representatives (Art. 35(9)); and if the DPIA indicates the processing would result in a high risk **in the absence of mitigating measures**, **consult the supervisory authority before processing** (Art. 36(1)). Record the outcome and who approved it.
