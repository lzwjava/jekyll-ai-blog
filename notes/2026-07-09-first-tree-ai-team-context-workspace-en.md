---
audio: false
generated: true
image: false
lang: en
layout: post
title: "First Tree: AI Team Context Workspace"
translated: false
type: note
---

Here's what **first-tree** is:

## high-level

It's an **open-source workspace + context layer for human-agent teams**. The core idea: instead of every AI agent starting a task cold with an isolated prompt, agents read from — and write back to — a shared, Git-native knowledge base called a **Context Tree**.

Think of it as **team memory that agents and humans maintain together**.

## architecture

It's a pnpm monorepo with 5 packages:

| Package | Role |
|---|---|
| `apps/cli` | `first-tree` / `ftd` CLI — login, daemon, agent management, tree operations |
| `packages/server` | Fastify API server (PostgreSQL/Drizzle/Zod) — the SaaS backend |
| `packages/client` | SDK + AgentRuntime — wraps WebSocket comms, handler registration, codex/copilot runtime glue |
| `packages/shared` | Zod schemas + types shared across server/client/cli — source of truth for DTOs |
| `packages/web` | React 19 + Vite web workspace — the GUI for chats, agents, context tree |

## what problem it solves

When an agent — or a human — needs to understand *why* something was built a certain way, there's usually nowhere to look. PRs get merged, issues closed, documents decay. The Context Tree is a **recursive `NODE.md` structure** (Git repo with markdown files) that holds durable decisions, ownership, constraints, and domain knowledge.

## how it works

1. **Context Tree** — a Git repo of markdown files that agents read before acting
2. **Web workspace** — chat surface for agents, team members, GitHub integration
3. **CLI + daemon** — signs a computer in, keeps local agents connected
4. **Agent runtime** — runs agents (Claude Code, Codex, your own) on your machine, routes through First Tree
5. **GitHub integration** — connects PRs, code reviews back into the workspace

The loop is:

```
user intent -> read team context -> agent works context-aware
-> human review/control -> durable outcome -> updated team context
```

## who made it

From the org name `agent-team-foundation/first-tree` — built by a team that works deeply with AI agents daily.

## how far along

~500 commits on main, CI, Docker compose for local dev, extensive API surface, database migrations, observability (OpenTelemetry), GitHub app integration. It's actively developed — the last few commits were about refactoring agent briefing generation, splitting service lifecycle backends, and surfacing terminal provider failures. Real production shape.

Want me to dive into a specific package or subsystem?