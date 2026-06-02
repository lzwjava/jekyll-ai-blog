---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Iteration Budget Explanation
translated: false
type: note
---

Here's how the iteration budget works in Hermes:

## Iteration Budget — How It Works

**The core class** is `agent/iteration_budget.py` — a thread-safe consume/refund counter (~62 lines). Each `AIAgent` instance (parent or subagent) holds one.

**Defaults:**

- Parent agent: `max_iterations=90` (configurable)
- Subagents (via `delegate_task`): `delegation.max_iterations` (default 50), independent budget

**The loop** in `agent/conversation_loop.py` line 796:

```python
while (api_call_count < agent.max_iterations
       and agent.iteration_budget.remaining > 0) \
      or agent._budget_grace_call:
```

Each iteration = one API call (which may include multiple tool calls in that turn).

**Budget flow per iteration:**

1. **Check interrupt** — if user sent `/stop` or new message, break immediately
2. **Grace call check** — if `_budget_grace_call` is set, consume the flag and let this one last iteration run (then exit regardless)
3. **`consume()`** — tries to deduct 1 from remaining. If already at 0, prints the ⚠️ warning you saw and breaks
4. **Run API call** — model responds, tools execute
5. **Refund on certain conditions:**
   - `execute_code` iterations get refunded (line 3403, 3883) — programmatic tool calls don't eat your budget
   - Context compression restarts get refunded (line 3403) — retrying with compressed context doesn't count
   - Ollama context-too-small errors get refunded (line 1100)

**When budget is fully exhausted** (line 4332-4349):

- If no final response yet, Hermes strips all tools and makes ONE extra call asking the model to summarize what it's done so far
- This is the "grace call" — the model gets a chance to wrap up cleanly instead of just dying mid-tool-use

**The message you saw:**

```
⚠ Iteration budget reached (60/60) — response may be incomplete
```

This means the agent hit `max_iterations=60` (either configured in your config.yaml or set by the caller). The response was the model's summary attempt after budget exhaustion.

**Key design decisions:**

- Budget is per-agent, not global — a subagent burning 50 iterations doesn't消耗 the parent's budget
- Thread-safe via `threading.Lock` — safe for concurrent gateway sessions
- Refunds prevent `execute_code` loops from starving the main conversation
- The grace call ensures you always get some response, even if truncated
