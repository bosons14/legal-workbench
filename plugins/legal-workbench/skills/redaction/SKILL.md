---
name: redaction
description: This skill should be used when the user asks to "redact this document", "remove personal data", "anonymise the judgment/contract", "pseudonymise names before sharing", "mask Aadhaar/PAN/SSN/phone numbers", "prepare a redacted copy for production/disclosure", "privilege log", or wants to share a document without identifying information.
---

# Redaction and pseudonymisation

Plugin root is two levels above this skill's directory.

## Tool
```
python3 <plugin>/scripts/redact.py FILE -o work/FILE.redacted.txt                      # mask
python3 <plugin>/scripts/redact.py FILE --mode pseudo --terms .legal/confidential-terms.txt \
        -o work/FILE.pseudo.txt --log .legal/redaction-key.json                       # pseudonymise
```
Detects email, phone, Aadhaar (checksum-verified), PAN, GSTIN, IFSC, US SSN, payment cards
(Luhn-verified), IBAN, IP addresses, plus custom terms (names, addresses, code names) from a
terms file (`label=term` per line - the same file the confidentiality hook uses).

- **mask** mode for court production, disclosure and publication.
- **pseudo** mode (consistent `PERSON_1`, `CLIENT_1`...) to share readable text with experts,
  translators, or other tools. The `--log` key contains original values: keep it inside
  `.legal/`, never share it.

## Procedure
1. Agree the redaction basis: personal data, privilege, commercial confidentiality,
   court rules (e.g. names of minors and sexual-offence victims must not be disclosed -
   India: s.72 BNS / formerly s.228A IPC; POCSO s.23 [VERIFY]), or a protective order.
2. Build the terms list: names (with variants, initials, nicknames), addresses, account
   numbers, vehicle numbers, case-specific identifiers. Pattern matching cannot find
   everything - e.g. "the CFO's wife", a unique job title, or a photo caption.
3. Run the tool, then **read the output** for residual identifiers and indirect
   identification; add terms and re-run.
4. Produce a redaction log for privilege/production: document, location, category, basis.
5. Final format: the tool outputs text. For a redacted **PDF** to file or produce, use a
   tool that removes the underlying text layer (true redaction) and then verify by
   searching the output PDF for a redacted term. Black boxes drawn over text do not redact.
