---
audio: false
generated: true
image: false
lang: en
layout: post
title: SQLite Database with Eight Tables
translated: false
type: note
---

The project uses **SQLite** — there's a dedicated `db.py` module. The database lives at `data/tt.db` (not the empty `tt.db` in the project root).

Here are the **8 tables** in the database:

```
users                — staff registry (staff_id, staff_name, registered_at)
session              — current logged-in user (single-row, id=1)
client_timesheets    — weekly timesheet records (staff_id, month, week, hours)
client_timesheet_days— daily breakdown per timesheet (FK → client_timesheets)
vendor_punch_cards   — daily punch card records (50+ columns for attendance data)
vendor_timesheets    — daily vendor timesheet records (am/pm/hours)
references           — record type references (essential_keys, raw_example)
contractor_cache     — cached contractor data (name, extracted_at, data as JSON blob)
images               — uploaded image registry (filename, md5, added_at)
```

The `data/tt.db` database is the real one. The root-level `tt.db` is empty/unused — probably a stale leftover from an earlier iteration.