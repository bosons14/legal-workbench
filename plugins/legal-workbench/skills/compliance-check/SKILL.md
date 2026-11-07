---
name: compliance-check
description: This skill should be used when the user asks to "check compliance", "gap analysis", "are we compliant with DPDP/GDPR/CCPA", "review this privacy policy", "draft a privacy policy / terms of use", "POSH compliance", "compliance calendar", "regulatory checklist", "what licences do we need", or wants a policy, product, or company practice assessed against a law or regulation.
---

# Compliance check and policy drafting

Plugin root is two levels above this skill's directory. Follow
`<plugin>/references/ground-rules.md` - regulations change frequently; confirm the current
text and any rules/notifications before relying on a requirement.

## 1. Scope
Which law(s) and regulator(s); which entity, product or process; jurisdictions of the
business and of its users/customers; sector (fintech, health, edtech, e-commerce...).

## 2. Build the requirements matrix
Research the current law (legal-research skill), then build
`work/<date>_compliance_<law>.md`:
`# | Requirement | Source (section/rule) | Current practice (evidence) | Gap | Risk | Action | Owner | Due`
Requirements must be pinned to provisions. Separate mandatory obligations from best practice.

## 3. Common frameworks (starting checklists - verify current text)
- **India DPDP Act 2023 and DPDP Rules**: notice and consent (itemised, plain language,
  available in English and scheduled languages), consent managers, legitimate uses, purpose
  limitation, data principal rights (access, correction, erasure, grievance, nomination),
  children's data (verifiable parental consent; no tracking/targeted ads), security
  safeguards, breach intimation to the Board and data principals, retention and erasure,
  Significant Data Fiduciary duties (DPO, DPIA, audits), cross-border transfer restrictions,
  processor contracts. Check the phased commencement dates of the Rules.
- **GDPR / UK GDPR**: lawful basis, transparency, rights, DPIA, records of processing,
  processors (Art. 28), international transfers (SCCs/IDTA), breach notification (72 hours), DPO.
- **POSH Act 2013 (India)**: written policy, Internal Committee constitution (presiding
  woman officer, external member), awareness programmes, inquiry timelines, annual report.
- **Website/app terms**: IT Act 2000 and Intermediary Guidelines (grievance officer,
  due diligence), Consumer Protection (E-Commerce) Rules 2020, dark patterns guidelines.
- **Corporate secretarial calendar**: annual filings, board meeting frequency, statutory
  registers, DIR-3 KYC, etc. (India - Companies Act 2013) [VERIFY each due date].

## 4. Output
Executive summary with the top gaps by risk; the matrix; a prioritised remediation plan;
and draft policy text or notices if requested (contract-drafting conventions apply).
State clearly that the assessment is based on information provided and the law as checked
on the date of the report.
