---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoChat KV Cache Internals
translated: false
type: note
---

Now I have the full picture. Here's how KV cache works in nanochat:

## Where it lives

- **`KVCache` class** — `nanochat/engine.py:82` — the state container
- **Consumed in attention** — `nanochat/gpt.py:108-123` (`CausalSelfAttention.forward`) and `gpt.py:459+` (position offset, smear)
- **Kernel glue** — `nanochat/flash_attention.py:200` (`flash_attn_with_kvcache` with FA3/FA2/SDPA backends)

## Layout & allocation

The cache is pre-allocated up front in FA3's native `(B, T, H, D)` layout (no transposes):

```python
self.k_cache = torch.zeros(num_layers, batch_size, seq_len, num_heads, head_dim, device=device, dtype=dtype)
self.v_cache = torch.zeros(num_layers, batch_size, seq_len, num_heads, head_dim, ...)
```

Key details:

- **One tensor per layer slice**: `get_layer_cache(layer_idx)` returns `self.k_cache[layer_idx]` views.
- **KV heads only** (`n_kv_head`, default 6): this is GQA-ready — even though `n_head == n_kv_head` in the default config, the cache is shaped by `n_kv_head`, and FA3/`enable_gqa` replicates KV heads internally for the query heads.
- **Compute dtype** (bf16), matching activation dtype so in-place cache writes by the kernel are dtype-correct.
- **Position is a per-batch `int32` tensor**: `cache_seqlens` (B,), not a scalar — FA3 wants this shape.

## Two-phase engine flow (`Engine.generate`, engine.py:156)

1. **Prefill, batch=1**: allocate a small cache with `seq_len=len(tokens)`, run the whole prompt through `model.forward(ids, kv_cache=kv_cache_prefill)` — one pass, all layers write KV, logits from the last position.
2. **Clone to decode cache**: `kv_cache_decode.prefill(kv_cache_prefill)` copies the KV slices plus the smear state into a `batch_size=num_samples` cache sized `len(tokens) + max_tokens`. The batch-1 cache is freed. (This lets you do one prefill and then generate many samples in parallel off the same prefix.)
3. **Decode loop**: each iteration feeds only the newly sampled token(s) `(B, 1)` through the model with the decode cache; attention sees the full cached prefix, so per-token cost is O(1) new work + O(context) attention reads, not O(T²).

## Per-forward mechanics (the interesting parts)

**Rotary offset** (`gpt.py:466-468`): the cache knows its absolute position via `kv_cache.get_pos()`, and the cos/sin tables are sliced `self.cos[:, T0:T0+T]`. So a decode step of 1 token at position 500 gets the rotary embedding for absolute position 500.

**Rotate-then-cache, don't cache-then-rotate**: in `CausalSelfAttention.forward`, the new `k` (and `q`) get `apply_rotary_emb` *before* the kernel call, using those absolute positions. Then the already-rotated, QK-normed, scaled `k` is handed to the kernel as `k=k`:

```python
q, k = apply_rotary_emb(q, cos, sin), apply_rotary_emb(k, cos, sin)
q, k = norm(q), norm(k)
...
y = flash_attn.flash_attn_with_kvcache(q, k_cache, v_cache, k=k, v=v,
        cache_seqlens=kv_cache.cache_seqlens, causal=True, window_size=window_size)
```

This is correct because rotation/norm happen once at write time with absolute position — at read time the cached keys are already in the right form. (FA3 also has an internal `rotary_cos/rotary_sin` path; this code does it manually so the same code path works on FA2/SDPA fallbacks.)

**Single kernel does write + attention**: `flash_attn_with_kvcache` inserts `k, v` into the cache in-place at position `cache_seqlens`, then computes attention of `q` against the cache up to `cache_seqlens + T`. Causal + sliding-window masking comes from `window_size` (e.g. `(768, 0)` for short layers, `(-1, 0)`/`(2048, 0)` for long).

**Position advance is manual, after the last layer only** (`gpt.py:122-123`):

```python
if self.layer_idx == kv_cache.n_layers - 1:
    kv_cache.advance(T)
```

All layers must see the *same* `cache_seqlens` during one forward (each layer writes at the same slot), so the pointer is bumped once per forward, not per layer. The tests (`test_attention_fallback.py:312-330`) do the same explicit `advance`, confirming the kernels here don't update `cache_seqlens` in place.

## Extra state cached beyond K/V

- **`prev_embedding`** (engine.py:104): the previous token's normalized embedding, needed for the "smear" trick (cheap bigram info). On decode with `T == 1`, the model reads it, mixes `x + gate * prev` (`gpt.py:483-492`), then stores the new token's embedding. `prefill()` also copies/expands this for the multi-sample cache.
- **Value embeddings (ResFormer)** are *not* cached — they're re-looked-up per step via `self.value_embeds[str(i)](idx)`, which is a cheap embedding gather.

## Cost accounting

- `kv_bytes_per_token()` (gpt.py:374): `n_layer × 2 × n_kv_head × head_dim × 2 bytes` — storage per token.
- `kv_read_bytes(context_len)` (gpt.py:380): per decode step, and it respects sliding windows — short-window layers only read `min(context, window)` of cache, which is the whole point of the SSSL pattern: long layers do full reads, short layers read only the last quarter.

## Fallbacks

The SDPA fallback (`flash_attention.py:235+`) replicates the kernel behavior: inserts `k, v` in-place at `pos`, slices the cache to `end_pos`, and builds an explicit bool mask for sliding window / chunk inference (assumes uniform position: `pos = cache_seqlens[0].item()`).

One thing worth noting: `GPT.generate()` (`gpt.py:518`) is the naive no-cache path — it re-runs the full forward over the growing sequence every step — and the engine's `__main__` test asserts it produces identical tokens to the cached path, so the cache is validated against ground truth.
