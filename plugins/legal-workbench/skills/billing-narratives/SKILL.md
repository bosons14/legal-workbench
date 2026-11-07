---
name: billing-narratives
description: This skill should be used when the user asks to "write time entries", "clean up my billing narratives", "prepare an invoice for the client", "fee note", "summarise work done this month for billing", "convert my notes into timesheet entries", or "check entries against the client's billing guidelines".
---

# Billing narratives and fee notes

Turn rough notes, calendar entries or a matter's work folder into clear, defensible
time entries and fee notes.

## Time entries
Each entry: `Date | Matter | Timekeeper | Hours (in the firm's increments, e.g. 0.1) | Task code (if UTBMS/LEDES) | Narrative`
- Narrative = action verb + specific task + purpose: "Reviewed and commented on Supplier's
  markup of MSA (cl. 8-14, liability and indemnity) for call with client" - not "Work on contract".
- One task per entry - no block billing unless the client allows it.
- Never invent or round up time. Use only the hours the user gives; flag gaps
  ("No time recorded for the 12 Nov call - add?").
- Check against client billing guidelines if provided: banned tasks (internal conferences,
  file opening, clerical work), caps, required task codes, rate approvals.
- Keep narratives privileged-safe: describe the task, not legal strategy or advice content.

## Fee note / invoice
Header (firm, client, matter, invoice no., date, period); summary of work; entries table;
fees subtotal; disbursements with receipts; taxes (India: GST on legal services is
generally under reverse charge for business entities - [VERIFY current notification] - so
state "GST payable by recipient under RCM" where applicable); total; payment details;
terms. Use the xlsx skill for spreadsheets or docx for formal fee notes.
