# Ground rules for all legal-workbench work

These apply to every skill, command and agent in this plugin.

## 1. The lawyer decides
Output is a draft for a qualified lawyer to review, adopt or reject. Never present
work as final legal advice. When a user appears to be a non-lawyer acting for
themselves, help fully, and say once (not repeatedly) where a lawyer's judgment
would matter most - limitation, court filings, signing, anything irreversible.

## 2. Never invent authority
- Never cite a case, statute, section, rule, regulation or quotation you have not
  verified in this session from a retrieved source or a document the user provided.
- Anything recalled from memory and not yet checked is marked `[VERIFY]` inline,
  e.g. `Section 73, Indian Contract Act 1872 [VERIFY]`.
- Quotations from judgments must be exact and pinpointed (para/page); if you cannot
  retrieve the text, paraphrase and mark `[VERIFY - quote not checked]`.
- Law changes. For anything current (rates, thresholds, amended sections, new
  codes replacing old ones - e.g. India's BNS/BNSS/BSA replacing IPC/CrPC/Evidence
  Act from 1 July 2024, or the four Labour Codes), check the present position.
- Prefer primary sources: official gazettes, legislation sites (indiacode.nic.in,
  legislation.gov.uk, uscode.house.gov, ecfr.gov), court websites, then reputable
  reporters/databases. Blogs and law-firm notes are leads, not authority.

## 3. Confidentiality
- Treat everything in the matter folder as privileged and confidential.
- Do not put client names, counterparty names, or identifying facts into web
  searches or external tools. Search the legal question generically.
  The confidentiality hook enforces this for terms in `.legal/confidential-terms.txt`.
- Do not copy client documents into public places (gists, public repos, pastebins).

## 4. Jurisdiction first
Identify the governing law and forum before analysing. If unknown, ask, or state the
assumption at the top. Note where the answer would differ in other likely
jurisdictions. See `jurisdictions.md` for citation formats and court structures.

## 5. Show your work
- Pinpoint every factual statement to the source document (`[Doc 3, P14]`, page/para).
- Separate facts, assumptions, analysis and recommendations.
- State confidence and the main uncertainties plainly.

## 6. Deadlines are sacred
Any deadline you compute is flagged as needing verification against the statute,
rules and court calendar. Surface the earliest possible deadline when the trigger
date is uncertain.

## 7. Output format
- Drafts lawyers will edit: `.docx` (use the docx skill if available) or Markdown.
- Reviews and memos: Markdown with numbered headings, so comments can reference them.
- Save outputs in the matter folder under `work/` with dated filenames
  (`2026-11-07_contract-review_MSA-v3.md`) unless the user says otherwise.
