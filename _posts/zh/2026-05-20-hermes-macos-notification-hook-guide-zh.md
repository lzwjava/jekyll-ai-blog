---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes macOS 通知钩子指南
translated: true
type: note
---

## Hermes macOS 任务完成通知钩子 — 使用指南

### 功能说明

每当代理完成一次对话轮次时，macOS 通知中心会弹出一条提示，显示：

- **标题：** `Hermes Agent — <项目目录>`（例如 `hermes-agent`、`jekyll-ai-blog`）
- **副标题：** `msg: hello worl | turns: 12`（用户查询的前10个字符 + 消息总数）
- **提示音：** Glass
- **不抢夺焦点** — 通知静默显示在通知中心

### 文件：`~/.hermes/agent-hooks/on-agent-done.sh`

```bash
#!/usr/bin/env bash
# Hermes 完成对话轮次时的 macOS 通知
# 通过 post_llm_call shell 钩子触发

set -euo pipefail

# 从标准输入读取 JSON 数据
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

# 为钩子系统返回静默空操作
printf '{}\n'
```

### 配置：添加到 `~/.hermes/config.yaml`

```yaml
hooks:
  post_llm_call:
    - command: "~/.hermes/agent-hooks/on-agent-done.sh"
      timeout: 5
hooks_auto_accept: true
```

### 测试

```bash
echo '{"hook_event_name":"post_llm_call","cwd":"/Users/lzwjava/projects/hermes-agent","extra":{"user_message":"hello world","conversation_history":[{"role":"system","content":""},{"role":"user","content":"hello"}]}}' \
  | ~/.hermes/agent-hooks/on-agent-done.sh
```

应该能看到通知弹出。如果没有，请检查：

1. **macOS 专注模式/勿扰模式** — 通知中心可能正在阻止显示
2. **声音权限** — 某些 macOS 版本需要为每个应用启用通知声音。前往系统设置 → 通知 →（触发应用）→ 启用声音
3. **`hooks_auto_accept: true`** — 缺少此设置时，首次触发钩子会在 CLI 中显示同意提示

### 数据载荷结构

`post_llm_call` 钩子通过标准输入接收 JSON 数据：

| 字段 | 来源 | 用途 |
|-------|--------|----------|
| `cwd` | 钩子触发时的 `Path.cwd()` | 标题中的目录名称 |
| `extra.user_message` | 用户的原始查询 | 预览文本 |
| `extra.conversation_history` | 完整消息列表 | 对话轮次计数 |
| `extra.assistant_response` | AI 的回复 | （可扩展） |
| `extra.model` | 模型名称 | （可扩展） |
| `extra.platform` | `"cli"`、`"gateway"` 等 | （可扩展） |

### 为何使用 `osascript` 而非 `terminal-notifier`

来自 Homebrew 的 `terminal-notifier` **未进行代码签名** — macOS 通知中心会静默丢弃其通知。可以通过临时签名解决：

```bash
sudo codesign --force --sign - /opt/homebrew/bin/terminal-notifier
```

但 `osascript` 无需签名即可正常工作。不过，`osascript` 的 `display notification` 无法实现点击激活（点击时聚焦终端）— 只有 `terminal-notifier -activate` 可以。如果需要点击激活功能，请临时签名 terminal-notifier 并切换回来。

### 自定义思路

- **添加模型名称：** 在 Python 提取部分添加 `model = data.get('extra', {}).get('model', '')[:20]`，然后追加到副标题
- **不同提示音：** 将 `"Glass"` 替换为 `"Basso"`、`"Frog"`、`"Pop"`、`"Submarine"`、`"Tink"` 或 `~/Library/Sounds/` 中的任何文件
- **按平台过滤：** 如果平台是 `gateway`（来自 Telegram 等机器人的回复），则跳过通知
- **静默模式：** 如果 `subtitle` 以 `msg:  ` 开头（空消息 — 可能是定时任务？），则跳过
