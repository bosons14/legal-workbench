# ⚖️ legal-workbench

**A legal workbench for Claude Code.** Contract review and drafting, research memos with
verified citations, litigation drafting, chronologies, due diligence, limitation
calculations, redlines, redaction and conflict checks - with a built-in guardrail that
stops client-confidential names from leaking into web searches.

Built for lawyers, in-house counsel, paralegals and law students. India, US and
England & Wales are covered out of the box; other jurisdictions work with research.

> **Not legal advice.** legal-workbench produces drafts and analysis for a qualified lawyer
> to review. It is designed to *never invent authority*: unverified citations are marked
> `[VERIFY]`, and computed deadlines are always flagged for checking.

---

## Install

In Claude Code:

```
/plugin marketplace add bosons14/legal-workbench
/plugin install legal-workbench@legal-workbench
```

Requirements: Python 3.9+ (standard library only). `pdftotext` (poppler) to read PDFs.
Optional: the `docx` skill for Word output with tracked changes.

---

## What's inside

### Slash commands

| Command | What it does |
|---|---|
| `/review-contract <file> [for <party>]` | Clause-by-clause risk review, issues table, fallback wording |
| `/draft <type> [details]` | Contracts, clauses, plaints, petitions, written statements, affidavits, legal notices |
| `/research <question>` | IRAC research memo with table of authorities (or `quick` answer) |
| `/cite-check <file>` | Verifies every citation and quotation before filing |
| `/deadline <action> <date>` | Limitation / procedural deadline with full working |
| `/chronology <folder>` | Sourced chronology, cast list, issues map, list of dates |
| `/compare <old> <new>` | Redline + explanation of every substantive change; catches silent edits |
| `/redact <file> [pseudo]` | Masks or pseudonymises PII and confidential names |
| `/new-matter <parties - description>` | Conflict check, confidentiality guard, matter folder, MATTER.md |
| `/stress-test <file>` | Opposing counsel attacks your draft before the other side does |
| `/explain <file or topic>` | Plain-language client explanation of a judgment, order or contract |

### Skills (load automatically when relevant)

`contract-review` · `contract-drafting` (with clause library) · `legal-research` ·
`citation-check` · `litigation-drafting` (India / US / UK skeletons, s.138 NI Act notices) ·
`case-chronology` · `due-diligence` (full DD checklist) · `legal-deadlines` ·
`document-compare` · `redaction` · `matter-intake` · `client-communication` ·
`witness-prep` (cross-examination chapters, mock cross) · `compliance-check`
(DPDP Act 2023, GDPR, POSH, e-commerce rules) · `billing-narratives`

### Agents (independent reviewers)

- **opposing-counsel** - attacks a draft from the other side: procedural objections, factual
  gaps, adverse authority, negotiation counters.
- **citation-verifier** - independently checks citations exist, say what they are cited for,
  are quoted exactly, and are still good law. Run several in parallel on long briefs.
- **drafting-proofreader** - defined terms, cross-references, numbering, parties, amounts,
  placeholders, annexures.

### Tools (pure Python, run locally)

| Script | Purpose |
|---|---|
| `scripts/extract_text.py` | Text from .docx / .pdf / .html / .txt, with `[P#]` paragraph numbers for pinpointing |
| `scripts/redline.py` | Paragraph-aligned, word-level redline to Markdown or HTML |
| `scripts/redact.py` | Masks/pseudonymises email, phone, Aadhaar (Verhoeff-checked), PAN, GSTIN, IFSC, SSN, cards (Luhn-checked), IBAN, IP + custom terms; writes a privileged key |
| `scripts/limitation.py` | Deadline calculator - excludes trigger day, adds excluded time, rolls past weekends/court holidays; presets for the Limitation Act 1963, NI Act s.138, Arbitration Act s.34, CPC, FRCP/FRAP, Limitation Act 1980, CPR |
| `scripts/conflicts.py` | Fuzzy conflict check against a local register (handles Pvt Ltd / LLP / Inc variants, aliases) |

### 🔒 Confidentiality guard (hook)

Put client and counterparty names in `.legal/confidential-terms.txt` in the matter folder:

```
client=Nimbus Software
adverse=Acme Holdings
person=Ravi Kumar
project=Project Falcon
```

Before every `WebSearch`, `WebFetch` or network command in Bash, the hook checks the outgoing
query and **blocks the call** if it contains any of those terms, telling Claude to search the
legal issue generically instead. The same file feeds `redact.py --terms`. No file, no blocking.

---

## Ground rules the plugin enforces

1. The lawyer decides - everything is a draft.
2. Never invent authority - retrieve it or mark it `[VERIFY]`.
3. Client names never go into external searches.
4. Jurisdiction first.
5. Pinpoint every fact to a document.
6. Deadlines are always flagged for verification.

See [`references/ground-rules.md`](plugins/legal-workbench/references/ground-rules.md) and
[`references/jurisdictions.md`](plugins/legal-workbench/references/jurisdictions.md).

## Typical workflow

```
cd ~/matters
claude
> /new-matter Nimbus Software vs Acme Holdings - recovery of unpaid licence fees
> cd M-2026-014_nimbus-acme   (restart Claude here so the guard uses this matter's terms)
> /chronology 01_client-docs/
> /deadline suit for recovery of licence fees, invoice due 2024-02-10, India
> /draft plaint for recovery, Commercial Court, Delhi
> /stress-test 03_pleadings/plaint-v1.docx we act for plaintiff
> /cite-check 03_pleadings/plaint-v2.docx
```

## Contributing

Issues and PRs welcome - especially jurisdiction packs (Singapore, Australia, Canada, UAE,
Kenya, Nigeria...), more limitation presets, and court-specific templates. Please cite the
statute or rule for every preset or template you add.

## License

MIT © Subhendra Basu
