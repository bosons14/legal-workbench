---
name: witness-prep
description: This skill should be used when the user asks to "prepare for cross-examination", "draft cross-examination questions", "examination-in-chief", "prepare a witness", "deposition outline", "evidence affidavit", "witness statement", "hearing preparation", "anticipate the judge's questions", "moot/argument prep", or is preparing for a hearing, trial, deposition or arbitration evidentiary session.
---

# Witness and hearing preparation

Plugin root is two levels above this skill's directory. Build on the matter chronology
(`case-chronology` skill) - every question and every proposition must be pinned to a document.

## Cross-examination outline
1. **Objectives**: list the 3-6 admissions you need from this witness, tied to issues in dispute.
2. For each objective, a **chapter** of short, leading, one-fact questions that build to the
   admission ("You signed the letter dated 3 March? / You read it before signing? / It says
   delivery was complete?"), each with the document pinpoint to confront the witness with.
3. **Impeachment** material: prior inconsistent statements (pleadings, emails, earlier
   affidavits), with exact quotes and locations.
4. **Danger zones**: open questions to avoid; topics where the witness can hurt us.
5. Order chapters for impact - strong start, strong finish.
Respect local rules (e.g. India: BSA ss.142-146 on leading questions and cross-examination
[VERIFY section numbers]; US: FRE 611; arbitration: the tribunal's procedural order).

## Examination-in-chief / witness statement / evidence affidavit
- In the witness's own words and knowledge; first person; chronological; numbered paras;
  exhibits referenced. Never put words into a witness's mouth or coach false evidence -
  preparation explains process and refreshes memory from documents; it does not script answers.
- Separate what the witness saw/did from what they were told (hearsay).

## Preparing our witness
Explain the process, demeanour, "listen to the question, answer only that, it's fine to
say you don't remember". Run a mock cross using the `opposing-counsel` agent to generate
the hardest questions the other side will ask, then review truthful, accurate answers.

## Oral argument / hearing bundle
- 1-page **argument outline**: relief sought, 3 key points, best authority for each, answer
  to the opponent's best point.
- **Judge's questions**: the 10 hardest questions the bench is likely to ask, with short answers.
- Hearing bundle index: pleadings, key documents (with page refs), authorities, chronology.
