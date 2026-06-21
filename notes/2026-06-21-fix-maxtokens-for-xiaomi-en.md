---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix max_tokens for Xiaomi
translated: false
type: note
---

OK here's the full picture after inspecting your config and the codebase.

---

## Your Setup

**Config:** `~/.hermes/config.yaml`
- Model: `mimo-v2.5-pro`
- Provider: `xiaomi`
- Base URL: `https://token-plan-cn.xiaomimimo.com/v1`
- **No `max_tokens` configured anywhere** — not in `model:`, not in `agent:`, not in `.env`

**Provider profile:** `plugins/model-providers/xiaomi/__init__.py`
- `default_max_tokens` is **not set** (defaults to `None`)

---

## Root Cause

The xiaomi provider profile has **no `default_max_tokens`**. Your config also doesn't set one. So when the agent calls the Xiaomi API, **no `max_tokens` parameter is sent at all** — the server picks its own default.

The server's default output cap for mimo-v2.5-pro appears to be relatively low. When the model generates a response that exceeds that server-side limit, the API returns `finish_reason="length"`, and Hermes reports:

    Error: Response truncated due to output length limit

The retry mechanism (up to 3 attempts with boosted max_tokens) also doesn't help much because the boost starts from `agent.max_tokens` which is `None`, falling back to `4096` as the base:

```python
# conversation_loop.py line 1741
_tc_boost_base = agent.max_tokens if agent.max_tokens else 4096
_tc_boost = _tc_boost_base * (truncated_tool_call_retries + 1)
```

So on retry it sends `max_tokens=8192`, then `12288`, then `16384` — which may still be under the server's actual limit.

---

## Fix

Add `max_tokens` to your config. The opencode-zen plugin already knows mimo-v2.5-pro supports **131072** completion tokens. Set it in `config.yaml`:

```yaml
model:
  default: mimo-v2.5-pro
  provider: xiaomi
  base_url: https://token-plan-cn.xiaomimimo.com/v1
  max_tokens: 131072    # <-- add this line
```

Or more conservatively if you want to save tokens:

```yaml
  max_tokens: 32768
```

Want me to add it to your config?
