---
description: Clause-by-clause risk review of a contract for one side, with issues list and fallback wording
argument-hint: <contract-file> [for <party>] [quick|full]
---

Review the contract using the legal-workbench `contract-review` skill.

Arguments: $ARGUMENTS

If the side we act for, governing law, or depth (quick scan vs full review) is not clear
from the arguments or the document, ask for it in one short question before starting.
Finish by offering an adversarial pass with the `opposing-counsel` agent.
