---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Coding Agent Whip-Cracking Skills
translated: false
type: note
---

This is **bonk-skills** — a collection of 28 "whip-cracking" skills for AI coding agents (Cursor, Claude Code, Codex, opencode, etc.).

The core idea: each skill is a **semantic button** that forces the AI agent into a specific working mode. Instead of politely asking the agent to do something, you type a short, blunt command and it must comply — no negotiation.

**Structure:** Each skill is a folder with a `SKILL.md` file containing YAML frontmatter (name + trigger description) and a strict behavior protocol: what to do immediately, hard bans (what the agent is NOT allowed to do), and output format.

**The 6 classes of skills:**

1. **Quality rejection** (`/gfy`, `/cringe`, `/skill-issue`) — Reject bad output, force a redo, audit for taste issues
2. **Action drivers** (`/jfdi`, `/stfu`, `/brrr`, `/yolo`) — Stop planning and execute, keep output short, max parallelism, skip confirmations
3. **Investigate the truth** (`/wtf`, `/sus`, `/fafo`, `/rtfm`, `/cap`) — Freeze writes and explain root cause, list hypotheses, verify for real, read docs not memory, fact-check claims
4. **Direction correction** (`/ngmi`, `/cope`, `/rage-quit`, `/ratio`) — Reject current path, stop making excuses, reset the session, admit when you're wrong
5. **Complexity control** (`/midwit`, `/touch-grass`, `/srs`) — Produce the simple version, ban new abstractions, give a real verdict instead of hedging
6. **Positive feedback** (`/based`) — Lock in what the user liked, record it as a session preference

Plus 9 extras like `/eli5`, `/tldr`, `/iykyk`, `/dgaf`, `/fml`, etc.

**Design philosophy:** The profanity is the shell; the behavior protocol is the core. Each skill anticipates exactly how the agent will try to weasel out and explicitly bans those escape routes. Commands are stackable — e.g. `/stfu /brrr` means "shut up and go parallel."

**Install:** Copy skill folders into your agent runtime's skills directory (`~/.cursor/skills/`, `~/.claude/skills/`, etc.).
