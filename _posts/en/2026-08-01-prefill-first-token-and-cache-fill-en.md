---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Prefill: First Token and Cache Fill"
translated: false
type: note
---

Yes, you're basically right — but let me be precise, because "prefill" in this file refers to a **phase of request processing**, and filling the KV cache is only part of what it does.

## What prefill means here

In LLM serving, a request goes through two phases:

**1. Prefill** (`context.is_prefill` → `_prefill_forward`)
- Processes the **entire prompt in one shot** (all tokens in parallel)
- Computes K/V for every prompt token and **stores them into the KV cache** via `store_kvcache(k, v, k_cache, v_cache, context.slot_mapping)` — this is the "filling the cache" part you mentioned
- Also **runs attention over the full prompt** (`_flash_attention` with `causal=True`) to produce the **first output token**

**2. Decode** (`_decode_forward`)
- Generates one token at a time
- Only computes K/V for the *new* token, stores it in the cache
- Then reads **all previous K/V back out of the cache** (`_gather_kv_from_cache`) so the new token can attend to everything the prompt already said — *without recomputing* the prompt's K/V

## The key lines

```python
# forward():
if has_cache and context.slot_mapping is not None:
    store_kvcache(k, v, k_cache, v_cache, context.slot_mapping)  # ← fill cache

if context.is_prefill:
    return self._prefill_forward(...)   # prompt processed at once → 1st token
else:
    return self._decode_forward(...)    # 1 new token, attends to cached K/V
```

## So your intuition, corrected

- ✅ **Yes**: prefill writes the prompt's K/V into the paged KV cache (`store_kvcache`), so decode steps can reuse them later without recomputation.
- ⚠️ **But**: prefill is not *just* cache-filling. It's the phase that consumes the whole prompt and produces the first token. The cache-fill is a side effect that makes all subsequent (decode) steps cheap.

Interesting detail in this file: there's also **prefix caching** support — in `_prefill_forward`, when `block_tables` is set and the cache already has content (`_gather_kv_from_cache`), a new request can reuse cached K/V from a previously-seen prefix instead of recomputing it. In that case prefill only computes K/V for the *new* suffix tokens and attends over the gathered cached prefix.
