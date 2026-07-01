---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Memory Two Layers Explained
translated: false
type: note
---

Question: Is OpenClaw's memory session-based? When a new session is created, does the chat history disappear?

Answer:

Yes and no — OpenClaw has **two distinct layers of memory**, and understanding the difference is key:

---

## 1. Conversation History (Session-Based — Temporary)

Conversation history is limited to the current session and cleared on restart. The agent remembers everything said in the current conversation, but this history is reset when the OpenClaw instance restarts or a new session begins.

Session history gives you conversation memory, but when you reset a session or start a new one, everything in that session is gone. A separate memory system is needed — persistent knowledge that survives session resets.

---

## 2. Long-Term Memory (Persistent — Survives Sessions)

Long-term memory lets your OpenClaw agent remember information across separate conversations. This is especially useful for personal preferences, project context, and facts about you. Simply tell your agent "Remember that [fact]", and it stores this in long-term memory and automatically uses it in future conversations.

OpenClaw has its AI automatically write daily logs as Markdown files. Those files are the source of truth, and the model only "remembers" what gets written to disk. Human developers can open those Markdown files, edit them directly, and see exactly what the AI remembers at any point.

---

## How Sessions Are Managed

Sessions are reused until they expire, and expiry is evaluated on the next inbound message. By default, a daily reset occurs at 4:00 AM local time on the gateway host. A session is considered stale once its last update is earlier than the most recent daily reset time. An optional idle reset (`idleMinutes`) adds a sliding idle window.

---

## Session Logs Are Still Saved to Disk

Even though chat history is cleared from the active context, session logs live under `~/.openclaw/agents/<agentId>/sessions/` as an index file and per-session `.jsonl` transcripts. Each line is a JSON object with metadata and message entries.

When starting a new session, OpenClaw can automatically save the previous conversation to a timestamped file with a descriptive slug. These session transcripts are indexed and searchable, allowing agents to recall past conversations.

---

## Summary Table

| Memory Type | Persists Across Sessions? | Where Stored |
| --- | --- | --- |
| Conversation History | ❌ No | In-memory only |
| Long-Term Memory (MEMORY.md) | ✅ Yes | Disk (Markdown files) |
| Session Logs (.jsonl) | ✅ Yes (readable/searchable) | `~/.openclaw/.../sessions/` |

**Bottom line:** Active chat history is cleared on new sessions, but you can preserve important information by explicitly telling the agent to remember it, or by using the session log search tools to retrieve past conversations.

References:

- [https://openclawlaunch.com/guides/openclaw-memory](https://openclawlaunch.com/guides/openclaw-memory)
- [https://docs.openclaw.ai/concepts/session](https://docs.openclaw.ai/concepts/session)
- [https://snowan.gitbook.io/study-notes/ai-blogs/openclaw-memory-system-deep-dive](https://snowan.gitbook.io/study-notes/ai-blogs/openclaw-memory-system-deep-dive)
- [https://playbooks.com/skills/openclaw/openclaw/session-logs](https://playbooks.com/skills/openclaw/openclaw/session-logs)
- [https://milvus.io/blog/we-extracted-openclaws-memory-system-and-opensourced-it-memsearch.md](https://milvus.io/blog/we-extracted-openclaws-memory-system-and-opensourced-it-memsearch.md)
