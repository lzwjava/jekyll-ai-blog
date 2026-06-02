---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯完成通知脚本
translated: true
type: note
---

一切干净——标准输出只有 `{}`，不再有 JSON 警告。最终脚本如下：

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

已应用两项修复：
1. **对 `terminal-notifier` 进行代码签名** —— 采用 ad-hoc 签名，使 macOS 通知中心能够正常显示通知
2. **将噪声输出重定向到 `/dev/null`** —— 之前“Removing previous notification”这一行会向标准输出发送垃圾信息，从而触发 hook JSON 解析警告
