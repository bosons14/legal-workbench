#!/usr/bin/env python3
"""PreToolUse hook: stop client-confidential terms from leaving the machine.

Before Claude runs WebSearch, WebFetch, or a network command in Bash (curl,
wget, http clients), this hook checks the outgoing query/URL/command against
the matter's confidential terms list and blocks the call if any term appears.

Terms file (first one found wins):
    $CLAUDE_PROJECT_DIR/.legal/confidential-terms.txt
    $LEGAL_WORKBENCH_TERMS  (path in an environment variable)
One term per line; '#' starts a comment; 'label=term' lines are accepted
(same format as redact.py --terms, so one file serves both).

No terms file -> the hook allows everything (it never blocks by accident).
"""
import json
import os
import re
import sys
from pathlib import Path

NET_CMD = re.compile(r"\b(curl|wget|http|httpie|aria2c|lynx|w3m|requests\.|urllib|fetch\()", re.I)


def terms_file():
    proj = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    for cand in (Path(proj) / ".legal" / "confidential-terms.txt", os.environ.get("LEGAL_WORKBENCH_TERMS")):
        if cand and Path(cand).is_file():
            return Path(cand)
    return None


def load_terms(p):
    out = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        term = line.split("=", 1)[1].strip() if "=" in line else line
        if len(term) >= 3:
            out.append(term)
    return out


def main():
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0
    tool = event.get("tool_name", "")
    ti = event.get("tool_input", {}) or {}
    if tool == "Bash":
        outgoing = ti.get("command", "")
        if not NET_CMD.search(outgoing):
            return 0
    elif tool in ("WebSearch", "WebFetch"):
        outgoing = " ".join(str(ti.get(k, "")) for k in ("query", "url", "prompt"))
    else:
        return 0

    tf = terms_file()
    if not tf:
        return 0
    hits = [t for t in load_terms(tf)
            if re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", outgoing, re.I)]
    if not hits:
        return 0
    reason = (f"legal-workbench confidentiality guard: this {tool} call contains "
              f"{len(hits)} term(s) from {tf.name} ({', '.join(repr(h) for h in hits[:5])}). "
              "Client-confidential names must not be sent to external services. Rephrase the query "
              "generically (e.g. 'a software vendor' instead of the client's name, the legal issue instead "
              "of the facts) and try again, or ask the user to confirm and remove the term from the list.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
