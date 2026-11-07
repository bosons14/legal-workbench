---
name: legal-research
description: This skill should be used when the user asks a legal question that needs research - "what is the law on", "can my client", "is this enforceable", "find case law on", "research memo", "what are the precedents for", "what does section X say", "has this been overruled", "compare the position in India and the UK" - or asks for a research memo, opinion draft, or brief on a point of law.
---

# Legal research and memos

Answer legal questions with verified authority, structured so a lawyer can rely on
the reasoning and check every source in minutes.

Plugin root is two levels above this skill's directory. Follow
`<plugin>/references/ground-rules.md` - especially **never invent authority** and
**never put client names into searches**. Citation formats and primary sources per
jurisdiction: `<plugin>/references/jurisdictions.md`.

## 1. Frame the question
Write down, and confirm with the user if unclear:
- the precise legal question(s) - split compound questions
- jurisdiction, forum, and relevant date (law at the time of the facts vs today)
- the material facts (anonymised), and which side we are on
- what the answer is for: advice, a pleading, a negotiation, an opinion

## 2. Research plan
1. **Statute first.** Locate the current text of the governing provision from an official
   source; check amendments, commencement, and whether it has been replaced
   (e.g. IPC -> BNS). Read definitions and exceptions in the same Act.
2. **Leading authorities.** Find the apex-court and binding appellate decisions. For each:
   holding, key reasoning (pinpointed), and whether it is still good law (later
   overruling, distinguishing, larger-bench references, legislative reversal).
3. **Adverse authority.** Actively search for decisions going the other way. A memo
   that hides bad law is useless; the duty of candour applies before courts.
4. **Secondary sources** (commentaries, law-firm notes) only to find primary authority.
5. Search generically: describe the legal issue, never the client or counterparty.

Run several distinct searches; WebFetch the actual judgment or statute page rather
than relying on snippets. Record each source's URL.

## 3. Write the memo (IRAC, numbered)
Save to `work/<date>_memo_<topic>.md`:

```
PRIVILEGED & CONFIDENTIAL - ATTORNEY WORK PRODUCT / PREPARED FOR LEGAL ADVICE
To / From / Date / Re
1. Question(s) presented
2. Short answer (yes / no / probably - with one-paragraph reasons)
3. Facts relied on (and assumptions)
4. Applicable law
   4.1 Statute (quoted precisely, with section numbers and current status)
   4.2 Case law (holding + pinpoint; binding vs persuasive)
5. Analysis - apply law to facts; address counter-arguments and adverse authority
6. Risks, open points, and facts that would change the answer
7. Recommendation / next steps
Table of authorities (every source with citation, court, date, URL, verified Y/N)
```

## 4. Verify before handing over
- Every citation in the memo appears in the table of authorities with a source you
  actually retrieved, or is marked `[VERIFY]`.
- For important or court-bound work, run the `citation-verifier` agent: it checks
  each citation independently.
- State plainly what you could not access (paywalled reporters such as SCC Online,
  Manupatra, Westlaw, Lexis) and suggest the user confirm there.

## Quick answers
If the user wants a quick answer, not a memo: give the short answer, the 2-3 key
authorities with links, and the main caveat - in under 200 words - and offer the full memo.
