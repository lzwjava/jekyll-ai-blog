---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Save Command Destination
translated: false
type: note
---

**Question:** In the Hermes agent (your `ww`/`zz` CLI agent), where does `/save` persist data to?

**Answer:**

I don't have enough context about your specific Hermes agent implementation to answer definitively. The `/save` command behavior depends entirely on how you wired it up.

To find out fast:

```bash
# If it's a Python CLI agent, grep for save logic
grep -rn "save\|/save\|checkpoint\|persist" ~/path/to/hermes/ --include="*.py" | grep -v ".pyc"

# Check for any config/state files it might write
lsof -p $(pgrep -f hermes) 2>/dev/null | grep REG

# Look for recent file writes in likely dirs
ls -lt ~/.config/hermes/ ~/.local/share/hermes/ ~/.hermes/ 2>/dev/null | head -20

# Or just strace the save command (macOS: use dtruss or dtrace)
# On macOS:
sudo dtrace -n 'syscall::open*:entry /pid == $target/ { printf("%s\n", copyinstr(arg0)); }' -p $(pgrep -f hermes)
```

Common patterns for agent state persistence:

| Pattern | Location |
| --- | --- |
| SQLite | `~/.local/share/<agent>/db.sqlite` |
| JSON/JSONL | `~/.config/<agent>/sessions/` |
| Pickle | `/tmp/<agent>_state.pkl` |
| Markdown/notes | `~/notes/` or cwd |
| Vector store | `~/.cache/<agent>/embeddings/` |

If you paste the relevant portion of your Hermes agent code (the `/save` handler or the state class), I can tell you exactly where it writes and suggest improvements — e.g., switching to SQLite with FTS for searchable conversation history.
