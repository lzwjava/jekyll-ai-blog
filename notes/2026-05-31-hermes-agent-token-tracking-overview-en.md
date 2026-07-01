---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Token Tracking Overview
translated: false
type: note
---

Now I have the full picture. Here's how token tracking works in Hermes Agent:

---

There are THREE layers of token tracking:

## 1. Per-API-call accumulation (agent/conversation_loop.py, lines ~1780-1886)

After every API call, the response's `usage` object is normalized via `normalize_usage()` from `agent/usage_pricing.py` into a `CanonicalUsage` dataclass:

```python
CanonicalUsage(
    input_tokens=...,      # raw input (excludes cache)
    output_tokens=...,     # generated tokens
    cache_read_tokens=..., # cache hits
    cache_write_tokens=...,# cache writes
    reasoning_tokens=...,  # thinking/reasoning tokens
)
```

These get accumulated into session counters on the `AIAgent` instance (defined in `run_agent.py` lines 625-636):

```
agent.session_input_tokens      += canonical_usage.input_tokens
agent.session_output_tokens     += canonical_usage.output_tokens
agent.session_cache_read_tokens += canonical_usage.cache_read_tokens
agent.session_cache_write_tokens+= canonical_usage.cache_write_tokens
agent.session_reasoning_tokens  += canonical_usage.reasoning_tokens
agent.session_total_tokens      += total_tokens
agent.session_api_calls         += 1
agent.session_estimated_cost_usd += cost
```

Also persisted to SQLite via `SessionDB.update_token_counts()` (hermes_state.py).

## 2. The /usage slash command

In CLI or gateway, type `/usage`. It:

- Reads the live agent's session counters (mid-turn) or cached agent (between turns)
- Calls `fetch_account_usage()` from `agent/account_usage.py` for provider-level rate limits
- Calls `estimate_usage_cost()` from `agent/usage_pricing.py` for cost estimates
- Shows: model, input tokens, cache read/write, output tokens, total, API calls, cost, context window %

Gateway handler: `gateway/run.py` line 13194 (`_handle_usage_command`).

## 3. Key files to search/read

| What you want | File | What to search |
| --- | --- | --- |
| Token accumulation logic | `agent/conversation_loop.py` | `session_input_tokens`, `canonical_usage` |
| Session counters init | `run_agent.py` | `session_total_tokens = 0` (line 625) |
| Normalize raw API usage | `agent/usage_pricing.py` | `normalize_usage`, `CanonicalUsage` |
| Cost estimation | `agent/usage_pricing.py` | `estimate_usage_cost`, `PricingEntry` |
| SQLite persistence | `hermes_state.py` | `update_token_counts` (line 938) |
| /usage command (gateway) | `gateway/run.py` | `_handle_usage_command` (line 13194) |
| /usage command (CLI) | `cli.py` | search for `usage` in `process_command` |
| Account-level limits | `agent/account_usage.py` | `fetch_account_usage` |
| Provider-specific parsing | `agent/gemini_native_adapter.py` | `usageMetadata`, `promptTokenCount` |
| Insights over time | `agent/insights.py` | `InsightsEngine` |

## Quick way to check your current session's tokens

In the CLI interactive session, just type:

```
/usage
```

Or programmatically after a `chat()` call:

```python
agent = AIAgent(...)
agent.chat("hello")
print(f"In: {agent.session_input_tokens}, Out: {agent.session_output_tokens}, Total: {agent.session_total_tokens}")
print(f"API calls: {agent.session_api_calls}, Cost: ${agent.session_estimated_cost_usd:.4f}")
```

The `/insights` command (line 13331) gives you historical analytics across sessions from the SQLite DB.
