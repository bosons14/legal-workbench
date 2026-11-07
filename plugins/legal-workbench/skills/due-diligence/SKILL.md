---
name: due-diligence
description: This skill should be used when the user asks to "do due diligence", "review the data room", "prepare a DD report", "red flag report", "legal diligence on the target", "review these contracts for change of control", "check title documents", "vendor due diligence", "investment diligence", or needs a large set of contracts and corporate documents reviewed against a checklist.
---

# Legal due diligence

Review a data room systematically and produce a red-flag report a deal team can act on.

Plugin root is two levels above this skill's directory. Follow
`<plugin>/references/ground-rules.md`.

## 1. Scope
- Transaction type (share purchase, asset purchase, investment, merger, lending, JV)
  and who we act for (buyer/investor/lender vs seller)
- Target entity/entities and jurisdictions
- Materiality threshold (e.g. contracts above INR/USD X; litigation above Y)
- Areas in scope (from `checklist.md`, this folder) and report format (red-flag only vs full)
- Deadline and any specific concerns from the client

## 2. Index the data room
Walk the folder; extract text from every file (`<plugin>/scripts/extract_text.py`).
Build `work/dd/index.csv`: folder ref, file, document type, parties, date, reviewed (Y/N).
Flag unreadable/scanned files and missing documents against the request list.

## 3. Review
For each area in `checklist.md`, review the documents and record findings in a
**findings register** (`work/dd/findings.csv`):
`Ref | Area | Document | Finding | Risk (Red/Amber/Green) | Recommendation (CP / indemnity / warranty / price / disclosure / post-closing) | Source`

Contract sweeps: for every material contract capture - parties, term/expiry, value,
**change of control / assignment**, exclusivity, non-compete, termination for
convenience, liability cap, governing law, unusual indemnities, consents needed.
For 50+ contracts, split into batches for parallel subagents with the same template.

## 4. Report
`work/dd/<date>_DD-report_<target>.md|docx`:
1. Executive summary - deal-breakers, key Red flags, and recommended protections
2. Scope, documents reviewed, limitations and assumptions (what wasn't provided)
3. Findings by area (Red first), each with source references
4. Recommended deal protections: conditions precedent, specific indemnities, warranties,
   price adjustments, escrows, post-closing undertakings
5. Annexures: document index, contract summary table, outstanding requests list

Red = could prevent closing, materially affect value, or create significant liability;
Amber = needs a contractual protection or follow-up; Green = noted, no action.
