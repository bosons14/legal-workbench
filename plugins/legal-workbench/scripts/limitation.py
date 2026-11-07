#!/usr/bin/env python3
"""Limitation / deadline calculator.

Computes a deadline from a trigger date using either a named preset (common
limitation periods and procedural deadlines) or a custom period, with the
usual counting rules:

  * the trigger day itself is excluded (e.g. India: Limitation Act s.12(1);
    US: FRCP 6(a)(1)(A); UK: CPR 2.8 "clear days" is stricter - see notes)
  * time spent obtaining certified copies or other excluded time can be added
    (--exclude-days, e.g. Limitation Act s.12(2))
  * if the last day falls on a weekend or a listed court holiday, the deadline
    rolls forward to the next working day (--roll, e.g. Limitation Act s.4,
    FRCP 6(a)(1)(C))

Usage:
    limitation.py --list [--jurisdiction in|us|uk]
    limitation.py PRESET DATE [--exclude-days N] [--holidays FILE] [--no-roll]
    limitation.py custom DATE --period 90d|3m|3y [--holidays FILE]

DATE is YYYY-MM-DD. Holidays file: one YYYY-MM-DD per line (court calendar).

THIS IS A CALCULATION AID, NOT LEGAL ADVICE. Presets are simplified - the
applicable article, the true trigger date, condonation, acknowledgment,
tolling, local rules and amendments all change the answer. Verify every
deadline against the current statute and court rules before relying on it.
"""
import argparse
import calendar
import datetime as dt
import json
import re
import sys
from pathlib import Path

# key: (jurisdiction, period, trigger description, authority, notes)
PRESETS = {
    # ---- India -------------------------------------------------------------
    "in-money-lent": ("in", "3y", "date the loan is made", "Limitation Act 1963, Sch. Art. 19", ""),
    "in-contract-breach": ("in", "3y", "date the contract is broken", "Limitation Act 1963, Sch. Art. 55",
                           "successive breaches: each breach; continuing breach: when it ceases"),
    "in-specific-performance": ("in", "3y", "date fixed for performance, or date plaintiff has notice performance is refused",
                                "Limitation Act 1963, Sch. Art. 54", ""),
    "in-possession-title": ("in", "12y", "possession of defendant becomes adverse to plaintiff",
                            "Limitation Act 1963, Sch. Art. 65", ""),
    "in-residuary-application": ("in", "3y", "right to apply accrues", "Limitation Act 1963, Sch. Art. 137", ""),
    "in-residuary-suit": ("in", "3y", "right to sue accrues", "Limitation Act 1963, Sch. Art. 113", ""),
    "in-appeal-hc-decree": ("in", "90d", "date of decree/order", "Limitation Act 1963, Sch. Art. 116(a)",
                            "appeal under CPC to a High Court; exclude time for certified copy (s.12(2))"),
    "in-appeal-other-court": ("in", "30d", "date of decree/order", "Limitation Act 1963, Sch. Art. 116(b)",
                              "appeal under CPC to any other court"),
    "in-intra-court-appeal": ("in", "30d", "date of decree/order", "Limitation Act 1963, Sch. Art. 117",
                              "appeal from a High Court decree/order to the same High Court"),
    "in-slp-sc": ("in", "90d", "date of High Court judgment/order", "Supreme Court Rules 2013, O. XXII r.2 (Art. 136)",
                  "60 days if from refusal of certificate of fitness; check current SC Rules"),
    "in-review": ("in", "30d", "date of decree/order", "Limitation Act 1963, Sch. Art. 124",
                  "review in a court other than the Supreme Court"),
    "in-ni138-notice": ("in", "30d", "receipt of information from bank about dishonour",
                        "Negotiable Instruments Act 1881, s.138 proviso (b)", "demand notice to drawer"),
    "in-ni138-payment": ("in", "15d", "receipt of the demand notice by drawer",
                         "Negotiable Instruments Act 1881, s.138 proviso (c)", "cause of action arises after this period"),
    "in-ni138-complaint": ("in", "1m", "date cause of action arises (expiry of 15-day payment period)",
                           "Negotiable Instruments Act 1881, s.142(1)(b)", "court may condone delay for sufficient cause"),
    "in-arb-s34": ("in", "3m", "receipt of the arbitral award", "Arbitration and Conciliation Act 1996, s.34(3)",
                   "court may extend by a further 30 days 'but not thereafter'"),
    "in-consumer-complaint": ("in", "2y", "date cause of action arises", "Consumer Protection Act 2019, s.69", ""),
    "in-ws-cpc": ("in", "30d", "service of summons", "CPC 1908, O. VIII r.1",
                  "extendable up to 90 days; commercial suits: hard stop at 120 days (Commercial Courts Act 2015)"),
    # ---- United States (federal) ------------------------------------------
    "us-answer": ("us", "21d", "service of summons and complaint", "FRCP 12(a)(1)(A)(i)",
                  "60 days if service waived under Rule 4(d); state courts differ"),
    "us-notice-of-appeal": ("us", "30d", "entry of judgment/order", "FRAP 4(a)(1)(A)",
                            "60 days if the United States is a party (FRAP 4(a)(1)(B))"),
    "us-cert-petition": ("us", "90d", "entry of judgment or denial of rehearing", "Sup. Ct. R. 13.1", ""),
    "us-new-trial": ("us", "28d", "entry of judgment", "FRCP 59(b)", "not extendable (FRCP 6(b)(2))"),
    # ---- England & Wales --------------------------------------------------
    "uk-contract": ("uk", "6y", "date of breach", "Limitation Act 1980, s.5", "12 years for a deed (s.8)"),
    "uk-tort": ("uk", "6y", "date damage is suffered", "Limitation Act 1980, s.2", ""),
    "uk-personal-injury": ("uk", "3y", "date of injury or date of knowledge", "Limitation Act 1980, s.11", ""),
    "uk-defence": ("uk", "28d", "service of particulars of claim (if acknowledgment filed)", "CPR 15.4(1)(b)",
                   "14 days if no acknowledgment of service"),
    "uk-appeal-notice": ("uk", "21d", "date of decision of lower court", "CPR 52.12(2)(b)",
                         "unless lower court directs otherwise"),
}


def add_period(d, period):
    m = re.fullmatch(r"(\d+)\s*([dwmy])", period.strip().lower())
    if not m:
        raise SystemExit(f"bad period '{period}' - use e.g. 30d, 2w, 3m, 12y")
    n, unit = int(m.group(1)), m.group(2)
    if unit == "d":
        return d + dt.timedelta(days=n)
    if unit == "w":
        return d + dt.timedelta(weeks=n)
    months = n if unit == "m" else 12 * n
    y, mo = divmod(d.month - 1 + months, 12)
    y, mo = d.year + y, mo + 1
    return dt.date(y, mo, min(d.day, calendar.monthrange(y, mo)[1]))


def load_holidays(path):
    if not path:
        return set()
    out = set()
    for line in Path(path).read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.add(dt.date.fromisoformat(line[:10]))
    return out


def roll_forward(d, holidays):
    reasons = []
    while d.weekday() >= 5 or d in holidays:
        reasons.append(f"{d.isoformat()} ({'holiday' if d in holidays else d.strftime('%A')})")
        d += dt.timedelta(days=1)
    return d, reasons


def compute(trigger, period, exclude_days=0, holidays=(), roll=True):
    raw = add_period(trigger, period) + dt.timedelta(days=exclude_days)
    final, skipped = roll_forward(raw, set(holidays)) if roll else (raw, [])
    return raw, final, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("preset", nargs="?")
    ap.add_argument("date", nargs="?")
    ap.add_argument("--period", help="for 'custom': e.g. 45d, 3m, 3y")
    ap.add_argument("--exclude-days", type=int, default=0, help="excluded time to add (e.g. certified-copy days)")
    ap.add_argument("--holidays", help="file of court holidays, YYYY-MM-DD per line")
    ap.add_argument("--no-roll", action="store_true", help="do not move a weekend/holiday deadline forward")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--jurisdiction", choices=["in", "us", "uk"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.list or not a.preset:
        for k, (j, p, trig, auth, note) in PRESETS.items():
            if a.jurisdiction and j != a.jurisdiction:
                continue
            print(f"{k:26} {p:>4}  from {trig}  [{auth}]" + (f"  - {note}" if note else ""))
        return
    if not a.date:
        ap.error("DATE (YYYY-MM-DD) is required")
    trigger = dt.date.fromisoformat(a.date)
    if a.preset == "custom":
        if not a.period:
            ap.error("custom needs --period")
        period, trig, auth, note = a.period, "trigger date", "custom period", ""
    elif a.preset in PRESETS:
        _, period, trig, auth, note = PRESETS[a.preset]
    else:
        sys.exit(f"unknown preset '{a.preset}' - run with --list")

    raw, final, skipped = compute(trigger, period, a.exclude_days, load_holidays(a.holidays), not a.no_roll)
    result = {
        "preset": a.preset, "authority": auth, "period": period, "trigger": trigger.isoformat(),
        "trigger_meaning": trig, "excluded_days": a.exclude_days,
        "computed_last_day": raw.isoformat(), "deadline": final.isoformat(),
        "deadline_weekday": final.strftime("%A"), "rolled_past": skipped, "notes": note,
        "days_from_today": (final - dt.date.today()).days,
        "warning": "Calculation aid only - verify the article/rule, trigger date, exclusions and court calendar.",
    }
    if a.json:
        print(json.dumps(result, indent=2))
        return
    print(f"{auth}: {period} from {trig}")
    print(f"  trigger date        {trigger.isoformat()} ({trigger.strftime('%A')})")
    if a.exclude_days:
        print(f"  excluded time       +{a.exclude_days} day(s)")
    print(f"  period ends         {raw.isoformat()} ({raw.strftime('%A')})")
    if skipped:
        print(f"  rolled past         {', '.join(skipped)}")
    print(f"  DEADLINE            {final.isoformat()} ({final.strftime('%A')})  "
          f"[{result['days_from_today']:+d} days from today]")
    if note:
        print(f"  note                {note}")
    print("  ! verify against the current statute, rules and court calendar before relying on this")


if __name__ == "__main__":
    main()
