---
audio: false
generated: true
image: false
lang: en
layout: post
title: Custom Rules in Claude Code CLAUDE.md
translated: false
type: note
---

Question: How do you make Claude Code follow custom rules — should you add them to CLAUDE.md or use skills?

Answer:

Great question. Claude Code has several mechanisms for injecting persistent instructions. Here's a comprehensive breakdown:

---

## 1. `CLAUDE.md` — The Primary Method

This is the **most recommended and native** way to give Claude Code persistent instructions.

### How it works

- Claude Code **automatically reads** `CLAUDE.md` at the start of every session
- You can have multiple `CLAUDE.md` files at different levels

### File locations (all are read, in order)

| Location | Scope |
|---|---|
| `~/.claude/CLAUDE.md` | Global — applies to ALL projects |
| `<project-root>/CLAUDE.md` | Project-level — applies to this repo |
| `<subdir>/CLAUDE.md` | Subdirectory-level — applies when working in that folder |

### Example `~/.claude/CLAUDE.md` for your formatting rules

```markdown
## Response Format Rules

Always respond in this exact format:

**Question:** [rephrased and grammar-fixed user question]

**Answer:**
[full answer in clean Markdown, always in English]

**References:**
[only show if there is at least one, use bullet list with [url](url) format]

- No Grok render tags
- Do not show images, prefer text only
- Give comprehensive explanations for exam questions
- Always answer in English, even if the question is in Chinese
- Always search the web before answering
```

---

## 2. Project-level `CLAUDE.md` — For Team/Repo Rules

Place a `CLAUDE.md` in your **project root** for rules specific to that codebase:

```markdown
## Project Conventions
- Use TypeScript strict mode
- All functions must have JSDoc comments
- Run `npm test` before committing
```

This is version-controlled and shared with your team automatically.

---

## 3. Skills (`/mnt/skills/`) — For Claude.ai Web, Not Claude Code

Skills (like the `/mnt/skills/` system you see in **Claude.ai**) are a feature of the **Claude.ai web interface**, not Claude Code CLI. They are pre-loaded instruction files injected by Anthropic's platform.

**Claude Code does NOT support the skills system.** Don't confuse the two.

---

## 4. System Prompt via API / `--system-prompt` flag

If you're calling Claude Code **programmatically or via the SDK**, you can pass a system prompt directly:

```bash
claude --system-prompt "Always answer in English. Follow this format: ..."
```

Or in the SDK:

```javascript
const claude = new Anthropic();
// pass system prompt in your API call
```

---

## 5. `/memory` Command (Runtime)

Inside a Claude Code session, you can use:

```
/memory
```

This lets you **add or edit memory** that persists across sessions — similar to CLAUDE.md but managed interactively.

---

## Best Practice Summary

| Goal | Method |
|---|---|
| Rules for ALL projects globally | `~/.claude/CLAUDE.md` |
| Rules for one specific project | `<project>/CLAUDE.md` |
| Rules for a subfolder | `<subdir>/CLAUDE.md` |
| One-off session rules | Type instructions inline or use `/memory` |
| Programmatic/API usage | `--system-prompt` flag or SDK system param |

---

## Recommendation for Your Use Case

Since your formatting rules (English-only, specific output structure, always search) are **personal preferences** that should apply everywhere, put them in:

```
~/.claude/CLAUDE.md
```

This is the **global CLAUDE.md** and will apply to every project you work on with Claude Code automatically — no per-project setup needed.

References:

- [Claude Code – CLAUDE.md documentation](https://docs.claude.com/en/docs/claude-code/memory)
- [Claude Code overview](https://docs.claude.com/en/docs/claude-code/overview)
