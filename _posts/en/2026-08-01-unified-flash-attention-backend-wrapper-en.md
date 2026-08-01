---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unified Flash Attention Backend Wrapper
translated: false
type: note
---

`nanochat/flash_attention.py` is a **unified wrapper around three attention backends** for this GPT-style training/inference codebase. Its purpose: expose a single API that matches FlashAttention-3's interface exactly, and automatically pick the best available kernel.

## What it does

**Backend auto-detection (at import time):**
1. **FA3** (`_load_flash_attention_3`) — tries to load a kernel package. On Hopper (sm90, `major == 9`) it prefers the `varunneal/flash-attention-3` HF kernel; on other archs it tries `kernels-community/flash-attn3`. Returns `None` on any failure (no CUDA, import error, etc.).
2. **FA2** (`_load_flash_attention_2`) — imports the `flash-attn` pip package. Works on both NVIDIA CUDA and AMD ROCm.
3. **SDPA fallback** — plain PyTorch `scaled_dot_product_attention`, works everywhere.

**Selection logic** (`_resolve_impl`):
- Env var `NANOCHAT_FORCE_SDPA=1` forces the fallback.
- A test override `_override_impl` lets you force `'fa3'`/`'fa2'`/`'sdpa'` (asserts the backend actually exists).
- Auto: FA3 wins only if compute dtype is bf16 on Hopper, else FA2, else SDPA.
- Prints which backend is active at import: `✓ Using Flash Attention 3 (Hopper GPU)` etc.

**Public API** (exported as `flash_attn`, a `SimpleNamespace`):

- **`flash_attn_func(q, k, v, causal, window_size)`** — training path, no KV cache. For SDPA it transposes `(B,T,H,D)` → `(B,H,T,D)` and delegates to `_sdpa_attention`.
- **`flash_attn_with_kvcache(q, k_cache, v_cache, k, v, cache_seqlens, causal, window_size)`** — inference path with a preallocated cache. FA3/FA2 write `k, v` into the cache in-place; the SDPA fallback replicates that manually (`k_cache[:, pos:pos+T_new] = k`), then slices the cache up to `end_pos` and attends.

**`_sdpa_attention`** is the interesting piece — it emulates FA semantics that SDPA doesn't do natively:
- Full-context causal when window covers everything and `Tq == Tk`.
- Single-token generation: slices the KV window tail instead of building a mask.
- Otherwise builds an explicit bool mask for **chunked inference** (`Tq != Tk`, where `is_causal` wouldn't align with the cache position) combined with a left sliding-window constraint `row_idx - col_idx <= window`.

**`_fa2_window_size`** — normalizes FA3's `(-1, -1)` convention to what FA2 expects.

## Where it's used
`nanochat/gpt.py` imports `flash_attn` and calls `flash_attn.flash_attn_func(...)` (line 110, training) or `flash_attn.flash_attn_with_kvcache(...)` (line 114, generation), so the rest of the model code never needs to know which backend is running.

## Possible issues worth noting
- `_load_flash_attention_2` imports `flash_attn_varlen_func` but never uses it (dead import).
- The SDPA kvcache path assumes uniform `cache_seqlens` across the batch (`cache_seqlens[0].item()`), which would be wrong for batched decoding with different sequence lengths.
- The FA3 Hopper branch only activates for bf16 — fp16 Hopper users silently fall to FA2/SDPA even though FA3 supports it.
