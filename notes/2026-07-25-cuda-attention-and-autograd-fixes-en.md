---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA, Attention, and Autograd Fixes
translated: false
type: note
---

Here's a breakdown of the bugs and obstacles I encountered, and how each was fixed:

---

## Obstacles & Fixes

### 1. `flash-attn` not installable (CUDA version mismatch)

**Obstacle:** Your system has CUDA 13.2, but PyTorch (2.10.0) was compiled with CUDA 12.8. Building `flash-attn` from source failed with:

```
RuntimeError: The detected CUDA version (13.2) mismatches the version that was used to compile PyTorch (12.8)
```

**Fix:** Replaced `flash_attn_varlen_func` and `flash_attn_with_kvcache` with PyTorch's native `torch.nn.functional.scaled_dot_product_attention` (SDPA), which internally uses FlashAttention when available. Also made `flash-attn` optional in `pyproject.toml`.

### 2. Triton segfault (CUDA version mismatch)

**Obstacle:** The `store_kvcache` kernel uses Triton 3.6.0, which also had CUDA compatibility issues with the mismatched driver/runtime, causing a hard segfault (core dump) with no Python traceback.

**Fix:** Rewrote `store_kvcache` using pure PyTorch indexing instead of Triton:

```python
# Before: triton kernel launching on CUDA
store_kvcache_kernel[(N,)](key, key.stride(0), value, value.stride(0), 
                           k_cache, v_cache, slot_mapping, D)

# After: pure PyTorch, works anywhere
k_cache_flat[slot_mapping[valid]] = key_flat[valid]
v_cache_flat[slot_mapping[valid]] = value_flat[valid]
```

### 3. `@torch.compile` segfault (in-place ops + inductor)

**Obstacle:** 4 files used `@torch.compile` with the `inductor` backend. The compiled RMSNorm contained in-place operations (`x.mul_()`, `x.add_()`) which triggered:

```
RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation
```

With `torch.inference_mode()` this caused a hard segfault instead of a proper error.

**Fix:** Removed all `@torch.compile` decorators from:
- `layernorm.py` (RMSNorm)
- `activation.py` (SiluAndMul)
- `sampler.py` (Sampler)
- `rotary_embedding.py` (RotaryEmbedding)

### 4. Autograd conflict in KV cache writes

**Obstacle:** `store_kvcache` used in-place assignment (`k_cache_flat[...] = key_flat[valid]`) where `key_flat[valid]` was part of the computation graph, causing:

```
RuntimeError: a leaf Variable that requires grad is being used in an in-place operation
```

**Fix:** Wrapped the cache writes in `torch.no_grad()`:

```python
with torch.no_grad():
    k_cache_flat[slot_mapping[valid]] = key_flat[valid]
    v_cache_flat[slot_mapping[valid]] = value_flat[valid]
```

### 5. Wrong decode attention mask (critical logic bug)

**Obstacle:** In the decode path, `is_causal=True` was used with `q_len=1` and `k_len=N` (N > 1). PyTorch's SDPA generates a causal mask where **query position 0 can only attend to key position 0**, not all N cached positions. This meant the model only ever saw the first cached token, producing gibberish.

```
q: (1 token at position 5)
k: (5 cached tokens at positions 0-4)

is_causal=True mask:  # WRONG
  query 0 -> key 0 only, keys 1-4 masked out

Expected mask:          # CORRECT
  query 0 -> keys 0-4 (all previous tokens)
```

**Fix:** Changed to `is_causal=False` with no attention mask, so the single query token attends to all cached key positions:

```python
# Before (broken):
o = F.scaled_dot_product_attention(q, k, v, is_causal=True)

# After (correct):
o = F.scaled_dot_product_attention(q, k, v, is_causal=False)
```

This is safe because in decode mode, there's only 1 query token and all cached KV positions are previous tokens.

---

## Verification

After all fixes, the model produces coherent output:

```
Input:  "introduce yourself"
Output: "Hello! I'm a language model trained on a diverse range of languages..."
```