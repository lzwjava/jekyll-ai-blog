---
audio: false
generated: true
image: false
lang: en
layout: post
title: Response Truncation Root Causes
translated: false
type: note
---

Now I have a clear picture. Here's the full analysis:

---

## Why "Response truncated due to output length limit"

This error comes from the agent conversation loop in `agent/conversation_loop.py`. It fires when the LLM API returns `finish_reason="length"` — meaning the model **hit its max output token cap** before it could finish its response.

### The three trigger paths

1. **Truncated tool call (line 1714–1777):** The model started generating a tool call (e.g. `write_file(...)`) but the JSON arguments got cut off mid-stream. The agent retries up to 3 times with boosted `max_tokens`. If all 3 retries still truncate, it gives up and returns this error — because executing a tool with broken JSON args would be dangerous.

2. **Truncated tool call detected during JSON validation (line 3900–3922):** Later in the loop, when the agent tries to parse tool call arguments, it checks if the JSON is incomplete (doesn't end with `}` or `]`). If truncated, same error.

3. **Truncated text response after 3 continuation attempts (line 1655–1712):** The model's text response got cut off. The agent tries to continue by injecting "please continue" prompts up to 3 times. If it's still truncated after 3 tries, it returns a slightly different error: `"Response remained truncated after 3 continuation attempts"`.

### Root causes

| Cause | What happens |
|---|---|
| **`max_tokens` too low** | The model runs out of output budget. Common with long tool calls or verbose responses. |
| **Thinking budget exhaustion** | The model spends ALL output tokens on `` blocks, leaving nothing for the actual response. Detected separately (line 1592–1651) with a specific "Thinking Budget Exhausted" message. |
| **Network/stream interruption** | Partial stream stub (`PARTIAL_STREAM_STUB_ID`) — the connection dropped mid-response. The agent distinguishes this from real truncation. |
| **Ollama/GLM quirk** | Some providers return `finish_reason="stop"` for what's actually a truncation. The agent has a heuristic (`_should_treat_stop_as_truncated`) to catch these. |

### What to do about it

- **If it's the model hitting max_tokens:** Increase `max_tokens` in your config or via `/maxtokens`. The agent already auto-boosts on retry (line 1741–1747: `_tc_boost_base * (retry + 1)`, capped at 32768).
- **If it's thinking exhaustion:** Use `/thinkon low` or `/thinkon minimal` to reduce reasoning token spend, or switch to a non-reasoning model.
- **If it's network-related:** The stream stall detection (`_is_stub_stall`) handles this — it's a transient issue, usually resolves on retry.

Which specific scenario are you hitting? I can dig deeper into the logs or your config if you share more context.
