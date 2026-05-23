---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use Clear to Save API Tokens
translated: false
type: note
---

**Question:** Is using `/clear` frequently (starting new sessions) one of the strategies for saving tokens when using Claude/Hermes agents?

**Answer:**

Yes, exactly. `/clear` is one of the most direct token-saving levers in any agentic CLI workflow. Here's the mental model:

## Why context length = token cost

Every message in a session appends to the context window sent on **each subsequent API call**. So a 50-turn conversation doesn't cost 50 × (last message tokens) — it costs 50 × (cumulative history tokens). This grows quadratically in practice.

```
Turn 1:  100 tokens sent
Turn 5:  500 tokens sent
Turn 20: 2000 tokens sent  ← even if each message is tiny
```

## `/clear` as a scalpel

When you `/clear`:
- Context resets to zero (or just system prompt)
- Next call costs only the new message + system prompt
- You lose history but gain a clean slate

The key insight is that **most tasks don't need full history** — they only need the last 1-3 turns of context. So `/clear` between distinct subtasks is almost always the right call.

## When to `/clear` aggressively

| Scenario | Clear? |
|---|---|
| Switching from debugging to writing | ✅ Yes |
| New file / new feature | ✅ Yes |
| After a long multi-tool exploration | ✅ Yes |
| Mid-debugging a single bug | ❌ No — context is load-bearing |
| Continuing a multi-step plan | ❌ No |

## Other token-saving strategies alongside `/clear`

Since you're building CLI agents (`ww`, `zz`, etc.), you probably already know some of these, but the full picture:

1. **`/clear` frequently** — main lever
2. **Compact system prompts** — don't stuff 2000 tokens of instructions into every session
3. **Tool output truncation** — if your agent reads files/runs bash, truncate stdout aggressively before injecting into context
4. **Summarize-then-clear** — ask Claude to summarize current state → `/clear` → inject summary as first message. Lossy but cheap
5. **Task decomposition** — break large agentic tasks into isolated subtasks, each with its own fresh session
6. **Avoid re-reading unchanged files** — cache file contents client-side, don't re-inject them every turn

## The summarize-then-clear pattern in code

```python
def compress_session(client, history):
    summary = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=history + [{
            "role": "user",
            "content": "Summarize the current task state in <200 words. Include: what's done, what's next, any key variables/paths/decisions."
        }]
    )
    # Now clear history and inject only the summary
    return [{
        "role": "user", 
        "content": f"[Session resumed] Context: {summary.content[0].text}"
    }]
```

This is what Claude Code's "compact" feature does internally — it's just a summarize + clear under the hood.

## Bottom line

Yes, `/clear` is a first-class strategy. The mental habit to build: **treat each `/clear` as a git commit boundary** — finish a coherent unit of work, clear, start fresh. Don't let context accumulate across unrelated tasks just because it's convenient.