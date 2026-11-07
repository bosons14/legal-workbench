---
description: Redact or pseudonymise personal and confidential data in a document
argument-hint: <file> [mask|pseudo]
---

Redact: $ARGUMENTS

Use the legal-workbench `redaction` skill. Use `.legal/confidential-terms.txt` as the
terms list if it exists. Default to mask mode unless "pseudo" is given. After running the
tool, read the output for residual or indirect identifiers and re-run with extra terms.
