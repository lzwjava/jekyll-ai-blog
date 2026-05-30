---
audio: false
generated: true
image: false
lang: en
layout: post
title: Manual Dedup Pattern for JSON Storage
translated: false
type: note
---

**Question:** Should I enforce uniqueness when adding records — i.e., is the dedup logic in `add_record` the right place to handle the "unique key" concern for JSON storage?

**Answer:**

Yes, your `_record_key` + `existing_keys` set approach in `add_record` is exactly the right pattern for JSON storage. You've essentially manually implemented what a DB `UNIQUE` constraint does.

But there are a few gaps worth fixing:

## Current logic is correct but fragile in one spot

```python
def _record_key(record_type: str, rec: dict) -> str:
    if record_type == "client_timesheet":
        return f"{rec.get('week_start', '')}_{rec.get('week_end', '')}"
    elif record_type == "vendor_punch_card":
        return rec.get("date", "")
    elif record_type == "vendor_timesheet":
        return rec.get("date", "")
    return str(sorted(rec.items()))  # ← fragile fallback
```

The fallback `str(sorted(rec.items()))` will fail silently if a new record type is added — it'll "deduplicate" by full content equality, which is almost never what you want. Make it explicit:

```python
def _record_key(record_type: str, rec: dict) -> str:
    if record_type == "client_timesheet":
        return f"{rec['week_start']}_{rec['week_end']}"
    elif record_type in ("vendor_punch_card", "vendor_timesheet"):
        return rec["date"]
    raise ValueError(f"Unknown record_type: {record_type!r}")
```

Fail loud, not silent.

## The real uniqueness gap: cross-month

Your dedup only checks within a month bucket:

```python
existing_keys = {_record_key(record_type, r) for r in all_data[month]["records"]}
```

A punch card date like `2026-05-31` could theoretically land in both `202605` and `202606` buckets if the caller passes the wrong `month`. For punch cards and vendor timesheets, the natural key is the `date` itself — consider validating that the date actually belongs to the declared month:

```python
def _validate_month(record_type: str, rec: dict, month: str) -> bool:
    date_field = rec.get("date") or f"{rec.get('week_start', '')}"
    return date_field.startswith(f"{month[:4]}-{month[4:]}")
```

## The `add_record` return value isn't used anywhere visibly

You return `(added, skipped)` but callers should log it:

```python
added, skipped = add_record(data_dir, staff_id, record_type, month, records)
if skipped:
    print(f"  ↩ {skipped} duplicate(s) skipped, {added} added")
```

Otherwise silent skips look like silent failures.

## Bottom line

Your JSON + manual dedup is **correct and sufficient** for this scale. The pattern maps cleanly to what SQLite would give you:

| SQLite | Your JSON |
|---|---|
| `PRIMARY KEY (date)` | `_record_key` returning `date` |
| `INSERT OR IGNORE` | `if key in existing_keys: skip` |
| `UNIQUE (week_start, week_end)` | `f"{week_start}_{week_end}"` composite key |

No database needed — just tighten the fallback and add logging on skips.