#!/usr/bin/env python3
"""Conflict-of-interest check against a local register of parties.

The register is a CSV kept with your matters (default .legal/conflicts.csv) with
columns: name,role,matter,aliases,notes
  role    - client | adverse | related | witness | counsel | other
  aliases - optional, separated by '|'  (former names, group companies, DBA)

Matching normalises case, punctuation and company suffixes (Pvt Ltd, LLP,
Inc, GmbH, ...) and uses fuzzy matching, so "ACME Holdings Private Limited"
matches "Acme Holdings Pvt. Ltd.".

Usage:
    conflicts.py check "Name One" "Name Two" ... [--register FILE] [--threshold 0.85]
    conflicts.py add NAME --role adverse --matter M-2026-014 [--aliases "A|B"] [--register FILE]
    conflicts.py list [--register FILE]

Exit code 2 if any potential conflict is found (handy for scripts). A hit is a
prompt for human review, not a conclusion; a miss only covers what is in the register.
"""
import argparse
import csv
import difflib
import re
import sys
from pathlib import Path

FIELDS = ["name", "role", "matter", "aliases", "notes"]
SUFFIXES = r"\b(private|pvt|limited|ltd|llp|llc|inc|incorporated|corp|corporation|co|company|plc|gmbh|ag|sa|bv|nv|pte|pty|the|and|&)\b"


def norm(s):
    s = re.sub(r"[^\w\s&]", " ", s.lower())
    s = re.sub(SUFFIXES, " ", s)
    return re.sub(r"\s+", " ", s).strip()


def score(a, b):
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    r = difflib.SequenceMatcher(None, na, nb).ratio()
    ta, tb = set(na.split()), set(nb.split())
    if ta and tb and (ta <= tb or tb <= ta):  # one name contained in the other
        r = max(r, 0.9)
    return r


def load(path):
    p = Path(path)
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "add", "list"):
        sp = sub.add_parser(name)
        sp.add_argument("--register", default=".legal/conflicts.csv")
        if name == "check":
            sp.add_argument("names", nargs="+")
            sp.add_argument("--threshold", type=float, default=0.85)
        if name == "add":
            sp.add_argument("name")
            sp.add_argument("--role", required=True)
            sp.add_argument("--matter", required=True)
            sp.add_argument("--aliases", default="")
            sp.add_argument("--notes", default="")
    a = ap.parse_args()

    rows = load(a.register)
    if a.cmd == "list":
        for r in rows:
            print(f"{r['name']:40} {r['role']:9} {r['matter']:16} {r.get('aliases', '')}")
        print(f"{len(rows)} entries in {a.register}", file=sys.stderr)
        return
    if a.cmd == "add":
        p = Path(a.register)
        p.parent.mkdir(parents=True, exist_ok=True)
        new = not p.exists()
        with p.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            if new:
                w.writeheader()
            w.writerow({"name": a.name, "role": a.role, "matter": a.matter, "aliases": a.aliases, "notes": a.notes})
        print(f"added '{a.name}' ({a.role}, {a.matter}) to {a.register}")
        return

    if not rows:
        print(f"register {a.register} is empty or missing - nothing to check against", file=sys.stderr)
    hits = 0
    for q in a.names:
        found = []
        for r in rows:
            cands = [r["name"]] + [x for x in (r.get("aliases") or "").split("|") if x.strip()]
            best = max(cands, key=lambda c: score(q, c))
            s = score(q, best)
            if s >= a.threshold:
                found.append((s, best, r))
        found.sort(key=lambda t: -t[0])
        if not found:
            print(f"CLEAR      {q}")
            continue
        hits += 1
        print(f"POSSIBLE   {q}")
        for s, matched, r in found:
            flag = " <-- ADVERSE" if r["role"].lower() == "adverse" else ""
            print(f"   {s:.2f}  '{matched}'  role={r['role']}  matter={r['matter']}{flag}"
                  + (f"  notes={r['notes']}" if r.get("notes") else ""))
    print(f"\n{hits} of {len(a.names)} name(s) need review. A clear result only covers names in the register.",
          file=sys.stderr)
    sys.exit(2 if hits else 0)


if __name__ == "__main__":
    main()
