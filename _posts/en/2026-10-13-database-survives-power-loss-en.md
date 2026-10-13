---
audio: false
generated: true
image: false
lang: en
layout: post
title: Database Survives Power Loss
translated: false
type: note
---

**Phase 2 delivered — the database now survives power loss.** Committed as `june` (804 lines added).

## What was built

**Write-ahead log (`wal.c`) with real LSN semantics:**

- Every mutation records a **seq-numbered JSON effect** before being confirmed, and is `fsync`'d — `insert` logs the *final* row (auto-increment preserved), `update` logs post-images, `delete` logs pre-images, DDL logs the schema op
- The snapshot file carries the covered `"seq"`; checkpoints write the snapshot **first**, then truncate the log — so a crash between the two replays duplicates as no-ops. This is the same idea SQLite/PostgreSQL use for LSN bookkeeping
- **Atomic batches**: `{"ops":[...]}` buffers its log lines and flushes on commit — a failing op or a crash leaves nothing partial on disk
- **`BEGIN` / `COMMIT` / `ROLLBACK`** at the REPL run on the same machinery — rollback discards buffered entries, and even a SIGKILL mid-transaction rolls back cleanly on restart

## Proof (tests/crash_recovery.sh — real SIGKILL, no simulation)

```
wal entries before crash: 4
SIGKILL while idle → recover → all 3 committed inserts survived
next auto-increment id is 4          ← PK continuity across the crash
clean exit → checkpoint → wal truncated to 0 lines
BEGIN; insert; SIGKILL → recover → 0 rows  ← uncommitted txn correctly lost
```

Engine suite grew 49 → **66 checks** (crash recovery, rollback visibility, checkpoint idempotency), zero warnings, all green.

## Where it stands & what's left

| | |
| --- | --- |
| ✅ | SQL features: JOIN, aggregates, ALTER, operators, DISTINCT |
| ✅ | Atomic batches + interactive transactions |
| ✅ | WAL durability + crash recovery + checkpoints |
| ⏳ | **pk B-tree index** (the remaining Phase 2 item — full scans are still the only access path) |
| → | **Phase 3**: streaming completions, `explain` plan printing, schema-hallucination validator |

The B-tree is the natural next step if you want an actual index structure; otherwise Phase 3 makes the AI interaction state of the art. Want me to keep going with one of those?
