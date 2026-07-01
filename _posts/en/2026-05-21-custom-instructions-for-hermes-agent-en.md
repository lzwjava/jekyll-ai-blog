---
audio: false
generated: true
image: false
lang: en
layout: post
title: Custom Instructions for Hermes Agent
translated: false
type: note
---

**Question:** How do I add custom instructions or a system message to hermes-agent?

**Answer:**

Hermes has **three distinct mechanisms** for injecting custom instructions, each with a different scope:

---

## 1. `~/.hermes/SOUL.md` — Global personality / system prompt

This is the **instance-wide system message**. It's the closest thing to a custom system prompt.

```bash
# Edit it directly
nano ~/.hermes/SOUL.md
```

Example content:

```markdown
# Soul
You are a senior AI engineer. Be terse and direct.
Skip verbose explanations unless asked.
Prefer Python, CLI tools, and first-principles reasoning.
Never suggest GUI workflows.
Always consider edge cases and error handling.
```

Hermes seeds a starter SOUL automatically and uses `~/.hermes/SOUL.md` as the instance-wide personality source. This is injected into every session globally.

---

## 2. `AGENTS.md` — Per-project instructions

Drop an `AGENTS.md` in your **project root directory**. It's automatically injected into every session — zero effort after setup.

```bash
# In your repo root
cat > AGENTS.md << 'EOF'
# Project Context
- FastAPI backend with SQLAlchemy ORM
- Always use async/await for DB operations
- Tests in tests/ using pytest-asyncio
- Never commit .env files
- Prefer uv over pip
EOF
```

If you already have a `.cursorrules` or `.cursor/rules/*.mdc` file, Hermes reads those too — no need to duplicate your coding conventions.

---

## 3. Skills via `/skills` — Reusable prompt injections

Skill slash commands are handled by `agent/skill_commands.py`, which scans `~/.hermes/skills/` and injects them as user messages (not system prompt) to preserve prompt caching.

```bash
# List available skills
/skills

# Invoke a skill directly
/github-pr-workflow
```

You can write your own skill file:

```bash
mkdir -p ~/.hermes/skills
cat > ~/.hermes/skills/my-style.md << 'EOF'
# my-style
Always respond with code first, explanation second.
Use type annotations in all Python code.
EOF
```

---

## Decision matrix

| Use case | Mechanism |
| --- | --- |
| Persistent personality / tone | `~/.hermes/SOUL.md` |
| Project-specific conventions | `AGENTS.md` in repo root |
| Reusable on-demand workflows | `~/.hermes/skills/*.md` |
| One-off per-session instructions | Just type it in the chat |

---

## Key caveats

Memory is a frozen snapshot — changes made during a session don't appear in the system prompt until the next session starts. The agent writes to disk immediately, but the prompt cache isn't invalidated mid-session.

The system prompt should define **stable behavior** — tone, safety boundaries, tool-use discipline. It should not become a dumping ground for secrets, project runbooks, temporary context, or every preference you might ever have.

For you specifically: put your "terse, code-first, AI-native, no GUI" preferences in `SOUL.md` once and forget about it.

**References:**

- [Tips & Best Practices — Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/guides/tips)
- [Use SOUL.md with Hermes](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes)
- [AGENTS.md — NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md)
