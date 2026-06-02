---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing CCR Code Service Startup Issues
translated: false
type: note
---

Question: Why does `ccr code` not work recently, showing "Service not running, starting service..." and then stopping?

Answer:

This is a **known and common issue** with Claude Code Router (CCR). Based on the GitHub issues, there are several root causes:

---

## Root Causes

### 1. `claude` command not found in PATH (most common)

When `ccr code` tries to auto-start the service and launch Claude Code, it runs `claude` in a `/bin/sh` subprocess — which may not inherit your shell aliases or PATH. The error `/bin/sh: claude: command not found` appears because the `claude` command is set up as a shell alias (e.g., `claude: aliased to /Users/.../.claude/local/claude`) but `/bin/sh` doesn't load shell aliases.

**Fix:** Run `ccr start` separately first in your terminal, then use `ccr code`. Or add the full Claude binary path to `/etc/paths` or your shell's `PATH` in a way that `/bin/sh` can find it.

### 2. Service startup timeout

`ccr code` times out waiting for the background service to start and shows "Service startup timeout, please manually run `ccr start`."

**Fix:** Run `ccr start` manually first, wait for it to confirm it's running, then run `ccr code`.

### 3. `ANTHROPIC_BASE_URL` not being set (routing failure)

The `ccr code` command starts the router service but fails to set the `ANTHROPIC_BASE_URL` environment variable before launching the Claude Code subprocess, causing Claude Code to connect directly to the Anthropic API instead of the configured CCR proxy.

**Fix:** Start and export manually:
```bash
ccr start
export ANTHROPIC_BASE_URL="http://127.0.0.1:3456"
export ANTHROPIC_API_KEY="routing-key"
claude
```

Or use `ccr activate`:
```bash
eval "$(ccr activate)"
claude
```

### 4. Permission denied on the `claude` binary

On some systems (e.g., WSL2 on Windows), the error is `/bin/sh: claude: Permission denied`, meaning the claude binary exists but is not executable.

**Fix:**
```bash
chmod +x ~/.claude/local/claude
```

---

## General Debugging Steps

1. **Check service status:**
   ```bash
   ccr status
   ```

2. **Start the service manually:**
   ```bash
   ccr start
   ```

3. **Check logs** for detailed error messages:
   ```bash
   tail -f ~/.claude-code-router.log
   ```

4. **Verify `claude` is accessible from a non-interactive shell:**
   ```bash
   /bin/sh -c "which claude"
   ```
   If this returns nothing, the PATH is the problem.

5. **Use `ccr activate` as a workaround:**
   ```bash
   eval "$(ccr activate)"
   claude
   ```
   The `activate` command sets the `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`, and `NO_PROXY` environment variables so the `claude` command automatically routes requests through the router.

6. **Update CCR** — this has been a recurring bug with fixes released over time:
   ```bash
   npm update -g @musistudio/claude-code-router
   ```

---

## Summary

The root problem is almost always that the background service fails to start cleanly, or the `claude` binary isn't found/accessible in the subprocess shell that `ccr code` uses. The most reliable workaround is to **run `ccr start` explicitly, then use `claude` directly** after activating the environment variables.

References:

- [CCR Issue #544: CCR start and then stop immediately](https://github.com/musistudio/claude-code-router/issues/544)
- [CCR Issue #211: running `ccr code` asks to run service manually](https://github.com/musistudio/claude-code-router/issues/211)
- [CCR Issue #327: Error starting `ccr code` — Permission denied](https://github.com/musistudio/claude-code-router/issues/327)
- [CCR Issue #1137: `ccr code` not passing routing config to Claude Code subprocess](https://github.com/musistudio/claude-code-router/issues/1137)
- [Claude Code Router GitHub README](https://github.com/musistudio/claude-code-router)
