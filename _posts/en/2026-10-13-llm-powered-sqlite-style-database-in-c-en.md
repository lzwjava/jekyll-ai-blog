---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM-Powered SQLite-Style Database in C
translated: false
type: note
---

Done. **isql** is committed and fully working — a minimal SQLite-style database in C where an LLM does all the SQL parsing.

## What got built

```
you type → LLM (system prompt includes live schema) → JSON query plan → C engine → ASCII table
```

| File | Role |
|---|---|
| `main.c` | REPL · bundles schema into prompt · calls LLM · prints results · persists |
| `db.c/h` | The engine: CREATE/DROP TABLE, INSERT, SELECT (WHERE/ORDER BY/LIMIT), UPDATE, DELETE, PK auto-increment + uniqueness, type coercion (`int`/`real`/`text`), JSON file persistence |
| `json.c/h` | Hand-written JSON parser/serializer — the plan wire format |
| `llm.c/h` | OpenAI-compatible `/chat/completions` client on libcurl |
| `tests/` | offline `test_engine` (22 checks) + `mock_llm.py` fake OpenAI server |

## The AI contract
The LLM never sees SQL — it returns one of 9 plan verbs (`{"op":"select","table":"users","where":{"age":{"gt":26}},...}`). There is **zero SQL parsing in the binary**; correctness depends on the prompt contract in `LLM_RULES`. Works with OpenAI or any compatible endpoint (Ollama, etc.).

## Verified
- `make test` — **22/22 engine checks green**
- Full REPL sessions via `ISQL_FAKE_LLM=1` (offline): create → insert ×3 → select/order/limit → update → delete → describe, incl. persistence across restarts
- **Real HTTP path exercised**: the sandbox could reach `api.openai.com` — got a proper `401` and our parser correctly surfaced OpenAI's error body, while the outgoing HTTPS/proxy path worked

## Bugs I found along the way (all fixed)
1. `json_obj_set` stored key pointers without copying → double-free of column names *(the crash you can't unsee)*
2. Same root cause for SELECT results: cells were shared with the DB, freed twice
3. UPDATE appended duplicate keys instead of replacing → stale reads
4. DELETE deleted the non-matching rows (logic inversion)
5. A **double `free(stmt)`** in the REPL's EOF path (missing `stmt = NULL`)

## Run it
```sh
make
make test                                  # offline
ISQL_FAKE_LLM=1 ./isql                     # offline demo
ISQL_KEY=sk-... ISQL_MODEL=gpt-4o-mini ./isql   # real AI parsing
```
