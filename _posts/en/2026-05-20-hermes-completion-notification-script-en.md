---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Completion Notification Script
translated: false
type: note
---

All clean — only `{}` on stdout, no more JSON warnings. Here's the final script:

```bash
#!/usr/bin/env bash
# ~/.hermes/agent-hooks/on-agent-done.sh
# macOS notification when Hermes finishes a turn.
# Fired via post_llm_call shell hook — runs after the tool-calling loop completes.

set -euo pipefail

# Read the JSON payload from stdin and extract fields
payload="$(cat -)"

extracted=$(echo "$payload" | python3 -c "
import json, sys
data = json.load(sys.stdin)

# Directory name from cwd
cwd = data.get('cwd', '')
import os
dirname = os.path.basename(cwd) if cwd else 'unknown'

# First 10 chars of user message
extra = data.get('extra', {})
user_msg = extra.get('user_message', '')[:10]

# Conversation history item count
history = extra.get('conversation_history', [])
hist_count = len(history)

print(f'{dirname}|{user_msg}|{hist_count}')
" 2>/dev/null) || extracted='unknown||0'

IFS='|' read -r dirname user_preview hist_count <<< "$extracted"

# Build subtitle
subtitle="msg: ${user_preview}  |  turns: ${hist_count}"

# Send macOS notification (clickable — brings Ghostty to front)
terminal-notifier \
  -title "Hermes Agent — ${dirname}" \
  -subtitle "${subtitle}" \
  -message "Hermes has completed one turn." \
  -sound Glass \
  -activate com.mitchellh.ghostty \
  -group com.hermes.notification \
  >/dev/null 2>&1 || true

# Silent no-op for the hook system
printf '{}\n'
```

Two fixes applied:
1. **Code-signed `terminal-notifier`** — ad-hoc signing so macOS Notification Center actually shows the notifications
2. **Redirected noise to `/dev/null`** — the "Removing previous notification" line was spamming stdout and triggering hook JSON parse warnings