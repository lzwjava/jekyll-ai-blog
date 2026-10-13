---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fuzzer Catches Two Real Bugs
translated: false
type: note
---

**Final milestones delivered and committed.** Four commits in this round — streaming, the golden corpus, the fuzzer — and the fuzzer immediately paid for itself by catching two real bugs.

## 1. Streaming (SSE)

- `llm_sse.c` — standalone, testable SSE parser (chunk-boundary/mid-line splitting covered by 8 unit checks)
- Plans now **stream to the terminal as the model emits them** (`ISQL_STREAM=0` to disable); servers/proxies that ignore `stream:` degrade gracefully to plain-JSON parsing
- `mock_llm.py` serves SSE mode for end-to-end testing

## 2. sqllogictest corpus

`tests/corpus.logic` — 25 natural-language cases each paired with its golden plan (recorded LLM output), executed against the engine with expectations. It's a regression net *and* prompt-example source. `make corpus` → **25/25 green**.

## 3. Fuzz harness — and the bugs it caught

`./fuzz 1000000 [seed]` hammers three targets: adversarial byte streams into `json_parse` (deep nesting up to 200k, truncations, escapes), random engine plans (including batches and nested `and/or` wheres), and serializer round-trips. **2M iterations across 3 seeds: zero crashes, zero violations** — and at iteration 67 of seed 42:

- **Bug 1 (round-trip)**: `json_to_string` never terminated its buffer after `realloc` growth — values crossing the 64-byte boundary returned strings with **uninitialized garbage tails** (the mystery `20753` mid-output). Every large JSON we ever serialized was slightly poisoned; only the fuzzer could see it.
- **Bug 2 (corpus harness)**: `snprintf(val, "\"%s\"", val)` overlapped src/dst, eating the first character of every seed string (`alice` → `lice`).

Also hardened: **nesting-depth guard (400)** in the parser so a hallucinated deep plan can't overflow the stack, and the engine now rejects unknown columns in `WHERE` (matching SQLite).

## Full project state

```
make test       100 unit checks (83 engine + 9 B+tree + 8 SSE) — 0 failures
make corpus      25 golden-logic checks — 0 failures
make fuzz        2M iterations / 3 seeds — clean
crash_recovery   kill -9 → all committed data survives
```

Commits: `Phase 1` (SQL features) → `june` (WAL + transactions) → `julius` (B+ index, validator, EXPLAIN) → `august` (streaming, corpus, fuzzing).

The project has come full circle: an AI drives a real C database — schema-aware plan generation → validation with one self-correction → indexed/streamed/transactional execution → crash-safe persistence — all held together by a test pyramid that now actually *catches* bugs. Natural next steps if you ever resume: an `sqllogictest` corpus generated from real LLM runs (golden plans for prompt tuning), or trim the retry loop into proper few-shot conversation.
