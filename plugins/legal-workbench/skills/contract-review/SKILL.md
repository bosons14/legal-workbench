---
name: contract-review
description: This skill should be used when the user asks to "review this contract", "check this agreement", "what are the risks in this NDA/MSA/SaaS/lease/employment agreement", "mark up this contract", "is this clause standard", "prepare an issues list", "negotiate this contract", or shares a contract and asks for comments, redlines or a negotiation position for either side.
---

# Contract review

Produce a clause-by-clause risk review from the perspective of **one named party**,
with concrete fallback language and a prioritised issues list. A good review reads
like a senior associate's work: it is specific to this contract, tells the client what
matters most, and gives wording ready to send to the other side.

Plugin root is two levels above this skill's directory. Read
`<plugin>/references/ground-rules.md` once per session before starting.

## 1. Set up (ask only what you can't infer)
- **Who we act for** and their role (supplier/customer, licensor/licensee, employer...).
  Never review "neutrally" unless asked - risk depends on the side.
- **Governing law and forum** (from the contract, else ask/assume and say so).
- **Deal context:** value, leverage, deal stage (first draft / their paper / final
  sign-off), any must-haves or a client playbook. If the user has a playbook file,
  apply it and cite its rule numbers; deviations from playbook are the headline.
- **Depth:** quick risk scan (top 10 issues, one page) vs full review.

## 2. Read the document properly
```
python3 <plugin>/scripts/extract_text.py CONTRACT.docx --numbered -o work/contract.txt
```
Use the `[P#]` paragraph numbers and the contract's own clause numbers in every comment.
Read the **whole** contract including schedules, annexures and incorporated documents
(terms on a URL, policies, SOWs). Note anything incorporated by reference that you
have not seen - it can override the main text.

## 3. Check systematically
Work through `checklist.md` (in this skill's folder). For each topic, record: what the
clause says, why it matters for our side, risk rating, and a fix.

Also check the drafting itself:
- defined terms used but not defined, defined but unused, or used inconsistently
- broken cross-references and numbering
- inconsistencies between body, schedules and order forms; order-of-precedence clause
- obligations without a deadline or standard ("shall endeavour" vs "shall")
- missing blanks, square brackets, "TBD", wrong party names (copied templates)

## 4. Rate risk
- **High** - could cause significant loss, is unenforceable/illegal, or breaches a
  playbook must-have. Recommend not signing until fixed.
- **Medium** - off-market or one-sided; negotiate, but can concede with a trade.
- **Low** - drafting/clarity; fix if convenient.

Flag legal-validity issues by jurisdiction where relevant (e.g. India: s.27 Indian
Contract Act renders post-termination non-competes in employment generally void;
s.74 limits penalties to reasonable compensation; stamp duty and e-stamping affect
admissibility; US: state non-compete statutes; UK: penalty doctrine after
*Cavendish v Makdessi*). Mark any authority you have not verified `[VERIFY]`.

## 5. Output
Save to `work/<date>_review_<contract>.md` (or .docx if asked) with:

1. **Executive summary** (5-8 lines): sign / sign with changes / do not sign; the
   3-5 points that matter most, in plain business language.
2. **Issues table:** `# | Clause | Issue | Risk | Recommendation | Proposed wording`
   sorted High -> Low.
3. **Clause-by-clause notes** for High/Medium items, with the exact current text
   quoted briefly, the problem, and **drop-in replacement wording**. Give a
   *preferred* and a *fallback* position for negotiable points.
4. **Missing clauses** that should be there for our side.
5. **Questions for the client** (facts that change the advice).
6. **Assumptions and limits** (law assumed, documents not seen).

If the user wants a marked-up contract, produce the revised text, then generate a
redline with `<plugin>/scripts/redline.py ORIGINAL REVISED -f html -o work/redline.html`
and, if a .docx is required, use the docx skill to write tracked changes.

For an adversarial second look before sending, offer the `opposing-counsel` agent.
