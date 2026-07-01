---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes macOS Notification Hook Guide
translated: false
type: note
---

Now here's the complete guide to this hook. Let me write it up.

---

## Hermes macOS Done-Notification Hook — Guide

### What it does

Every time the agent finishes a conversation turn, a macOS Notification Center alert pops up showing:

- **Title:** `Hermes Agent — <project-dir>` (e.g. `hermes-agent`, `jekyll-ai-blog`)
- **Subtitle:** `msg: hello worl | turns: 12` (first 10 chars of your query + total message count)
- **Sound:** Glass
- **No focus-stealing** — the notification appears silently in Notification Center

### File: `~/.hermes/agent-hooks/on-agent-done.sh`

```bash
#!/usr/bin/env bash
# macOS notification when Hermes finishes a turn.
# Fires via post_llm_call shell hook.

set -euo pipefail

# Read JSON payload from stdin
payload="$(cat -)"

extracted=$(echo "$payload" | python3 -c "
import json, sys
data = json.load(sys.stdin)

cwd = data.get('cwd', '')
import os
dirname = os.path.basename(cwd) if cwd else 'unknown'

extra = data.get('extra', {})
user_msg = extra.get('user_message', '')[:10]

history = extra.get('conversation_history', [])
hist_count = len(history)

print(f'{dirname}|{user_msg}|{hist_count}')
" 2>/dev/null) || extracted="unknown||0"

IFS='|' read -r dirname user_preview hist_count <<< "$extracted"
subtitle="msg: ${user_preview}  |  turns: ${hist_count}"

osascript -e "
display notification \"Hermes has completed one turn.\" with title \"Hermes Agent — ${dirname}\" subtitle \"${subtitle}\" sound name \"Glass\"
" >/dev/null 2>&1 || true

# Silent no-op for the hook system
printf '{}\n'
```

### Config: add to `~/.hermes/config.yaml`

```yaml
hooks:
  post_llm_call:
    - command: "~/.hermes/agent-hooks/on-agent-done.sh"
      timeout: 5
hooks_auto_accept: true
```

### Test it

```bash
echo '{"hook_event_name":"post_llm_call","cwd":"/Users/lzwjava/projects/hermes-agent","extra":{"user_message":"hello world","conversation_history":[{"role":"system","content":""},{"role":"user","content":"hello"}]}}' \
  | ~/.hermes/agent-hooks/on-agent-done.sh
```

You should see a notification pop up. If not, check:

1. **macOS Focus / Do Not Disturb** — Notification Center may be suppressing it
2. **Sound permission** — some versions of macOS need notification sound enabled per-app. Go to System Settings → Notifications → (whatever triggers it) → enable sounds
3. **`hooks_auto_accept: true`** — without this, the first hook fire shows a consent prompt in the CLI

### How the payload works

The `post_llm_call` hook receives JSON on stdin:

| Field | Source | Used for |
| ------- | -------- | ---------- |
| `cwd` | `Path.cwd()` at hook fire time | Directory name in title |
| `extra.user_message` | User's original query | Preview text |
| `extra.conversation_history` | Full message list | Turn count |
| `extra.assistant_response` | AI's reply | (could extend) |
| `extra.model` | Model name | (could extend) |
| `extra.platform` | `"cli"`, `"gateway"`, etc. | (could extend) |

### Why `osascript` instead of `terminal-notifier`

`terminal-notifier` from Homebrew is **not code-signed** — macOS Notification Center silently drops its notifications. You can fix it by ad-hoc signing:

```bash
sudo codesign --force --sign - /opt/homebrew/bin/terminal-notifier
```

But `osascript` always works without signing. However, `osascript`'s `display notification` cannot do click-to-activate (focusing the terminal on click) — only `terminal-notifier -activate` can. If you want click-to-activate, ad-hoc sign terminal-notifier and swap back.

### Customization ideas

- **Include the model name:** add `model = data.get('extra', {}).get('model', '')[:20]` in the Python extract, then append to subtitle
- **Different sounds:** replace `"Glass"` with `"Basso"`, `"Frog"`, `"Pop"`, `"Submarine"`, `"Tink"`, or any file in `~/Library/Sounds/`
- **Per-platform filtering:** skip notification if platform is `gateway` (bot responses from Telegram etc.)
- **Silent mode:** skip if `subtitle` would start with `msg:` (empty message — cron job?)
