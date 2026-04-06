---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Progress Update Methods
translated: false
type: note
---

Question: How does OpenClaw (an AI agent) display real-time progress updates while working on a big problem — does it just repeatedly send updated status messages?

Answer:

## How AI Agents Stream Progress Updates

Yes, essentially — but there are a few different mechanisms depending on the implementation. Here's how it works:

---

### 1. **Server-Sent Events (SSE) — Most Common**

The backend streams incremental updates to the frontend over a persistent HTTP connection.

```
Client → POST /run-agent
Server → keeps connection open, pushes text chunks:
  "data: Checking DB schema...\n\n"
  "data: Found 25 tables...\n\n"
  "data: Spawning coding agent...\n\n"
```

The frontend listens and appends each chunk to the UI in real time. This is how Claude.ai itself works — the text "streams" in word by word.

---

### 2. **WebSocket — Bidirectional**

Similar to SSE but allows two-way communication. The agent sends status frames as it progresses:

```json
{ "type": "status", "message": "Scanning 76 CI3 patterns..." }
{ "type": "status", "message": "Running sed replacement..." }
{ "type": "result", "message": "Done. 76 occurrences fixed." }
```

---

### 3. **Polling — Simpler but Less Elegant**

The frontend repeatedly asks "are you done yet?" every second or two:

```
Client → GET /task/status?id=123  →  { "status": "running", "log": "..." }
Client → GET /task/status?id=123  →  { "status": "running", "log": "..." }
Client → GET /task/status?id=123  →  { "status": "done",    "result": "..." }
```

---

### 4. **How the "Log Lines" Are Generated**

The agent itself just calls a log/emit function at key checkpoints in its code:

```python
emit("Checking DB schema...")
result = check_db()

emit(f"Found {len(tables)} tables")
run_migration()

emit("Spawning coding sub-agent...")
sub_agent.run()
```

Each `emit()` call pushes a message through SSE/WebSocket to the UI. The UI appends it to the visible log.

---

### 5. **What You See in the Document You Shared**

The transcript you pasted is exactly this pattern — an agent narrating its own steps as it goes:

- *"Let me check the DB schema..."* → runs query → emits result
- *"Another CI3→CI4 issue found..."* → emits finding
- *"This is a bulk-fix task. Let me spawn a coding agent..."* → emits spawn event

These are checkpoint log messages, streamed out progressively so the user knows the agent is alive and making progress, not just silently hanging.

---

### Summary

| Mechanism | How it works | Best for |
|---|---|---|
| SSE | One-way HTTP stream | Simple log streaming |
| WebSocket | Persistent two-way socket | Interactive agents |
| Polling | Repeated HTTP requests | Simple/legacy systems |

The agent itself just calls `emit(message)` at each step — the transport layer (SSE/WebSocket) handles getting it to your screen in real time.