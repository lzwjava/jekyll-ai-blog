---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sliding Window Attention Architecture
translated: false
type: note
---

Sliding-window attention in this codebase is a three-layer story: a **pattern string → per-layer window sizes** in `gpt.py`, then **actual enforcement inside the attention kernel** via `flash_attention.py`.

## 1. Where windows are assigned (gpt.py)

The `Config` has `window_pattern: str = "SSSL"` (gpt.py:39), where `L` = full context, `S` = quarter context. `_compute_window_sizes` (gpt.py:287) turns that into one `(left, right)` tuple per layer:

```python
long_window  = config.sequence_len                          # L: full 2048
short_window = -(-long_window // 4 // 128) * 128            # S: ~quarter, rounded UP to 128 (FA3 tile size)
char_to_window = {"L": (long_window, 0), "S": (short_window, 0)}
# tile pattern across layers: "SSSL" -> S,S,S,L, S,S,S,L, ...
window_sizes[-1] = (long_window, 0)   # final layer ALWAYS full context
```

So the pattern is tiled over `n_layer` layers, and each `Block` receives `window_sizes[i]` which it forwards into `flash_attn.flash_attn_func(...)` / `flash_attn_with_kvcache(...)` (gpt.py:110, 119).

**Window semantics**: `(left, right)` is a *distance-based band*, not "the last N positions". Each query token attends to keys whose distance behind it is ≤ `left` — plus itself. `right = 0` plus `causal=True` means nothing to the future; `left = -1` would mean unlimited. Here `left` is always the concrete window (or full `sequence_len`), never `-1`.

## 2. `flash_attention.py` — the dispatch layer

The file doesn't implement sliding window itself; it's a **unified wrapper** that forwards the `window_size` tuple to whichever backend is active, with three cases:

### FA3 (Hopper) — pass-through
```python
return _fa3.flash_attn_func(q, k, v, causal=causal, window_size=window_size)
```
The FA3 CUDA kernel gets `(left, 0)` and does banded masking natively *inside* the kernel — each query block only loads key/value blocks within the window, which is where the FLOP/memory savings come from.

### FA2 — near pass-through
```python
return _fa2.flash_attn_func(q, k, v, dropout_p=0.0, causal=causal, window_size=_fa2_window_size(window_size))
```
FA2's kernel supports the same `(left, right)` banded attention natively. `_fa2_window_size` maps an unlimited left to FA2's `(-1, -1)` sentinel (in this model right is always 0, so it mostly passes through untouched).

### SDPA fallback — manual emulation (`_sdpa_attention`, the real meat)
PyTorch's `scaled_dot_product_attention` has no banded-window concept, so it's emulated three ways depending on the case:

**a) Full context, equal lengths** (`window < 0 or window >= Tq`, and `Tq == Tk`):
```python
return F.scaled_dot_product_attention(q, k, v, is_causal=True, ...)
```
The window covers everything anyway, so plain causal SDPA is used (fast path).

**b) Single-token decode** (`Tq == 1`) — the interesting trick:
```python
start = max(0, Tk - (window + 1))
k = k[:, :, start:, :]   # keep only the last window+1 keys
v = v[:, :, start:, :]
return F.scaled_dot_product_attention(q, k, v, is_causal=False, ...)
```
A query attending to a `window`-wide band only needs the **tail** of the KV cache, so it literally slices `k/v` down to the last `window + 1` keys. No mask needed at all — mathematically identical to banded attention because the query is the last position.

**c) Chunked inference / prefill** (`Tq != Tk`, both > 1): here the query is a chunk positioned *inside* the sequence, so the relevant keys are the tail of the cache *plus* earlier tokens within the chunk. It builds an explicit boolean mask:
```python
row_idx = (Tk - Tq) + torch.arange(Tq)          # absolute positions of query rows
col_idx = torch.arange(Tk)                       # absolute positions of key columns
mask = col_idx <= row_idx                        # causal: key position <= query position
if window >= 0 and window < Tk:
    mask = mask & ((row_idx - col_idx) <= window)  # sliding: distance back <= window
return F.scaled_dot_product_attention(q, k, v, attn_mask=mask, ...)
```
The `row_idx` offset `(Tk - Tq)` maps query rows to their true cache positions so causality and the distance band are computed in absolute positions, not relative offsets.

## Key observations

- **Savings come from the kernels, not the mask.** With FA3/FA2, the band is a *kernel-level* optimization: key blocks outside the window are never loaded, so attention FLOPs per layer scale with the window, not full context. With SDPA fallback it's just a mask/slice — correct but no speed win.
- **The KV cache still grows unboundedly.** The `KVCache` in engine.py just keeps appending (`cache_seqlens += num_tokens`); nothing is evicted. Sliding window here only limits *attention*, it doesn't bound cache memory. (The comment in gpt.py:107 — `(N, 0)` for sliding window — confirms only the left band is used.)
- **Effective context per position** is `min(position, window+1)` tokens — layers with `S` get roughly quarter-context local attention, alternating with full-context `L` layers, and the last layer always sees everything, giving the cheap "locality + global recap" mix typical of sliding-window LLMs (e.g., Longformer/BigBird-style hybrids).
- The SDPA window check `window >= Tq` treats "window at least as big as the query run" as full context — an important edge case because during decode `Tq` is small (often 1) and even a "short" window of 512 covers everything the query has seen so far early in generation.