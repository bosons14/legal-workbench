---
name: citation-check
description: This skill should be used when the user asks to "check the citations", "verify these cases", "are these authorities real", "cite-check this brief", "Bluebook/OSCOLA/SCC format these citations", "is this case still good law", "check the quotes in my submission", or before filing any brief, petition, written submission, or opinion that cites authority - including documents drafted by AI tools.
---

# Citation check

Courts have sanctioned lawyers for filing AI-hallucinated citations. This skill
checks every authority in a document is **real, correctly cited, accurately
described, and still good law**.

Plugin root is two levels above this skill's directory. For citation formats see
`<plugin>/references/jurisdictions.md`.

## Procedure
1. **Extract** the document text with paragraph numbers:
   `python3 <plugin>/scripts/extract_text.py FILE --numbered -o work/cite-src.txt`
2. **Inventory every authority**: cases, statutes/sections, rules, regulations,
   treaties, secondary sources, and every direct quotation. Record the `[P#]` where each appears.
3. **Verify each one** by retrieving it (WebSearch + WebFetch on official or reputable
   sources). For each, check:
   - **Exists:** the case/statute is real; parties, year, court match.
   - **Citation correct:** reporter, volume, page, neutral citation; pinpoint page/para exists.
   - **Proposition supported:** the authority actually says what the document claims it
     says - read the cited paragraph, not just the headnote.
   - **Quotation exact:** word-for-word match, with ellipses and alterations marked.
   - **Still good law:** not overruled, reversed, stayed, referred to a larger bench, or
     superseded by amendment; statute section not repealed/renumbered.
   - **Format:** matches the required style (Bluebook / OSCOLA / Indian SCC-AIR-neutral / court's own practice direction).
4. For large documents, have the `citation-verifier` agent check authorities in
   parallel batches; it works without seeing your conclusions.

## Output
Save `work/<date>_cite-check_<doc>.md`:

| # | Location | Citation as written | Status | Problem | Corrected citation / note | Source URL |
|---|----------|--------------------|--------|---------|---------------------------|-----------|

Status values: **OK**, **FORMAT** (real, minor citation error), **MISDESCRIBED**
(real but doesn't support the proposition), **QUOTE** (quotation inaccurate),
**BAD LAW** (overruled/superseded), **NOT FOUND** (could not locate - treat as possibly
fabricated), **UNVERIFIED** (exists behind a paywall you couldn't access).

Lead with a one-line verdict: "Safe to file" / "Fix N issues before filing", and list
NOT FOUND and MISDESCRIBED items first - those are the dangerous ones. Never mark an
item OK unless you retrieved it.
