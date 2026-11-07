---
name: legal-deadlines
description: This skill should be used when the user asks "what is the limitation period", "when is the last date to file", "compute the deadline", "is this time-barred", "when must we reply", "calculate 90 days from the order", "condonation of delay", "court holidays", or needs any statutory or procedural deadline calculated or a matter's deadlines tracked.
---

# Limitation and deadlines

Missing a deadline is the most common cause of professional negligence claims.
Calculate carefully, show the working, and always flag for verification.

Plugin root is two levels above this skill's directory.

## Calculator
```
python3 <plugin>/scripts/limitation.py --list [--jurisdiction in|us|uk]   # presets
python3 <plugin>/scripts/limitation.py in-arb-s34 2026-08-31              # preset
python3 <plugin>/scripts/limitation.py in-appeal-hc-decree 2026-01-15 --exclude-days 12 --holidays court-holidays.txt
python3 <plugin>/scripts/limitation.py custom 2026-03-01 --period 45d
```
It excludes the trigger day, adds excluded time (e.g. certified-copy period, Limitation
Act s.12(2)), and rolls a weekend/holiday deadline forward to the next working day
(s.4; FRCP 6(a)(1)(C)). Use `--no-roll` where the rule does not extend (some statutory
periods, and some "not thereafter" outer limits). `--json` gives machine-readable output.

## Procedure
1. **Identify the right provision.** Which article/rule governs depends on the precise
   nature of the claim. If two could apply, compute both and lead with the earlier.
   If the preset list lacks it, research the provision (legal-research skill) and use `custom`.
2. **Fix the trigger date** from the documents (date of breach, of knowledge, of
   receipt of the order/award, of service). If uncertain, compute from the earliest
   plausible date and say so.
3. **Apply exclusions and extensions**: certified copy time, acknowledgment in writing
   (fresh period - India s.18), part payment (s.19), legal disability (s.6), fraud
   (s.17), time during which proceedings were bona fide pursued in a wrong court (s.14),
   any court-ordered extensions. Note general extensions ordered by courts (e.g. the
   Supreme Court's COVID-period exclusion, 15.03.2020 to 28.02.2022 [VERIFY scope]).
4. **Court calendar**: ask for or locate the court's holiday list for the year and pass it
   with `--holidays`. Vacation benches and filing-counter rules can differ from sitting days.
5. **Output** a deadline table and add it to `MATTER.md`:
   `Deadline | Action | Authority | Trigger | Computation | Days left | Verified by lawyer (Y/N)`
6. Recommend an internal target date several days before the legal deadline.

If a deadline has **passed**, say so clearly, then identify options: condonation of delay
(India s.5 Limitation Act - not available for suits, and expressly limited under some
statutes such as Arbitration Act s.34(3) and Commercial Courts Act timelines),
continuing cause of action, fresh acknowledgment, or alternative remedies.

Never tell a user they are "within time" without the caveat that the computation must be
verified against the statute, rules and court calendar.
