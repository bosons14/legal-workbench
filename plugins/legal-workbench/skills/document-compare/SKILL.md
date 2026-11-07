---
name: document-compare
description: This skill should be used when the user asks to "compare these two versions", "redline", "what changed between v2 and v3", "blackline", "did they sneak in any changes", "compare the draft with the signed copy", "summarise the other side's markup", or provides two versions of a contract, pleading, or policy.
---

# Document comparison

Show exactly what changed between two versions and explain why it matters.

Plugin root is two levels above this skill's directory.

## Run the comparison
```
python3 <plugin>/scripts/redline.py OLD NEW --changes-only            # markdown, changes only
python3 <plugin>/scripts/redline.py OLD NEW -f html -o work/redline.html   # full visual redline
```
Accepts .docx, .pdf, .txt, .md, .html. For a .docx with tracked changes, the extractor
reads the current (accepted-insertions, deletions-removed) text - so compare against the
earlier clean version to see the changes in context.

## Explain the changes
Never just hand over a diff. Produce a **change summary** (`work/<date>_changes_<doc>.md`):
`# | Clause | Change | Effect on our client | Accept / Reject / Counter | Suggested response`

- Separate **substantive** changes (rights, obligations, money, risk, time, law/forum)
  from **drafting** changes (typos, renumbering, style).
- Hunt for **silent changes**: changes the other side did not flag in their cover email
  or that appear outside tracked changes - compare against the last version *you* sent,
  not their marked-up copy. Call these out at the top.
- Check knock-on effects: a changed definition alters every clause that uses it; list them.
- Before signing: compare the execution version against the last agreed draft; any
  difference is a red flag until explained.

To produce a .docx with genuine tracked changes, use the docx skill with the revised text.
