---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Claude Code Router Startup Timeout
translated: false
type: note
---

**Question:** Why does Claude Code Router (`ccr`) fail to start, showing "Service startup timeout" even after `ccr restart` reports success?

**Answer:**

This is a very common and well-documented issue with `claude-code-router`. Here are the most likely causes and fixes:

---

## Root Causes

### 1. `claude` command not found in `$PATH` (Most Common on Mac/zsh)

The service crashes silently with `/bin/sh: claude: command not found` because `ccr` spawns the background service using `/bin/sh`, which does **not** load your shell aliases or `~/.zshrc`. If `claude` is installed as an alias (e.g., `alias claude=...`) or lives in a path only in `.zshrc`, the daemon won't find it.

**Fix:** Make sure `claude` is accessible as a real binary in a standard `PATH` location, not just as a shell alias. Check:

```bash
which claude        # should return a real path, not "aliased to..."
ls -la $(which claude)
```

If it's only an alias, add the real path to `/etc/paths` or create a symlink:

```bash
sudo ln -sf ~/.claude/local/claude /usr/local/bin/claude
```

---

### 2. Config file is missing or malformed

Most startup failures come down to either a port conflict or a malformed `config.json` file. The most common config mistake is a mismatch between the model name in `Providers` and the one in `Router` — both must be identical.

Check your config:

```bash
cat ~/.claude-code-router/config.json
```

Make sure it is valid JSON (no comments, no trailing commas) and that provider model names exactly match router model names.

---

### 3. Port 3456 already in use

If the port is occupied or the service failed to start, you'll see connection refused errors. Check the server logs in `~/.claude-code-router/logs/` for details.

```bash
lsof -i :3456
```

If something is already on that port, kill it or configure a different port.

---

### 4. Known race condition bug in the router itself

The `claude-code-router` service was experiencing a race condition where HTTP requests arriving during server startup could access an undefined `providerService`. The issue stems from the constructor pattern: constructors in JavaScript are synchronous and return immediately, but the original code was initiating asynchronous initialization of `ProviderService` within callbacks. This caused intermittent startup failures.

**Fix:** Update to the latest version:

```bash
npm update -g @musistudio/claude-code-router
```

---

## Debugging Steps

1. **Check the logs directly:**
```bash
tail -f ~/.claude-code-router/logs/$(ls -t ~/.claude-code-router/logs/ | head -1)
```

2. **Run `ccr start` manually in foreground** to see actual error output:
```bash
ccr start
```

3. **Verify `claude` is accessible from a non-interactive shell:**
```bash
/bin/sh -c "which claude"
```

4. **Check if service is actually running after `ccr restart` reports success:**
```bash
ccr status
curl http://127.0.0.1:3456
```

---

## Summary Table

| Cause | Fix |
|---|---|
| `claude` not in `/bin/sh` PATH | Symlink to `/usr/local/bin/claude` |
| Malformed `config.json` | Validate JSON, fix model name mismatch |
| Port 3456 occupied | `lsof -i :3456` and kill the process |
| CCR version bug (race condition) | `npm update -g @musistudio/claude-code-router` |

**References:**

- [Issue #544: CCR start and then stop immediately](https://github.com/musistudio/claude-code-router/issues/544)
- [Issue #211: running `ccr code` asks to run service manually](https://github.com/musistudio/claude-code-router/issues/211)
- [Issue #1258: Fixing the ProviderService Race Condition](https://github.com/musistudio/claude-code-router/issues/1258)
- [DataCamp: Claude Code Router tutorial](https://www.datacamp.com/tutorial/claude-code-router)
