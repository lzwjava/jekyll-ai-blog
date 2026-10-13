---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Phase 1 Complete: A Real Mini-DB"
translated: false
type: note
---

**Phase 1 complete and committed** — the engine went from a single-table demo to a real mini-DB:

## What's new (v0.2)

| Feature | Before | Now |
|---|---|---|
| **JOIN** | ✗ | INNER JOIN with symmetric `"on"` column maps, qualified `users.name` / `orders.total` references |
| **Aggregations** | ✗ | count/sum/avg/min/max + `GROUP BY` (`{"op":"aggregate",...}`) |
| **WHERE ops** | gt/gte/lt/lte/ne | + `IN`, `LIKE` (`%`/`_`), `BETWEEN` |
| **ALTER TABLE** | ✗ | add/drop column (rows re-keyed) |
| **DISTINCT** | ✗ | `select ... "distinct":true` |
| **Batches** | fire-and-forget | `{"ops":[...]}` now **atomic** — any failing op rolls back all earlier ones |
| **LLM context** | stateless | 6-turn (request → plan) memory in the system prompt so "and those older than 40" works |

Tests grew 22 → **49 checks, all green**; zero compiler warnings. Two more real bugs caught along the way (aggregate double-free, wrong-side `on` resolution).

## Verified by the offline demo (real LLM path identical)

```
create users / orders → insert 3 users → insert orders (id looked up by name)
name LIKE 'a%' → age BETWEEN 25..30 → count/sum per city → collapse
JOIN orders×users with WHERE total>50, ORDER BY → ALTER add email → atomic batch
```

## Suggested next milestones

**Phase 2 — internals** (my top pick): ordered primary-key **index/B-tree** (full scans are the current bottleneck), append-only **WAL + crash recovery** instead of whole-file rewrites, and MVCC-ish read snapshots so `SELECT` inside a batch sees a stable view.

**Phase 3 — the AI layer**: **streaming** completions (SSE) so results appear as the LLM thinks, an **`EXPLAIN`-style plan printout** (`> explain "show me users"` prints the JSON plan the model decided on — great for demos and debugging), and a **schema-hallucination guard** that validates every plan field against the real schema *before* execution and auto-asks the model to retry once.

**Phase 4 — testing**: an sqllogictest-style corpus of (query → expected rows) pairs run nightly against the engine, plus a plan-JSON fuzzer.

I'd go Phase 2 → WAL next if you want it to feel like "a real database", or Phase 3 → streaming if you want the AI interaction to feel state-of-the-art. Which direction interests you?
