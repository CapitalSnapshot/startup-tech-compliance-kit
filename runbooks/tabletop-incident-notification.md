# Tabletop exercise: who must be told, and by when

**Review label: community draft.** Decision support, not legal advice. **Get specialist advice** for real incidents. The expected answers follow Regulation (EU) 2016/679, Articles 4(7), 4(8), 4(12), 33 and 34 (official text, Official Journal L 119, 4 May 2016), and the walkthrough in [`incident-response.md`](incident-response.md).

<!-- kit-evidence: control=09 date=YYYY-MM-DD result=pass type=effectiveness -->

**Purpose:** show that staff can tell a **contractual** notification requirement from a **statutory controller deadline**, and know which role they are in.

**How to run it (60 to 90 minutes):** gather the incident lead, an engineer, the privacy contact and a senior decision-maker. Read one scenario aloud. Without looking at the answers, work through the runbook and fill in the decision log. Then compare with the expected answers, note every difference, and record what you changed. Use the facts as written; do not add facts.

---

## Scenario A: processor breach discovered

**Facts.** You run a SaaS product. You process your customers' end-user data on their behalf; each customer decides why and how its data is used. At 14:00 UTC on a Monday an engineer finds that a storage bucket was misconfigured and customer export files were readable by anyone with the link for the last six hours. Two customers are affected. The agreement with **Customer X** says you must notify it of a security incident **within 24 hours**. The agreement with **Customer Y** says **"without undue delay"** and names no number.

**Questions**
1. What is your role for this data?
2. Which 72-hour rule, if any, applies to you?
3. Who do you notify, by when, and who notifies the supervisory authority?
4. Which deadlines are contractual and which are statutory?

**Expected answers**
1. **Processor** (Art. 4(8)): you process on behalf of the customers, who are the controllers (Art. 4(7)).
2. **None.** The 72-hour period is in Art. 33(1) and is the **controller's** duty. Art. 33(2) says the processor notifies the controller **without undue delay after becoming aware**, with no number.
3. Notify **both customers** as soon as you have enough to tell them something useful: without undue delay, and inside Customer X's 24 hours. Do not wait until the 24 hours is nearly up. **Each customer decides** whether to notify its supervisory authority and the people affected. Do not do that for them unless they instruct you to and you have taken advice.
4. **Contractual:** Customer X's 24 hours. Customer Y's "without undue delay" is also written into the contract. **Statutory:** Art. 33(2), "without undue delay after becoming aware". The 24 hours is a contract term and does not replace or relax the statutory duty. Record which one applied to each notification.

**Self-check.** Did you record the awareness time (14:00) and how you decided it? Did you record the role per dataset? Did you log the notification times for each customer?

---

## Scenario B: controller breach, low risk

**Facts.** You are the controller of your own marketing contact list (business email addresses of 300 prospects). On Tuesday at 09:30 UTC a colleague mistakenly sends the list to an internal mailing group of 40 colleagues, who are bound by confidentiality. The colleague spots the error at once and recalls the message; mail logs show it was opened by 6 colleagues. The data is not encrypted in the email.

**Questions**
1. What is your role, and is this a personal data breach?
2. Must you notify the supervisory authority? What must you record?
3. Must you tell the 300 people?
4. When did any clock start?

**Expected answers**
1. **Controller.** Yes, it is a personal data breach: an unauthorised disclosure (Art. 4(12)) to people not meant to receive it.
2. **Possibly not, but you must decide and document it.** Art. 33(1) requires notification **unless the breach is unlikely to result in a risk to people's rights and freedoms**. Here an assessment may reasonably conclude that it is unlikely, because the recipients are internal and bound by confidentiality, the list is business emails only, and the message was recalled. If you decide not to notify, **document the facts, effects, remedial action and the reason** (Art. 33(5)). If you are unsure, take advice or notify.
3. **Probably not.** Communication to people is required when the breach is **likely to result in a high risk** (Art. 34(1)). Record why you concluded it is not.
4. The 72 hours counts from **becoming aware** (09:30 Tuesday, when the colleague spotted it), even if you later decide no notification is needed. Make the assessment and write it down well inside that time.

**Self-check.** Is there a written assessment and reason? Is the breach in the register even though it was not notified?

---

## Scenario C: controller breach, high risk to individuals

**Facts.** You are the controller of your customers' account data. On Friday at 17:30 UTC you learn that a laptop holding an **unencrypted** export of 12,000 user accounts (names, email addresses, hashed passwords and the last login location) was stolen from a car. You do not yet know if the export has been accessed.

**Questions**
1. When does the clock start, and when is the 72-hour point?
2. Can you wait until Monday morning for the supervisory authority?
3. Do you have to tell the 12,000 people? Does any exception apply?
4. What if you cannot complete the notification in time?

**Expected answers**
1. The clock starts at **awareness: Friday 17:30 UTC**. The 72-hour point is **Monday 17:30 UTC**. The period is counted in hours; the text does not say working days, so the weekend counts.
2. You may be able to, but the duty is to notify **without undue delay**, and where feasible within 72 hours (Art. 33(1)). Do not plan around the deadline. Start Friday evening.
3. Assess whether the breach is **likely to result in a high risk** (Art. 34(1)). Credentials and location data on an unencrypted device may point that way; this is a judgement to document, with advice. If it is likely high risk, you must communicate to the people **without undue delay**. The encryption exception (Art. 34(3)(a)) **does not apply**, because the data was not protected. Exception (b) applies only if subsequent measures actually ensure the high risk is no longer likely to materialise; for example forcing a password reset may help, but it does not remove the risk from exposed location data, so record your reasoning. Exception (c), disproportionate effort, would need a public communication instead, and is unlikely to fit 12,000 identified users.
4. **Notify in phases** (Art. 33(4)) rather than wait for full information, and if you are later than 72 hours, include **reasons for the delay** (Art. 33(1)).

**Self-check.** Did you separate the statutory 72-hour period from any deadline in a customer contract? Did you use the decision log? Did you assess Art. 34 separately from Art. 33?

---

## After the exercise

Record the date, who took part, which scenarios, the times, what differed from the expected answers and what you changed (runbook, contacts, contracts). Save it as evidence for control 09 with `type=effectiveness` ([`../evidence/README.md`](../evidence/README.md)).
