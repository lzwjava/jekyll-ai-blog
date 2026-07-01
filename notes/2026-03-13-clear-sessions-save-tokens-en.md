---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clear Sessions Save Tokens Always
translated: false
type: note
---

**Question:** For OpenCode / Claude Code / Codex CLI, should we create a new session or run `/clear` after finishing an unrelated task to reduce token usage, or does prompt caching (as used by Gemini/Claude) handle this automatically so we don't need to worry about it?

---

**Answer:**

## The Short Answer

**Yes, you should `/clear` or start a new session between unrelated tasks.** Prompt caching does help, but it does NOT eliminate the cost of carrying stale context from a previous task — it just makes re-reading that stale context cheaper, not free.

---

## How the Context Window Actually Works

Each message you send in a session **re-sends the entire conversation history** to the model. This is true for Claude Code, OpenCode (using Claude/Gemini backends), and Codex CLI alike.

As the conversation advances through turns, each user message and assistant response accumulates within the context window. Previous turns are preserved completely, following a linear growth pattern.

So a 50-turn session sends significantly more tokens per message than a 5-turn session — even if the model appears to "remember" everything instantly.

---

## What Prompt Caching Actually Does

Prompt caching (used by Anthropic's Claude and Google's Gemini) reduces the **cost** of re-reading already-seen content, but it does not eliminate it:

- Prompt caching works because Claude Code frequently re-reads the same context. Files don't change between requests. System prompts are static. Conversation history grows incrementally. The cache captures all of this.

- In real-world data tracking 100M tokens: 84% of input tokens were served from Anthropic's prompt cache.

- However, cache read tokens count fully against your usage quota. Every message re-sends the complete instruction set regardless of whether it changed. A 100-message session costs 1.5M cache reads just from instructions.

So the cache **reduces cost per token** (to about 10% of standard price), but the tokens still **accumulate and still count**. A long session with irrelevant prior context wastes quota on every subsequent message.

---

## Why `/clear` or New Session Matters for Unrelated Tasks

When you switch to a completely different task within the same session:

1. All prior tool calls, file reads, and conversation turns are still in context.
2. Every new message you send re-sends all that irrelevant history.
3. The model may get confused or "distracted" by stale context (context rot).
4. You pay cache-read tokens for all that irrelevant content repeatedly.

Token costs scale with context size: the more context Claude processes, the more tokens you use. Clear between tasks: Use `/clear` to start fresh when switching to unrelated work. Stale context wastes tokens on every subsequent message.

---

## Practical Guidance Per Tool

### Claude Code

- Use **`/clear`** between unrelated tasks. Use `/compact` when you notice Claude losing track, and `/clear` when switching to completely different work.
- Use **`/compact`** (not `/clear`) when still on the same task but the session is getting long — it summarizes history while preserving intent.
- Claude Code automatically optimizes costs through prompt caching (which reduces costs for repeated content like system prompts) and auto-compaction (which summarizes conversation history when approaching context limits).

### Codex CLI (OpenAI)

- Use the `/compact` command when conversations get long to summarize history and free up tokens.
- Use `/fork` to branch a session for a different approach, preserving the original.
- Starting fresh with a new session for truly unrelated work is recommended.

### OpenCode

- OpenCode is newer and a provider-agnostic `/compact` command and auto-compaction support are proposed features — not yet universally available across all backends.
- Starting a new session between unrelated tasks is still the safest approach for now.

---

## The "One Session Per Logical Task" Rule

One session per logical task works best. One bug fix, one feature, one refactor. Don't try to fix three bugs and add two features in one conversation.

Between sessions, use a `CLAUDE.md` file to persist important project context: A CLAUDE.md file with key architecture decisions, file locations, and conventions means Claude spends fewer tokens rediscovering your project structure each time.

---

## Summary Table

| Scenario | Recommendation |
| --- | --- |
| Same task, long session | `/compact` — summarize, keep going |
| Switching to unrelated task | `/clear` or new session |
| Related follow-up task | Keep session OR use `/compact` first |
| Resuming old work later | `/resume` with `CLAUDE.md` for context |
| Very long codebase analysis | New session per logical unit |

**Bottom line:** Prompt caching is a cost multiplier (cheaper reads), not a "free context" pass. Irrelevant prior context always costs you — clearing it between unrelated tasks is one of the highest-leverage optimizations available.

---

**References:**

- [Claude Code Cost Management Docs](https://code.claude.com/docs/en/costs)
- [Anthropic Context Windows Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [7 Ways to Cut Claude Code Token Usage – DEV Community](https://dev.to/boucle2026/7-ways-to-cut-your-claude-code-token-usage-elb)
- [Claude Code Token Usage: Real Data From 100M Tokens](https://docs.bswen.com/blog/2026-03-10-claude-code-token-usage-per-request/)
- [Claude Code Context Window Optimization](https://claudefa.st/blog/guide/mechanics/context-management)
- [OpenCode /compact Feature Discussion](https://github.com/anomalyco/opencode/issues/4317)
- [Codex CLI Session Resume Guide](https://inventivehq.com/knowledge-base/openai/how-to-resume-sessions)
