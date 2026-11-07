---
name: matter-intake
description: This skill should be used when the user says "open a new matter", "new client", "set up a matter folder", "run a conflict check", "check conflicts for these parties", "add to the conflicts register", "set up confidentiality terms", "engagement letter", "client intake", or starts work on a new legal matter in an empty folder.
---

# Matter intake

Open a matter properly: conflicts cleared, confidentiality guard on, folder organised,
engagement documented.

Plugin root is two levels above this skill's directory.

## 1. Gather intake details
Client (legal name, contact, KYC docs where required), all other parties (adverse,
related, group companies, key individuals), matter description, jurisdiction, urgency
and known deadlines, fee basis, who is responsible.

## 2. Conflict check
The register lives at `.legal/conflicts.csv` in the user's practice folder (ask where,
default: the current project). Check **every** party name and alias:
```
python3 <plugin>/scripts/conflicts.py check "Client Name" "Adverse Party" "Group Co" --register PATH
```
Report CLEAR / POSSIBLE for each. A POSSIBLE hit - especially against an *adverse* role -
must go to the user for a decision; never decide a conflict yourself. After the user
confirms the matter is opened, add all parties:
```
python3 <plugin>/scripts/conflicts.py add "Name" --role client|adverse|related --matter M-YYYY-NNN --aliases "A|B"
```

## 3. Switch on the confidentiality guard
Create `<matter>/.legal/confidential-terms.txt` listing the client's name, counterparties,
individuals, project code names and other identifying terms, one per line
(`label=term` format, e.g. `client=Nimbus Software`). The plugin's hook will then block
any web search, web fetch or network command containing those terms, and
`redact.py --terms` uses the same file. Tell the user it is on and how to edit it.
Claude Code runs hooks from the project directory where the session started, so the
session should be started in the matter folder.

## 4. Create the folder structure
```
M-YYYY-NNN_<short-name>/
  .legal/confidential-terms.txt
  00_admin/        engagement letter, KYC, conflict record, fee notes
  01_client-docs/  originals as received (never edit; work on copies)
  02_correspondence/
  03_pleadings/    or 03_transaction-docs/
  04_research/
  05_evidence/
  work/            Claude's working drafts, reviews, chronologies
  MATTER.md        one-page matter summary (below)
```
Write `MATTER.md`: parties, our client, matter description, jurisdiction/forum, key
dates and deadlines (with computations), team, status, next steps. Keep it updated - it
is the first thing to read when resuming the matter.

## 5. Engagement letter (draft, if asked)
Scope (and exclusions), who is the client, team, fees and billing basis, expenses,
retainer, confidentiality, conflicts disclosure, data handling (including use of AI
tools and the safeguards in place), termination, complaints procedure, governing law.
Check local professional-conduct requirements (e.g. Bar Council of India rules restrict
advertising and solicitation; SRA rules in England require costs information) and
mark them `[VERIFY]`.
