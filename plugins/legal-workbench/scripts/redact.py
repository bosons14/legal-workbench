#!/usr/bin/env python3
"""Redact or pseudonymise personal and confidential data in a document's text.

Detects: email addresses, phone numbers, Indian Aadhaar (Verhoeff-checked),
PAN, GSTIN, IFSC, US SSN, payment cards (Luhn-checked), IBAN, IP addresses,
plus any custom terms (client names, project code names) you list in a file.

Usage:
    redact.py FILE [-o OUT] [--terms TERMS.txt] [--mode mask|pseudo]
              [--only email,phone,...] [--log LOG.json]

--mode mask   replaces matches with [REDACTED-TYPE]   (default; for production/filing)
--mode pseudo replaces matches with consistent labels like PERSON_1, EMAIL_2
              (for sharing with experts or AI tools while keeping the text readable)
--log         writes a JSON key of what was replaced - this file contains the
              original sensitive values: keep it privileged and out of shared folders.

Output is plain text. This does not edit a .docx/.pdf in place: to produce a
redacted PDF for filing, use a dedicated tool that removes the underlying text
(drawing black boxes over a PDF does NOT remove the text).
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_text import paragraphs  # noqa: E402

# --- checksum validators ------------------------------------------------------
_V_D = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],[2,3,4,0,1,7,8,9,5,6],[3,4,0,1,2,8,9,5,6,7],
        [4,0,1,2,3,9,5,6,7,8],[5,9,8,7,6,0,4,3,2,1],[6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],
        [8,7,6,5,9,3,2,1,0,4],[9,8,7,6,5,4,3,2,1,0]]
_V_P = [[0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],[5,8,0,3,7,9,6,1,4,2],[8,9,1,6,0,4,3,5,2,7],
        [9,4,5,3,1,2,6,8,7,0],[4,2,8,6,5,7,3,9,0,1],[2,7,9,3,8,0,6,4,1,5],[7,0,4,6,9,1,3,2,5,8]]


def verhoeff_ok(num):
    c = 0
    for i, d in enumerate(reversed(num)):
        c = _V_D[c][_V_P[i % 8][int(d)]]
    return c == 0


def luhn_ok(num):
    total, alt = 0, False
    for d in reversed(num):
        n = int(d)
        if alt:
            n = n * 2 - 9 if n > 4 else n * 2
        total += n
        alt = not alt
    return total % 10 == 0


def digits(s):
    return re.sub(r"\D", "", s)


# order matters: more specific patterns first
PATTERNS = [
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"), None),
    ("card", re.compile(r"\b(?:\d[ -]?){13,19}\b"), lambda m: 13 <= len(digits(m)) <= 19 and luhn_ok(digits(m))),
    ("aadhaar", re.compile(r"\b[2-9]\d{3}[ -]?\d{4}[ -]?\d{4}\b"), lambda m: verhoeff_ok(digits(m))),
    ("iban", re.compile(r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,3})?\b"), None),
    ("gstin", re.compile(r"\b\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b"), None),
    ("pan", re.compile(r"\b[A-Z]{3}[ABCFGHLJPT][A-Z]\d{4}[A-Z]\b"), None),
    ("ifsc", re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b"), None),
    ("ssn", re.compile(r"\b(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b"), None),
    ("ip", re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"), None),
    ("phone", re.compile(
        r"(?<![\w+])(?:"
        r"\+\d{1,3}[ .-]?\(?\d{1,5}\)?(?:[ .-]?\d){5,11}"      # international: +91 98765 43210, +1 (415) 555-0100
        r"|0?[6-9]\d{4}[ -]?\d{5}"                             # Indian mobile: 98765 43210, 09876543210
        r"|0\d{2,4}[ -]\d{6,8}"                                # Indian landline: 011-23456789
        r"|\(\d{3}\)[ ]?\d{3}[-.]\d{4}|\d{3}[-.]\d{3}[-.]\d{4}"  # NANP: (415) 555-0100, 415-555-0100
        r")(?![\w])"),
     lambda m: 10 <= len(digits(m)) <= 15),
]


def load_terms(path):
    terms = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            label, _, term = line.partition("=") if "=" in line else ("term", "", line)
            terms.append((label.strip() if term else "term", (term or label).strip()))
    # longest first so "Acme Holdings Ltd" wins over "Acme"
    return sorted(terms, key=lambda t: -len(t[1]))


class Redactor:
    def __init__(self, mode, only=None, terms=()):
        self.mode, self.only, self.terms = mode, only, terms
        self.key, self.counter, self.counts, self.original = {}, {}, {}, {}

    def label(self, kind, value):
        self.counts[kind] = self.counts.get(kind, 0) + 1
        if self.mode == "mask":
            self.key.setdefault(value, f"[REDACTED-{kind.upper()}]")
            return f"[REDACTED-{kind.upper()}]"
        norm = value.lower().strip()
        if norm not in self.key:
            self.counter[kind] = self.counter.get(kind, 0) + 1
            self.key[norm] = f"{kind.upper()}_{self.counter[kind]}"
            self.original[norm] = value.strip()
        return self.key[norm]

    def run(self, text):
        for kind, term in self.terms:
            pat = re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE)
            text = pat.sub(lambda m, k=kind: self.label(k, m.group(0)), text)
        for kind, pat, check in PATTERNS:
            if self.only and kind not in self.only:
                continue

            def sub(m, kind=kind, check=check):
                v = m.group(0)
                if check and not check(v):
                    return v
                return self.label(kind, v)
            text = pat.sub(sub, text)
        return text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("-o", "--out")
    ap.add_argument("--terms", help="file of custom terms, one per line; optional 'label=term' (e.g. person=Ravi Kumar)")
    ap.add_argument("--mode", choices=["mask", "pseudo"], default="mask")
    ap.add_argument("--only", help="comma list of detector types to run, e.g. email,phone,aadhaar")
    ap.add_argument("--log", help="write replacement key (sensitive!) to this JSON file")
    a = ap.parse_args()

    terms = load_terms(a.terms) if a.terms else []
    only = set(a.only.split(",")) if a.only else None
    r = Redactor(a.mode, only, terms)
    text = "\n\n".join(r.run(p) for p in paragraphs(a.file)) + "\n"
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    summary = ", ".join(f"{k}: {v}" for k, v in sorted(r.counts.items())) or "nothing found"
    print(f"redactions - {summary}", file=sys.stderr)
    if a.log:
        Path(a.log).write_text(json.dumps({"mode": a.mode, "counts": r.counts,
                                           "key": ({v: r.original[k] for k, v in r.key.items()} if a.mode == "pseudo"
                                                   else {k: v for k, v in r.key.items()})},
                                          indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"key written to {a.log} (contains original values - keep privileged)", file=sys.stderr)


if __name__ == "__main__":
    main()
