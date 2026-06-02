---
audio: false
generated: true
image: false
lang: en
layout: post
title: Track Claude Code in OpenClaw Tools
translated: false
type: note
---

Question: How can I monitor Claude Code's progress and see what it's currently working on inside OpenClaw?

Answer:

## Monitoring Claude Code Progress in OpenClaw

I don't have specific documentation on OpenClaw's exact UI, so let me give you the best general answer and suggest how to find out.Question: How can I monitor and check what Claude Code is currently doing inside OpenClaw?

Answer:

## How to Monitor Claude Code Progress in OpenClaw

There are several ways, from simple to sophisticated:

---

### 🥇 Option 1: ClawPort (Best Visual Dashboard)

ClawPort is a free, open-source visual command center for Claude Code agent teams. It gives you an org map, agent chat, kanban board, cron pipeline monitor, cost dashboard, live log streaming, and memory browser — all in one dashboard.

Install it:

```bash
npm install -g clawport
clawport setup   # auto-detects your OpenClaw workspace
clawport dev     # launches the dashboard
```

What you can see:

- Which agent is running and what tool it's currently using
- Kanban board: queued → in progress → done
- Live log stream
- Token usage and cost per agent

---

### 🥈 Option 2: claw-monitor (Terminal Dashboard)

claw-monitor is a terminal dashboard that provides live session tracking, shows the current tool being executed and total tool calls, elapsed time per session, and agent detail view — select agents with arrow keys and press Enter to expand recent tools and errors.

It watches `~/.openclaw/agents/main/sessions/` and `sessions.json` in real time.

---

### 🥉 Option 3: CLI Status Check (Quickest)

You can check session status directly from the command line using `claude-code-skill session-status myproject` after starting a session.

```bash
# Check what a session is doing
claude-code-skill session-status myproject

# Stream live output
claude-code-skill session-send myproject "status update" --stream
```

---

### 📋 What to Look For When Monitoring

| Signal | Meaning |
|--------|---------|
| Tool calls increasing | It's actively working |
| Same tool repeating | May be stuck in a loop |
| No activity for 5+ min | May need a nudge or hit an error |
| "Write" tool firing | It's creating/editing files |
| "Bash" tool firing | It's running commands |

---

### ✅ Recommended Workflow

```
Start task in OpenClaw
    ↓
Open ClawPort dashboard (or claw-monitor)
    ↓
Check every 10-15 minutes
    ↓
If stuck → message the agent directly in ClawPort chat
    ↓
When done → review output files
```

---

### 💡 Key Insight

OpenClaw is best thought of as the "operations team" — it runs things day-to-day, monitors, and executes recurring processes — while Claude Code is the "engineering team" that builds. For your Todo app task, Claude Code is building, and you use ClawPort or claw-monitor to watch it happen in real time.

References:

- [ClawPort - AI Agent Command Center](https://www.clawport.dev/)
- [claw-monitor on GitHub](https://github.com/DanWahlin/claw-monitor)
- [openclaw-claude-code-skill on GitHub](https://github.com/Enderfga/openclaw-claude-code-skill)
