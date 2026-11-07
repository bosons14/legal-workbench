---
name: contract-drafting
description: This skill should be used when the user asks to "draft an NDA", "write a contract", "prepare an agreement", "draft a clause", "create a term sheet", "draft an MOU/LOI", "make a services/consultancy/employment/lease/licence/shareholders agreement", "draft an amendment/addendum", "convert this term sheet into an agreement", or needs any new contractual document or clause.
---

# Contract drafting

Draft contracts that are tailored, internally consistent and protective of the
client - not generic templates with the names swapped.

Plugin root is two levels above this skill's directory. Follow
`<plugin>/references/ground-rules.md`.

## 1. Take instructions (a short intake - ask in one go)
- Document type and **who we act for**
- Parties (full legal names, entity type, registered address, jurisdiction of incorporation)
- Commercial terms: what is exchanged, price/payment, term, key dates, deliverables
- Governing law and dispute forum (courts or arbitration seat/institution)
- Risk positions: liability cap, indemnities, IP ownership, exclusivity, non-compete
- Any precedent, template or playbook to follow (always prefer the client's own paper)
- Output format: .docx (default for lawyers - use the docx skill) or Markdown

If the user says "just draft it", use market-standard positions favouring our side,
then list every assumption at the top in a **Drafting note** box.

## 2. Structure
Use `structure.md` (this folder) for clause order by document type. Standard skeleton:
title -> date and parties -> recitals -> definitions and interpretation -> operative
clauses -> boilerplate -> signature blocks -> schedules.

## 3. Drafting rules
- **"shall"** for obligations, **"may"** for discretions, **"will"** only for future facts.
  Never "shall be entitled to endeavour".
- Define a term once, capitalise it, use it identically everywhere. No synonyms.
- One obligation per sentence where possible; actor + verb + object + deadline.
- Every obligation needs a time ("within 10 Business Days after...") and every
  discretion a standard ("acting reasonably", "in its sole discretion").
- Numbers: words and figures for money and key periods ("INR 5,00,000 (Rupees Five Lakh only)"
  in India; "USD 50,000 (fifty thousand US dollars)").
- Avoid ambiguous "and/or", "including" without "without limitation", undefined "material".
- Cross-references by clause number; re-check them all at the end.
- Square-bracket every unknown: `[PARTY B REGISTERED ADDRESS]`, and list them in the
  drafting note. Never invent facts.
- Jurisdiction-specific must-haves: stamp duty note and execution formalities (India),
  deed vs simple contract execution (UK), state-specific restrictions on
  non-competes/arbitration/consumer terms (US). Mark unverified points `[VERIFY]`.

## 4. Quality pass before handing over
1. Defined-terms audit: every capitalised term defined; every definition used.
2. Cross-reference and numbering audit.
3. Consistency: party names, amounts, dates, periods identical everywhere.
4. Read from the **other side's** perspective: where would they push back? Note it.
5. Run the `drafting-proofreader` agent on the draft for an independent check.

## 5. Deliver
Save to `work/<date>_<doc-type>_<parties>_v1.docx|md`. Lead with a drafting note:
assumptions, open points (bracketed items), positions taken and why, and points the
client must decide. For later rounds, produce a redline against the previous version
with `<plugin>/scripts/redline.py`.

## Clause library
`clauses.md` in this folder has balanced starting wording for common clauses with
pro-party variants. Adapt - never paste without fitting to the deal and law.
