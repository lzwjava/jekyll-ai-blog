---
audio: false
generated: true
image: false
lang: en
layout: post
title: SQLite Versus JSON Tooling Comparison
translated: false
type: note
---

**Question:** SQLite has GUI/CLI database clients to view and inspect data — is that an advantage over JSON?

**Answer:**

Yes, that's a real advantage of SQLite. But for your case, JSON still wins because your tooling is already good.

## SQLite client ecosystem

- **TablePlus**, **DBeaver**, **DB Browser for SQLite** — GUI, browse rows, filter, sort
- `sqlite3` CLI — built into macOS/Linux, no install
- VS Code extension — SQLite Viewer, inline table browsing

```bash
sqlite3 data/tt.db "SELECT * FROM punch_days WHERE status='missed_punch'"
```

## But JSON has equivalent tooling

```bash
# jq - already in your README
cat data/contractor_a.json | jq '.punch_days[] | select(.status=="missed_punch")'

# fx - interactive JSON browser (like a GUI)
fx data/contractor_a.json

# gron - makes JSON grep-able
gron data/contractor_a.json | grep missed_punch
```

`jq` is honestly as powerful as SQL for read-only inspection of this data shape. You're already using it.

## The real tradeoff

| | SQLite | JSON |
|---|---|---|
| GUI client | ✅ TablePlus etc | ❌ |
| CLI inspect | ✅ `sqlite3` | ✅ `jq`, `fx` |
| `grep` / `cat` | ❌ binary | ✅ |
| Edit a single value | ❌ need client/SQL | ✅ `vim data/x.json` |
| Non-technical user viewing | ✅ GUI | ❌ |

## Verdict for `tt`

You're the only user, terminal-first, already using `jq`. The GUI client advantage doesn't apply to you. If you were handing this to a non-technical HR person who needs to browse records — SQLite + TablePlus would win immediately. That's the real use case for that advantage.