---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Desktop bypass permissions mode
translated: false
type: note
---

**Question:** In the Claude macOS desktop app, there's no `--dangerously-skip-permissions` flag like in Claude Code CLI — it keeps prompting "Allow once / Always allow" for code actions. How do I enable bypass mode in the desktop app?

**Answer:**

The desktop app does have an equivalent, but it's gated behind a settings toggle, since there's no CLI flag to pass:

1. Open the Claude app → click your profile menu in the lower-left corner → **Settings** → **Claude Code** → turn on **Allow bypass permissions mode**
2. Restart/open a new Claude Code session, then use the mode selector next to the send button and pick **Bypass permissions**. Auto and Bypass permissions only appear in that selector after you enable them in Desktop settings.
3. You can also set a per-folder permission mode to bypassPermissions</parameter>for a specific project folder.

A few caveats worth knowing:

- **Known bugs.** This is flaky right now. Issue #62907 (Desktop 1.9255.x, embedded Claude Code 2.1.149) reports that even after enabling the toggle, the desktop launcher spawns the child `claude` process with `--permission-mode acceptEdits` and never passes `--dangerously-skip-permissions`, so switching to bypass fails with "Cannot set permission mode to bypassPermissions because the session was not launched with --dangerously-skip-permissions". Issue #29026 also reports that `~/.claude/settings.json` `permissions.allow` rules and `defaultMode: "bypassPermissions"` are ignored by the desktop app entirely. If you hit this, update the app first — and if it persists, the CLI is the reliable path.

- **`defaultMode` in settings.** For the CLI (and theoretically desktop once fixed), the persistent equivalent is:

  ```json
  // ~/.claude/settings.json
  {
    "permissions": {
      "defaultMode": "bypassPermissions"
    }
  }
  ```

  This is the persistent equivalent of launching with `--dangerously-skip-permissions` — set once at the user level and every new session boots into bypass mode.

- **Consider `auto` mode instead.** Since you're on Opus-class models, auto mode lets Claude execute without routine permission prompts — a separate classifier model reviews actions and blocks things like `curl | bash`, force pushes, prod deploys, or exfiltrating sensitive data, while local file ops and dependency installs run freely. It kills ~95% of the prompt fatigue without giving up all guardrails, and it's enabled the same way: Settings → Claude Code, then pick **Auto** in the mode selector. For unattended runs on your MI300X droplet or workstation, bypass in a disposable environment is fine; on your daily M2 Air, auto mode is the better tradeoff.

**References:**

- [Choose a permission mode — Claude Code Docs](https://code.claude.com/docs/en/permission-modes)
- [Claude Desktop doesn't pass --dangerously-skip-permissions to child processes (Issue #62907)](https://github.com/anthropics/claude-code/issues/62907)
- [Desktop app ignores settings.json permissions (Issue #29026)](https://github.com/anthropics/claude-code/issues/29026)
- [How we built Claude Code auto mode — Anthropic](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [Claude Code Desktop Bypass Permissions — Kanaries](https://docs.kanaries.net/topics/AICoding/claude-code-desktop-bypass-permissions)
