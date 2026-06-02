---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Notification Hook Setup
translated: false
type: note
---

Done. Here's what was created:

**Script:** `/Users/lzwjava/.hermes/agent-hooks/on-agent-done.sh`

Reads the hook JSON payload from stdin, extracts the working directory, and sends a macOS Notification Center notification via `osascript`. The notification shows:

> **Hermes Agent — jekyll-ai-blog**
> Ready for next input

**Config added to `config.yaml`:**

```yaml
hooks:
  post_llm_call:
    - command: "~/.hermes/agent-hooks/on-agent-done.sh"
      timeout: 5
hooks_auto_accept: true
```

Hooks are loaded at startup, so restart Hermes for it to take effect (`/exit` and relaunch). After that, every time the agent finishes a turn, you'll get a system notification with the current working directory name.

To customize the notification (sound, message, etc.), edit the script — the `osascript` line is near the bottom. Remove `sound name "Glass"` for a silent notification, or use `"Basso"`, `"Funk"`, `"Ping"`, etc. for different alert sounds.
