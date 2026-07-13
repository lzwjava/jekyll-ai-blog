---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ASStaticCache: CUDA Graph Fix"
translated: false
type: note
---

Good question. The author didn't just arbitrarily extend `StaticCache` — the customizations are **all driven by CUDA Graph constraints**. Here's what's special about `ASStaticCache` vs HuggingFace's stock `StaticCache`:

## The core problem CUDA Graphs impose

A captured CUDA Graph is **frozen** — every tensor shape, every kernel launch is baked in. You cannot reallocate, reshape, or change tensor sizes between captures. But KV cache in autoregressive decoding **grows by 1 token per step**. HuggingFace's `StaticCache` expects to be re-allocated or grown — that breaks inside a graph.

`ASStaticCache` solves this with 3 specific tricks:

---

### 1. `update()` slices to `:done` — the "valid window" hack

```python
def update(self, key_states, value_states, layer_idx, cache_kwargs=None):
    done = cache_kwargs["cache_position"].shape[0]
    k_out, v_out = super().update(
        key_states[:, :, :done, :], value_states[:, :, :done, :], ...
    )
```

Inside a CUDA Graph replay, `key_states` and `value_states` are **pre-allocated tensors of shape `[1, n_heads, max_seq, head_dim]`** — the graph captured the full-size write operation. But only `done` tokens' worth of actual KV data is valid this step; the rest is garbage/padding from the pre-allocated buffer.

By slicing `:done`, it ensures `StaticCache.update()` only writes the **real** KV pairs into the cache, and doesn't contaminate past positions with padding garbage.

---

### 2. `reset()` fills `cumulative_length` to `max_cache_len` — faking position

```python
def reset(self, device="cuda:0"):
    for layer in self.layers:
        layer.reset()
        if hasattr(layer, 'cumulative_length'):
            layer.cumulative_length.fill_(self._max_cache_len)
    self._cache_position.fill_(self._max_cache_len)
```

After reset, both `cumulative_length` and `cache_position` say **"I already have `max_cache_len` tokens cached"**. Why? Because the pre-allocated KV cache buffer is already full-sized. RoPE position calculations inside Qwen3VL decoder layers read `cumulative_length` to determine positional embeddings. If it was 0 after reset, the RoPE positions would be wrong during the very first decode step. By setting it to `max_cache_len`, the model thinks it's always doing a "mid-sequence" decode, which matches the static buffer's geometry.

---

### 3. `cache_position` bridges two position-tracking systems

```python
@property
def cache_position(self):
    if self._cache_position is None and len(self.layers) > 0:
        first_layer = self.layers[0]
        if hasattr(first_layer, 'cumulative_length'):
            self._cache_position = first_layer.cumulative_length
    return self._cache_position
```

HuggingFace's `StaticCache` uses `cache_position` to know where in the cache to write. Qwen3VL's internal decoder layers track position via `cumulative_length` on each layer. After graph replay, these two can drift out of sync. The property ties them together — `cache_position` always reflects whatever the first layer's `cumulative_length` says.

---

## Summary: what makes `ASStaticCache` special

| Feature | Stock `StaticCache` | `ASStaticCache` |
| --- | --- | --- |
| **Allocation** | Grows dynamically, re-allocatable | Fixed once at `max_cache_len` — graph-compatible |
| **Update** | Writes all incoming states | Slices to `:done` — prevents padding contamination |
| **Reset** | Sets length to 0 | Sets `cumulative_length` to `max_cache_len` — fakes full cache |
| **Position tracking** | Single `cache_position` | Bridges `cache_position` ↔ per-layer `cumulative_length` |

It's essentially a **CUDA Graph compatibility layer** for HuggingFace's StaticCache. The author couldn't use the stock cache inside a captured graph because it doesn't account for the "static buffer, dynamic valid-content" pattern that CUDA Graphs force you into. Each of the 3 overrides directly addresses a specific graph-incompatible behavior of the parent class.
