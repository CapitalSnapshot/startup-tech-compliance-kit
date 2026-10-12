# GDPR territorial scope: screening worksheet

> **Standing notice.** This is repository based, community maintained guidance. It is not legal advice, a formal compliance assessment, a certification or an independent security audit. Mappings and statements about frameworks are unverified unless their review label says otherwise ([review labels](../docs/review-labels.md)).

**Review label: community draft.** Proposed guidance. It has not been reviewed by a maintainer or by a specialist. It is decision support, not legal advice, and it never concludes that you are, or are not, subject to the GDPR. **Get specialist advice** for anything that matters.

Sources used: Regulation (EU) 2016/679 (GDPR), Article 3 (territorial scope) and Article 27 (representatives), official text as published in the Official Journal of the European Union, L 119, 4 May 2016. Further reading: EDPB, *Guidelines 3/2018 on the territorial scope of the GDPR (Article 3)*, version adopted after public consultation, 12 November 2019. The guidelines were identified but their content was not reviewed for this worksheet; no specific point in them is relied on here (source verification pending).

<!-- kit-evidence: control=08 date=YYYY-MM-DD result=pass type=operational -->

## The main point

**Where the people are is not the only test.** The GDPR can apply because of where you (or a group company) are established, or, if you are not established in the Union, because of what you do toward people who are in the Union. These are different routes with different questions.

| Route | What Article 3 says, in short | Where the data subject is |
|---|---|---|
| **Establishment** (Art. 3(1)) | Applies to processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, **whether or not the processing takes place in the Union** | Not a condition. The data subjects can be anywhere |
| **Offering goods or services** (Art. 3(2)(a)) | Applies to a controller or processor **not established in the Union** processing personal data of data subjects who are in the Union, where the processing relates to offering goods or services to them, **irrespective of whether a payment is required** | In the Union, **and** the offering link must be present |
| **Monitoring behaviour** (Art. 3(2)(b)) | Same, where the processing relates to monitoring their behaviour **as far as that behaviour takes place within the Union** | In the Union, **and** the monitoring link must be present |
| **Public international law** (Art. 3(3)) | Applies to a controller not established in the Union but in a place where Member State law applies by virtue of public international law | Not the usual startup case |

Having a customer or user who happens to be in the Union does not by itself settle which route applies, or whether any does.

## 1. Record the facts

Complete this before using the tree. Update it when the facts change.

| Fact | Answer |
|---|---|
| Legal entities and where each is established (including group companies, branches, offices, agents) | <...> |
| Which entity decides the purposes and means of the processing (controller), and which processes on another's behalf (processor)? | <...> |
| The processing activities concerned | <...> |
| Where the data subjects are (countries) | <...> |
| Do you direct your service at people in the Union? Evidence: languages, currencies, EU domains, marketing, delivery or sign-up in the Union, named EU customers | <...> |
| Do you track or profile people's behaviour that takes place in the Union (analytics, cookies, device tracking, behavioural advertising)? | <...> |
| Jurisdictions relevant to this decision | <...> |

## 2. Decision tree

Take the questions in order and stop at the first that points to "may apply". Record the answer and the reason for each.

1. **Establishment in the Union.** Does the controller or the processor have an establishment in the Union, and is the personal data processed in the context of that establishment's activities?
   - **Yes or probably:** GDPR **may apply** under Article 3(1), wherever the processing takes place and wherever the data subjects are. Go to step 5.
   - **No:** go to 2.
   - **Unsure what counts as an establishment, or whether the processing is in its context:** **needs advice**. Go to step 6.
2. **Offering to people in the Union.** You have no EU establishment. Are you offering goods or services (paid or free) to people in the Union?
   - **Yes or probably:** GDPR **may apply** under Article 3(2)(a). Go to step 4, then 5.
   - **No:** go to 3.
   - **Unsure whether your offering is directed at people in the Union:** **needs advice**. Go to step 6.
3. **Monitoring behaviour in the Union.** Do you monitor the behaviour of people, where that behaviour takes place in the Union?
   - **Yes or probably:** GDPR **may apply** under Article 3(2)(b). Go to step 4, then 5.
   - **No:** go to the unusual cases below.
   - **Unsure:** **needs advice**. Go to step 6.
4. **EU representative (Article 27).** Where Article 3(2) may apply, Article 27(1) requires a controller or processor to designate in writing a representative in the Union. Article 27(2) lists exceptions: (a) processing which is occasional, does not include on a large scale special-category data (Art. 9(1)) or criminal conviction and offence data (Art. 10), and is unlikely to result in a risk to people's rights and freedoms, taking into account the nature, context, scope and purposes; and (b) a public authority or body. Whether an exception fits is a judgement. **Record whether a representative is needed and who decided.** Take advice.
5. **If it may apply:** follow [`../privacy/`](../privacy/) and record the route, the reasons and who decided.
6. **Needs advice:** route to legal review. Record the question you are asking, who you asked and the date.

**Unusual cases.** If none of the questions fits (for example a public body, a diplomatic or consular setting, processing connected to Article 3(3), or an arrangement spread across several entities), **route to legal review**. Do not conclude from the absence of a match.

## 3. Outcomes

Only these outcomes are valid. None is a legal conclusion.

| Outcome | Meaning | Next |
|---|---|---|
| **GDPR may apply (Art. 3(1))** | Establishment route | Privacy process; record the decision |
| **GDPR may apply (Art. 3(2)(a) or (b))** | Non-EU route: offering or monitoring | Privacy process; decide on a representative (Art. 27) |
| **Needs advice** | Facts or law unclear | Legal review; do not proceed on an assumption |
| **No route identified on the facts recorded** | You answered no to every question on facts you can support. **This is not a finding that the GDPR does not apply** | Write the facts and the reasoning; set a review date; recheck on any change (for example you start marketing in the Union, add tracking, open an EU office, take an EU customer on whose behalf you process data) |

## 4. Record the decision

| Item | Entry |
|---|---|
| Route and outcome | <...> |
| Reasons, with the facts relied on | <...> |
| Was an EU representative considered? Outcome | <...> |
| Advice taken (who, date) | <...> |
| Decision owner (role) | <...> |
| Date | <YYYY-MM-DD> |
| Review date and triggers | <YYYY-MM-DD>, and on any change in the facts above |

Related: [`applicability-matrix.md`](applicability-matrix.md), [`questionnaire.md`](questionnaire.md), [`../privacy/README.md`](../privacy/README.md).
