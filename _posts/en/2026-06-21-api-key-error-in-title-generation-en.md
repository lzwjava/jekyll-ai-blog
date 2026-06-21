---
audio: false
generated: true
image: false
lang: en
layout: post
title: API Key Error in Title Generation
translated: false
type: note
---

Question: Why does "Auxiliary title generation failed: HTTP 401: Invalid API Key" occur?

Answer:

I traced the full code path. Here's what's happening:

## The Flow

1. After the first user/assistant exchange, `maybe_auto_title()` fires a background thread (agent/title_generator.py)
2. It calls `call_llm(task="title_generation", main_runtime=main_runtime)` in agent/auxiliary_client.py
3. `_resolve_task_provider_model()` reads config `auxiliary.title_generation` — yours is set to `provider: auto` with empty model/base_url/api_key
4. `_resolve_auto()` picks up your main provider (xiaomi) + model (mimo-v2.5-pro) + base_url (<https://token-plan-cn.xiaomimimo.com/v1>)
5. It creates an OpenAI client hitting `XIAOMI_API_KEY` from your `.hermes/.env`
6. If that key is invalid/expired → HTTP 401 from the Xiaomi API

## Why Main Chat Works But Title Gen Fails (or vice versa)

The key resolution paths differ slightly:

- **Main chat**: Creates an OpenAI client at agent init time with the API key from the credential pool/env
- **Title gen**: Creates a *separate* cached client via `resolve_provider_client()` in a background thread, resolving the API key fresh from `XIAOMI_API_KEY` env var or the credential pool

If the key was recently rotated, expired, or the credential pool had a stale entry, one path might use a cached valid client while the other resolves a fresh (now-invalid) key.

## Evidence From Your Logs

From `errors.log`, on 2026-05-29 both paths were failing:

```
10:13:25 API call failed ... provider=xiaomi ... summary=HTTP 401: Invalid API Key
10:13:55 API call failed ... provider=xiaomi ... summary=HTTP 401: Invalid API Key
10:14:13 API call failed ... provider=xiaomi ... summary=HTTP 401: Invalid API Key
```

These were main conversation loop calls, not just title gen. Your `XIAOMI_API_KEY` was invalid at that time. After you updated the key, everything recovered — the recent logs (June 14-21) show successful title_generation calls.

## If It's Happening Right Now

The 401 means your `XIAOMI_API_KEY` in `~/.hermes/.env` is invalid. Verify:

```bash
# Check if the key works directly
curl -s https://token-plan-cn.xiaomimimo.com/v1/models \
  -H "Authorization: Bearer *** | head -5
```

If it returns 401, regenerate the key at <https://platform.xiaomimimo.com> and update `~/.hermes/.env`.

## To Suppress the Warning (if key is fine and it's a transient blip)

You can configure title_generation to use a different provider:

```yaml
auxiliary:
  title_generation:
    provider: xiaomi
    model: mimo-v2.5
    timeout: 30
```

Or disable auto-titling entirely by setting `auxiliary.title_generation.provider: none` in config.yaml.
