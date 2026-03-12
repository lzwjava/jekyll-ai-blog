---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Configuration Guide 2026
translated: false
type: note
---

**Question:** How to use such settings in Claude Code?

**Answer:**

The file you showed is the user-level configuration file for **Claude Code** (the Anthropic coding agent/CLI tool, often used in terminal or via the VS Code extension).

Place this file at:

- `~/.claude/settings.json` (Linux/macOS)
- `%USERPROFILE%\.claude\settings.json` (Windows)

Claude Code automatically reads this file (both the CLI version and the official Anthropic VS Code extension respect it in recent versions).

Your current file configures three main things:

```json
{
  "feedbackSurveyState": {
    "lastShownTime": 1753996737780
  },
  "skipDangerousModePermissionPrompt": true,
  "env": {
    "ANTHROPIC_BASE_URL": "https://v2-as.pincc.ai",
    "ANTHROPIC_AUTH_TOKEN": "sk-8a25bb9202a81c57xx",
    "CLAUDE_CODE_ATTRIBUTION_HEADER": "0"
  }
}
```

### What each setting does and how it's used

- **`env.ANTHROPIC_BASE_URL`**  
  Changes the API endpoint Claude Code talks to (instead of official api.anthropic.com).  
  → You are pointing it to a reverse proxy / third-party provider / custom Anthropic-compatible server.

- **`env.ANTHROPIC_AUTH_TOKEN`**  
  The API key / bearer token sent to that custom endpoint.  
  → Format usually starts with `sk-` (same as official Anthropic keys).

- **`env.CLAUDE_CODE_ATTRIBUTION_HEADER`** set to `"0"`  
  Most likely disables the attribution / "Powered by Claude" header or watermark that some providers force.

- **`skipDangerousModePermissionPrompt`: true**  
  Automatically accepts / skips the confirmation prompt when using dangerous tools (file write, shell commands, etc.).  
  → Useful for fully automated workflows, but increases risk.

### How to make it work

1. **Save the file correctly**  
   Make sure the path is exactly `~/.claude/settings.json` (create the `.claude` folder if it doesn't exist).

2. **Restart Claude Code sessions**  
   - Terminal: close & reopen terminal, then run `claude` again  
   - VS Code extension: reload VS Code window (`Ctrl+R` or `Cmd+R` on Mac) or restart the extension

3. **Test it**  
   Run in terminal:
   ```
   claude
   ```
   or use the VS Code sidebar / command palette → "Claude Code".

   If configured correctly you should see no login prompt and it should connect to `https://v2-as.pincc.ai` instead of Anthropic directly.

### Notes / common issues (2026 status)

- Some older versions of the VS Code extension ignored `~/.claude/settings.json` → make sure you use a recent version of the **official Anthropic Claude Code** extension.
- If it still asks for login → try temporarily setting the same variables in your shell (`export ANTHROPIC_BASE_URL=...`) before launching, or check GitHub issues for your exact version.
- Many proxy providers (LiteLLM, AskSage, 302.ai, custom gateways, etc.) use exactly this settings.json + `ANTHROPIC_BASE_URL` pattern.

That's the standard and recommended way to use custom endpoints / keys / behavior tweaks in Claude Code.

**References:**

- [Claude Code settings documentation](https://code.claude.com/docs/en/settings)
- [AskSage Claude Code integration guide](https://docs.asksage.ai/docs/integrations/claude-code.html)
- [GitHub issue – VS Code extension custom endpoint support](https://github.com/anthropics/claude-code/issues/8727)
- [GitHub issue – regression with custom ANTHROPIC_BASE_URL](https://github.com/anthropics/claude-code/issues/9010)