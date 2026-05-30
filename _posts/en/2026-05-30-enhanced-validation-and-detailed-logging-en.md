---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enhanced Validation and Detailed Logging
translated: false
type: note
---

Good. Here's what changed in `/Users/lzwjava/projects/tt/tt/repl.py`:

1. Added `_validate_client_week()` — runs sanity checks on extracted client timesheet data:
   - Must have at least 1 day
   - total_hours must be > 0
   - project_pct must be 0.0–1.0
   - week_end must not be before week_start
   - All days must fall within the week range
   - Extracted month must match the user-selected month

2. After extraction, full detail is printed for each record type:
   - client_timesheet: week range, status, total/project hours, per-day breakdown
   - vendor_punch_card: per-day status and raw label
   - vendor_timesheet: per-day AM/PM checkmarks and hours

3. If validation fails → prints "REJECTED" with reasons, does NOT add to records list
4. If all images rejected → shows rejection summary and returns (no Save? prompt)
5. If some pass and some reject → asks Save? only for valid ones, notes rejection count