---
audio: false
generated: true
image: false
lang: en
layout: post
title: Agent Notification for Context Switching
translated: false
type: note
---

Question: I thought of a simple way to manage 10+ OpenClaw or Hermes agent sessions — writing a program that reminds me to switch context via Telegram notification or desktop notification, so I can check which terminal to look at and whether an agent task is done. How does this idea sound?

Answer:

## Idea Assessment: Simple Multi-Agent Context Switcher

This is a **genuinely practical idea** and you're thinking about it the right way — **don't over-engineer, just stay informed**.

---

### Why This Makes Sense

Running multiple instances of the same agent creates coordination overhead that often cancels out the productivity gains. So instead of trying to make agents talk to each other, **you become the lightweight coordinator** — and your notifier script is the glue.

Claude Code's Agent View shows what every session is doing and which ones need your input — you can dispatch new sessions, watch their state at a glance instead of scrolling through transcripts, and step in only when one needs you. Your idea is essentially building the same mental model for OpenClaw/Hermes sessions that don't have a built-in dashboard.

---

### Simple Script Design (Python)

Here's a minimal approach — **no framework, just polling + notify**:

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

### What This Gives You

| Feature | How |
|---|---|
| **Rotating reminders** | Cycles through all agents every N minutes |
| **Desktop popup** | `osascript` (Mac) or `notify-send` (Linux) |
| **Telegram alert** | Tells you which tmux/terminal window to check |
| **Task label** | You always know what that agent was doing |
| **Zero dependency on agent internals** | Works with OpenClaw, Hermes, Claude Code, anything |

---

### Tips to Make It Even Better

- **Use `tmux` named sessions** — name them `agent-auth`, `agent-test`, etc. so the notification directly tells you `tmux attach -t agent-auth`
- **Add a simple status file** — each agent writes `DONE` or `WAITING` to a `.status` file, your watcher reads it and only notifies for active ones
- **Skip completed agents** — check the status file and remove agents from rotation once done

```bash
# Agent writes this when done:
echo "DONE" > ~/.agents/agent-1.status

# Watcher skips it:
if cat ~/.agents/agent-1.status == "DONE": skip
```

---

### Overall Verdict

✅ **Simple, smart, no over-engineering**
✅ **Works across any agent framework** — OpenClaw, Hermes, Claude Code
✅ **Telegram is perfect** — you see it even when away from desk
✅ **The rotating "which terminal to check" concept is the key insight** — most people just forget which session is running what

If you want a 24/7 personal-agent surface in Telegram or terminal — not in a code repo or workspace orchestration dashboard — this kind of lightweight setup is exactly the right fit.

Looking forward to hearing how it works for you when you try it!