---
name: case-chronology
description: This skill should be used when the user asks to "build a chronology", "make a timeline of events", "list of dates", "summarise these documents by date", "what happened when", "prepare a dramatis personae", "case summary from the file", or hands over a bundle of emails, letters, contracts or pleadings and needs the facts organised.
---

# Case chronology, cast list and fact summary

Turn a pile of documents into a sourced chronology - the backbone for pleadings,
submissions, witness preparation and settlement.

Plugin root is two levels above this skill's directory.

## 1. Ingest
For each document in the bundle (or folder the user names):
```
python3 <plugin>/scripts/extract_text.py DOC --numbered -o work/text/<n>_<name>.txt
```
Assign each document an ID (`D1`, `D2`...) and keep a **document index**: ID, file name,
type, date, author, recipient, one-line description. Scanned PDFs with no text need
OCR first - tell the user which ones.

For large bundles (20+ documents), process in batches; for 100+ consider parallel
subagents each producing rows in the same format, then merge and de-duplicate.

## 2. Extract events
For every event: date (normalise to YYYY-MM-DD; keep the original form if ambiguous
- "03/04/2025" is 3 April in India/UK and March 4 in the US: flag it), time if relevant,
actors, what happened, source pinpoint `[D7, P12]`, and significance.
- Capture **communications** (who told whom what, when) and **knowledge** (when a party
  knew a fact - crucial for limitation and notice).
- Note contradictions between documents explicitly - they are often the case.
- Undated events: place by inference and mark `~` with reasoning.

## 3. Outputs (save under `work/`)
1. **Chronology** - `chronology.md` (and `.csv` for spreadsheets):
   `Date | Event | Actors | Source | Significance | Disputed?`
2. **Dramatis personae** - every person/entity: role, organisation, relationship to the
   parties, documents in which they appear.
3. **Key issues map** - for each issue in dispute, the events and documents that help
   and hurt our client.
4. **Gaps and questions** - missing documents (referenced but not in the bundle),
   periods with no evidence, questions for the client.
5. **List of dates** (court format, India SC/HC style) if a filing is planned: concise,
   numbered, neutral in tone, each with annexure reference.
6. **Limitation flags** - triggering events and computed deadlines via
   `<plugin>/scripts/limitation.py`.

Keep the chronology neutral and factual; put argument in "Significance".
