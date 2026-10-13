---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Third Milestone: Index, Validator, EXPLAIN"
translated: false
type: note
---

**Third milestone committed.** The roadmap's remaining items are done — the database now has a real index structure, production-style plan validation, and execution transparency:

## 1. Primary-key B+ tree index (`btree.c`)

A genuine in-memory B+ tree (order-64, copy-up leaf splits) used as a lazy pk-index cache:

- **Inserts maintain it incrementally** — duplicate-pk checks, auto-increment, and `where: {"id": N}` probes are O(log n)
- Updates/deletes mark it dirty; the next lookup rebuilds lazily (correctness never depends on it)
- Found and fixed **three real B+ bugs** along the way — child-count on internal splits (OOB read), post-split descent steering, and a shift-scan replace that duplicated keys

**Benchmark proves it** (`make benchmarks`, 50k rows):

```
insert 50000 rows : 9654 ms   (pk-conflict via B+, 1 rebuild total)
pk select 50000   :  106 ms   (2.12 us/lookup, B+ tree)
full scan ×100    : 2909 ms   (29 ms per scan)
```

→ an indexed lookup is **~14,000× faster** than a scan, and the tree was rebuilt only once across 50k incremental inserts.

## 2. Schema validator + LLM self-retry

`db_validate_plan` non-destructively checks every plan against the live schema (tables, `values`, `columns`, `order_by`, `group_by`, nested `and`/`or`, join `on` maps). On the real-LLM path, a rejected plan is **sent back to the model once with the exact error** — a hallucination guard — before giving up with a clear `PLAN ERROR`.

## 3. EXPLAIN (what the AI decided)

```
isql> explain list anyone over 25;
[plan] {"op":"select","table":"users","columns":"*","where":{"age":{"gt":25}}}
[cost] select: scans/joins 3 row(s), pk index: no (full scan)
execute? [y/N]
```

`ISQL_EXPLAIN=1` prints plan + cost for every statement (great for demos).

## Status: 92 checks green (83 engine + 9 B+ tree), crash-recovery intact, 0 warnings

```
423a5f9  isql: AI-driven minimal database  (LLM parses SQL, C executes)
fd4fd7a  Phase 1: JOIN, aggregate, ALTER, IN/LIKE/BETWEEN, DISTINCT, atomic batches, multi-turn memory
fb9fc97  june: WAL crash-recovery + interactive BEGIN/COMMIT/ROLLBACK
10ccd59  julius: B+ pk index, validator + LLM retry, EXPLAIN
```

**What's left on the table:** streaming completions (SSE), a proper `sqllogictest`-style corpus, an fuzz harness for the plan/JSON layers. Want me to push into those, or call it here?
