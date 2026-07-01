---
audio: false
generated: true
image: false
lang: en
layout: post
title: JSON vs SQLite vs MongoDB Scale Advice
translated: false
type: note
---

**Question:** Should I use MongoDB or SQLite (instead of JSON files) for the `tt` timesheet verification tool?

**Answer:**

Neither. **Keep the JSON cache.** Your own README says it best: "no database needed at this scale."

Here's why, specifically for `tt`:

## What `tt` actually stores

```
contractors: ~1-20
weeks per contractor: ~4-5
punch days per contractor: ~20-31
```

That's maybe **500 records total per month**, read once per run, written once per extraction. This is config-file scale, not database scale.

## Why JSON wins here

- **No relations to enforce** — `client_weeks` and `punch_days` are denormalized per contractor. No cross-contractor joins ever happen.
- **The "foreign key problem" doesn't apply** — each `contractor_a.json` is self-contained. You're not linking rows across files.
- **Human-editable** — you explicitly use `jq` to inspect/fix extracted data. A database breaks this workflow.
- **LLM extraction output is naturally JSON** — you'd just serialize to DB and deserialize back out for zero gain.
- **`--force` re-extraction replaces the whole record** — atomic file replace is simpler than `DELETE + INSERT`.

## When you'd actually need a DB

| Condition | SQLite | Mongo |
| --- | --- | --- |
| 50+ contractors, querying across all | ✅ | ✅ |
| Historical month-over-month trend analysis | ✅ | ✅ |
| Multiple users writing concurrently | ✅ | ✅ |
| Flexible schema per contractor (nested, variable) | — | ✅ |
| You need `GROUP BY month, contractor` in SQL | ✅ | — |

None of these apply to `tt` right now.

## If you did outgrow JSON → SQLite, not MongoDB

MongoDB would be overkill (separate server process, no ACID by default pre-4.0, operational overhead). If you ever needed querying across contractors or historical runs, SQLite is the right step:

```python
CREATE TABLE contractor_weeks (
    contractor TEXT,
    week_start DATE,
    total_hours REAL,
    project_hours REAL,
    status TEXT,
    extracted_at TIMESTAMP
);
```

Then `SELECT contractor, AVG(project_hours/total_hours) FROM contractor_weeks GROUP BY contractor` — actually useful for trend reports.

## Verdict

```
tt scale:  JSON ✅   SQLite (overkill)   MongoDB (way overkill)
```

The JSON design is correct for this tool. The previous conversation about JSON-as-DB applies when you have **relational data with integrity requirements** — `tt`'s data is flat, isolated per contractor, and LLM-generated. JSON is the right call.
