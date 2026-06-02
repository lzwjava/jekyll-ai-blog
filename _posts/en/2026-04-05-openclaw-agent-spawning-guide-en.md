---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Coding Agent Spawning Guide
translated: false
type: note
---

Question: How does "spawn coding agent" work in OpenClaw (AI agent)?

Answer:

## How Spawning a Coding Agent Works in OpenClaw

OpenClaw is an open-source personal AI agent framework. One of its most powerful features is the ability to **spawn sub-agents** — background agent sessions that handle specific tasks (like a large refactor) independently, without blocking your main agent conversation.

---

### What Is a "Spawn Coding Agent"?

Sub-agents are background agent runs spawned from an existing agent run. They run in their own isolated session (`agent:<agentId>:subagent:<uuid>`) and, when finished, announce their result back to the requester's chat channel. Each sub-agent run is tracked as a background task.

This is exactly what the message "spawn coding agent now, ~2h" means — OpenClaw is about to kick off a long-running coding task (like rewriting your JSSDK + CI4 controllers) as a background agent, freeing your main session while the work runs.

---

### How to Spawn a Coding Agent

#### Method 1: Slash Command (Manual)

```
/subagents spawn <agentId> <task> [--model <model>] [--thinking <level>]
```

The spawn command is non-blocking; it returns a run ID immediately. On completion, the sub-agent announces a summary/result message back to the requester chat channel.

#### Method 2: Via the `sessions_spawn` Tool (Agent-triggered)

The main agent can call `sessions_spawn` internally during its reasoning, with these parameters:

- `task` (required) — what the sub-agent should do
- `model?` — override the model for this sub-agent
- `thinking?` — override thinking level
- `runTimeoutSeconds?` — abort after N seconds if set
- `thread?` — keep the session bound to a chat thread for follow-ups
- `mode?` — `run` (one-shot) or `session` (persistent, requires `thread: true`)

---

### Coding Agent Backends (ACP Agents)

OpenClaw delegates coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs, (3) refactoring large codebases, (4) iterative coding that needs file exploration.

Each backend has different invocation requirements:

- **Codex / Pi / OpenCode** → require `pty:true` (interactive terminal)
- **Claude Code (`claude` CLI)** → use `--print --permission-mode bypassPermissions` (no PTY needed)

Example bash invocations:

```bash
# Quick one-shot with Codex (auto-approves, PTY required)
bash pty:true workdir:~/project command:"codex exec --full-auto 'Rewrite JSSDK for CI4'"

# Long background refactor
bash pty:true workdir:~/project background:true command:"codex --yolo 'Refactor all CI4 controllers'"

# Claude Code (no PTY)
claude --print --permission-mode bypassPermissions 'Rewrite the JSSDK module'
```

---

### Nesting & Concurrency Rules

By default, sub-agents cannot spawn their own sub-agents (`maxSpawnDepth: 1`). You can enable one level of nesting by setting `maxSpawnDepth: 2`, allowing the orchestrator pattern: main → orchestrator sub-agent → worker sub-sub-agents.

Each agent session can have at most `maxChildrenPerAgent` (default: 5) active children at a time. This prevents runaway fan-out from a single orchestrator.

---

### Monitoring & Controlling Sub-Agents

Use `/subagents` to inspect or control sub-agent runs for the current session:

| Command | Purpose |
|---|---|
| `/subagents list` | See all active sub-agents |
| `/subagents log <id>` | View progress/output |
| `/subagents info <id>` | Status, timestamps, session ID |
| `/subagents kill <id>` | Stop a specific agent |
| `/subagents steer <id> <msg>` | Send mid-task guidance |

---

### Important Safety Rules

Never checkout branches in `~/Projects/openclaw/` — that's the LIVE OpenClaw instance. When you spawn coding agents in the background, keep the user in the loop. Send 1 short message when you start (what's running + where). If an agent fails or hangs, respawn it or ask the user for direction — don't silently take over.

Never start Codex inside your OpenClaw state directory (`$OPENCLAW_STATE_DIR`, default `~/.openclaw`) — it will read your soul docs and get confused about the org chart!

---

### Applied to Your CI4 Refactor Decision

When OpenClaw says **"spawn coding agent now, ~2h"**, it means:

1. It will call `sessions_spawn` or execute a background `bash` command
2. A Codex/Claude Code agent starts in your project directory
3. It autonomously edits files, runs tests, and works for ~2 hours
4. When done, it posts a summary back to your chat
5. You can monitor progress with `/subagents log` at any time

References:

- [OpenClaw Sub-Agents Official Docs](https://docs.openclaw.ai/tools/subagents)
- [coding-agent-local Skill on LLMBase](https://llmbase.ai/openclaw/coding-agent-local/)
- [openclaw/openclaw SKILL.md on GitHub](https://github.com/openclaw/openclaw/blob/main/skills/coding-agent/SKILL.md)
- [OpenClaw Complete Guide – Lenny's Newsletter](https://www.lennysnewsletter.com/p/openclaw-the-complete-guide-to-building)
