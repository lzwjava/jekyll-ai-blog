---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Turn Completion Hook
translated: false
type: note
---

This is a **`post_llm_call` shell hook** for Hermes Agent — it fires a macOS notification every time the agent finishes a turn (i.e., after the tool-calling loop completes and the final response is ready).

Let me break it down piece by piece:

---

**Shebang & metadata**

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/on-agent-done.sh
```

Saved to `~/.hermes/agent-hooks/` — that's the directory Hermes watches for lifecycle hooks. This one runs automatically after each LLM call completes.

---

**Payload reading**

```bash
payload="$(cat -)"
```

The hook system pipes a JSON payload to the script via stdin. The payload contains the current context: `cwd`, `extra.user_message`, `extra.conversation_history`, etc.

---

**Data extraction via embedded Python**

```bash
extracted=$(echo "$payload" | python3 -c "...")
```

A quick inline Python script parses the JSON and extracts 3 things:

1. **Directory name** — takes the basename of `cwd` (e.g., `hermes-agent` from `/Users/lzwjava/projects/hermes-agent`)
2. **First 10 chars of the user's message** — so you can see what the last prompt was about
3. **Conversation history count** — how many turns deep you are

These are packed into a pipe-delimited string like `hermes-agent|what's the|3`.

---

**Notification construction**

```bash
subtitle="msg: ${user_preview}  |  turns: ${hist_count}"
```

Builds a subtitle showing the message preview and conversation depth.

---

**macOS notification**

```bash
terminal-notifier \
  -title "Hermes Agent — ${dirname}" \
  -subtitle "${subtitle}" \
  -message "Hermes has completed one turn." \
  -sound Glass \
  -activate com.mitchellh.ghostty \
  -group com.hermes.notification \
  2>/dev/null || true
```

Uses [`terminal-notifier`](https://github.com/julienXX/terminal-notifier) (a macOS notification CLI tool — installable via `brew install terminal-notifier`) to:

- Show a notification like:
  **Hermes Agent — hermes-agent**
  *msg: what's the  |  turns: 3*
  Hermes has completed one turn.
- Plays the `Glass` system sound
- `-activate com.mitchellh.ghostty` makes clicking the notification bring **Ghostty** (your terminal emulator) to front instead of just opening Notification Center
- `-group com.hermes.notification` groups all Hermes notifications together (so macOS replaces old ones rather than stacking them)

---

**Hook system requirement**

```bash
printf '{}\n'
```

The hook system expects a JSON object on stdout (even if empty) as an acknowledgment. `{}` means "all good, proceed." Without this, Hermes might log a warning.

---

**Why you'd want this**: if you run long tasks in the background or step away while Hermes works, this ping lets you know the agent is done and ready for your next input — without having to keep checking the terminal.
