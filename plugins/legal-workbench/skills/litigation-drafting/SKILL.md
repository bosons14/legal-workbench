---
name: litigation-drafting
description: This skill should be used when the user asks to draft court or tribunal documents - "draft a plaint", "written statement", "reply/rejoinder", "writ petition", "bail application", "SLP", "complaint", "appeal memo", "affidavit", "interim application", "stay application", "written submissions", "synopsis and list of dates", "motion to dismiss", "particulars of claim", "defence", "witness statement", "legal notice", "demand letter", "cease and desist", "Section 138 cheque bounce notice", or "reply to legal notice".
---

# Litigation drafting

Draft pleadings, applications, submissions and notices that comply with the forum's
rules, are anchored to the documents, and make the client's strongest case.

Plugin root is two levels above this skill's directory. Follow
`<plugin>/references/ground-rules.md`. Court structures and citation forms:
`<plugin>/references/jurisdictions.md`. Forum-specific skeletons: `templates.md` (this folder).

## 1. Intake
- Forum (court/tribunal, bench, original/appellate side), case type, case number if any
- Who we act for; parties with full descriptions (age, parentage/occupation and address
  as Indian practice requires; corporate details)
- Cause of action: facts with dates, and the documents proving each fact
- Relief sought (final and interim)
- Limitation: compute with `<plugin>/scripts/limitation.py` and show the computation
  in the draft's limitation paragraph and in your note to the user
- Jurisdiction: pecuniary, territorial, subject-matter - one paragraph each, with facts
- Valuation and court fee (India: per state Court Fees Act and Suits Valuation Act)
- For replies/defences: the document being answered (read it paragraph by paragraph)

## 2. Build the factual spine first
Create (or reuse) the matter chronology (`case-chronology` skill). Every factual
averment in the draft must trace to a document or to client instructions. Mark facts
from client instructions not yet backed by a document as `[CLIENT TO CONFIRM]`.

## 3. Draft
- Follow the forum's format exactly: cause title, memo of parties, index, synopsis and
  list of dates (SC/HC), numbered paragraphs, grounds (lettered A, B, C... in Indian
  petitions), prayer, verification, affidavit, annexure labels (P-1/A-1/Exhibit 1),
  certificate requirements (e.g. India: certificate under s.63 BSA / formerly s.65B Evidence
  Act for electronic evidence [VERIFY current form]).
- **Replies / written statements:** answer every paragraph of the other side - admit,
  deny, or "not admitted / no knowledge"; preliminary objections first (limitation,
  jurisdiction, maintainability, non-joinder, suppression, arbitration clause); then
  parawise reply; then additional facts. Evasive denials are deemed admissions in
  many systems (India: O. VIII r.3-5 CPC [VERIFY]).
- **Grounds / arguments:** strongest first; each ground = proposition + facts + authority.
  Authority must be verified (see `citation-check`), else `[VERIFY]`.
- **Legal notices:** sender's advocate letterhead; "Under instructions from and on behalf of
  my client..."; facts; legal basis; specific demand with a deadline; consequence; reservation
  of rights. For s.138 NI Act notices see `templates.md` - statutory timelines are strict.
- Tone: firm, factual, no adjectives that can't be proved, no threats beyond lawful action.

## 4. Check and deliver
- Cross-check every date, amount and name against the chronology and documents.
- Annexure list matches the references in the text, in order.
- Run the `opposing-counsel` agent to find weaknesses before filing; fix or pre-empt them.
- Run `citation-check` if authorities are cited.
- Save as .docx (via docx skill) - courts and lawyers work in Word - plus a short covering
  note listing: limitation computation, court fee, annexures to collect, and items marked
  `[CLIENT TO CONFIRM]` / `[VERIFY]`.
