---
audio: false
generated: true
image: false
lang: en
layout: post
title: Command Logging and Database Features Added
translated: false
type: note
---

Done. Here's what was built:

**New files:**
- `ww/db.py` — SQLite module: `get_db_path()`, `init_db()`, `log_command()`, `parse_command()`
- `ww/db_stats.py` — `ww db` command with 5 subcommands: `stats`, `recent`, `top`, `errors`, `search`

**Modified files:**
- `ww/main.py` — `main()` now captures raw args and logs every invocation (success or error) via try/finally. Dispatch moved to `_main_dispatch()`.
- `.env.example` — added `DB_PATH` documentation
- `.env` — set `DB_PATH=/Users/lzwjava/projects/jekyll-ai-blog/ww.db`
- `~/.zsh/completions/_ww` — added `db` command with all subcommands and `--limit` flag

**Database schema:**
```sql
command_log (
    id, timestamp, raw_command, group_name, subcmd, exit_code, cwd
)
```

**Usage:**
```
ww db stats      -- overall stats, top groups, error rate, busiest days
ww db recent     -- last 20 commands (use --limit N)
ww db top        -- most frequently used commands (use --limit N)
ww db errors     -- recent failed commands
ww db search <pattern>  -- grep through history
```

Every `ww` invocation is now logged — even wrong commands like `ww nonexistent` get captured with their exit code. The `raw_command` column stores the full command string for later parsing/analysis.
