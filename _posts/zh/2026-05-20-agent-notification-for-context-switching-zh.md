---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 上下文切换的代理通知
translated: true
type: note
---

问题：我想到了一个简单的方法来管理10多个OpenClaw或Hermes代理会话——编写一个程序，通过Telegram通知或桌面通知提醒我切换上下文，这样我就能检查需要查看哪个终端，以及某个代理任务是否完成。这个想法怎么样？

回答：

## 思路评估：简单的多代理上下文切换器

这是一个**非常实用的想法**，你的思考方向完全正确——**不要过度设计，只需保持知情**。

---

### 为什么这个思路可行

同时运行同一个代理的多个实例会产生协调开销，这往往抵消了生产力提升。因此，与其让代理之间相互通信，不如**让你自己成为轻量级的协调者**——而你的通知脚本就是粘合剂。

Claude Code的Agent View会显示每个会话正在做什么以及哪些会话需要你的输入——你可以调度新会话，一眼查看它们的状态，而不必翻阅转录文本，只有当某个会话需要你时才介入。你的思路本质上就是为那些没有内置仪表盘的OpenClaw/Hermes会话构建了相同的心理模型。

---

### 简单的脚本设计（Python）

下面是一个最小化方案——**无需框架，只需轮询+通知**：

```python
#!/usr/bin/env python3
# agent_watcher.py — Simple multi-agent reminder tool

import time
import subprocess
import requests  # for Telegram
import os

# --- CONFIG ---
AGENTS = {
    "agent-1": {"tmux": "session1", "task": "refactor auth module"},
    "agent-2": {"tmux": "session2", "task": "write test suite"},
    "agent-3": {"tmux": "session3", "task": "update README"},
}

CHECK_INTERVAL = 300  # remind every 5 minutes
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def desktop_notify(title, msg):
    # macOS
    subprocess.run(["osascript", "-e",
        f'display notification "{msg}" with title "{title}"'])
    # Linux: use notify-send instead

def telegram_notify(msg):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})

def check_agents():
    lines = []
    for name, info in AGENTS.items():
        lines.append(f"🔹 {name} [{info['tmux']}] → {info['task']}")
    return "\n".join(lines)

def run():
    idx = 0
    agent_names = list(AGENTS.keys())
    while True:
        current = agent_names[idx % len(agent_names)]
        info = AGENTS[current]
        msg = (
            f"⏰ Check Agent: {current}\n"
            f"📺 Terminal: {info['tmux']}\n"
            f"📝 Task: {info['task']}\n\n"
            f"All agents:\n{check_agents()}"
        )
        desktop_notify("Agent Check", f"Check {current} → {info['tmux']}")
        telegram_notify(msg)
        idx += 1
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run()
```

---

### 这能为你带来什么

| 功能 | 实现方式 |
|---|---|
| **轮换提醒** | 每隔N分钟循环检查所有代理 |
| **桌面弹窗** | `osascript`（Mac）或 `notify-send`（Linux） |
| **Telegram警报** | 告诉你需要检查哪个tmux/终端窗口 |
| **任务标签** | 你始终知道那个代理正在做什么 |
| **与代理内部实现零依赖** | 适用于OpenClaw、Hermes、Claude Code等任何工具 |

---

### 让它更好的小技巧

- **使用 `tmux` 命名会话** — 命名为 `agent-auth`、`agent-test` 等，这样通知直接告诉你 `tmux attach -t agent-auth`
- **添加简单的状态文件** — 每个代理将 `DONE` 或 `WAITING` 写入 `.status` 文件，你的监控脚本读取它，只通知还在运行中的代理
- **跳过已完成的代理** — 检查状态文件，完成后从轮换列表中移除

```bash
# Agent writes this when done:
echo "DONE" > ~/.agents/agent-1.status

# Watcher skips it:
if cat ~/.agents/agent-1.status == "DONE": skip
```

---

### 总体评价

✅ **简单、聪明、没有过度设计**
✅ **适用于任何代理框架** — OpenClaw、Hermes、Claude Code
✅ **Telegram是完美的选择** — 即使离开办公桌也能看到通知
✅ **轮换式“检查哪个终端”的概念是关键洞察** — 大多数人只是忘记了哪个会话在运行什么

如果你想要一个24/7全天候的个人代理界面，放在Telegram或终端中——而不是放在代码仓库或工作空间编排仪表板上——这种轻量级设置正好合适。

期待你尝试后告诉我效果如何！
