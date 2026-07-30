---
audio: false
generated: true
image: false
lang: en
layout: post
title: RoPE Implementation Walkthrough
translated: false
type: note
---

Here's a detailed walkthrough of the RoPE (Rotary Position Embedding) implementation:

---

## `apply_rotary_emb` — The core rotation function

```python
def apply_rotary_emb(x, cos, sin):
    x1, x2 = torch.chunk(x.float(), 2, dim=-1)
    y1 = x1 * cos - x2 * sin
    y2 = x2 * cos + x1 * sin
    return torch.cat((y1, y2), dim=-1).to(x.dtype)
```

**What it does:** Applies a 2D rotation to each pair of dimensions in the input.

- Splits the last dimension into two halves: `x1` (even-indexed dims) and `x2` (odd-indexed dims)
- Applies the rotation matrix:
  ```
  [y1]   = [cos  -sin] [x1]
  [y2]     [sin   cos] [x2]
  ```
- Casts to float32 for precision, then back to the original dtype

This rotates each consecutive pair `(d, d+1)` by an angle determined by the position, giving the model a way to encode relative position information via dot products of rotated queries and keys.

---

## `RotaryEmbedding.__init__` — Precomputing the cache

```python
inv_freq = 1.0 / (base**(torch.arange(0, rotary_dim, 2, dtype=torch.float) / rotary_dim))
```

Computes the **inverse frequency** for each pair of dimensions. For `rotary_dim = 64`, this gives 32 frequency bands:

```
inv_freq[i] = 1.0 / base^(2i / rotary_dim)
```

These frequencies decrease geometrically — early pairs rotate fast (high frequency), later pairs rotate slow (low frequency).

```python
t = torch.arange(max_position_embeddings, dtype=torch.float)
freqs = torch.einsum("i,j -> ij", t, inv_freq)
```

Outer product of position indices × frequencies → shape `[max_pos, rotary_dim/2]`. This gives each position × frequency pair its rotation angle.

```python
cos = freqs.cos()
sin = freqs.sin()
cache = torch.cat((cos, sin), dim=-1).unsqueeze_(1)
```

Computes cos/sin and concatenates them: shape `[max_pos, 1, rotary_dim]`. The `unsqueeze_(1)` adds a dummy head dimension, making it broadcastable across heads.

```
self.register_buffer("cos_sin_cache", cache, persistent=False)
```

Registers as a non-persistent buffer (not saved in `state_dict`), since it can be recomputed from config.

---

## `RotaryEmbedding.forward` — Applying at given positions

```python
cos_sin = self.cos_sin_cache[positions]    # [batch, 1, rotary_dim]
cos, sin = cos_sin.chunk(2, dim=-1)        # [batch, 1, rotary_dim/2] each
query = apply_rotary_emb(query, cos, sin)
key = apply_rotary_emb(key, cos, sin)
```

- Indexes into the precomputed cache at the given positions
- Splits the cache back into cos/sin halves
- Rotates both query and key

---

## `get_rope` — Singleton factory

```python
@lru_cache(1)
def get_rope(head_size, rotary_dim, max_position, base):
    rotary_emb = RotaryEmbedding(head_size, rotary_dim, max_position, base)
    return rotary_emb
```

Cached factory so only **one** `RotaryEmbedding` instance is ever created per unique config. Since these params are typically constant across the whole model, this is effectively a singleton.

---

## Visual summary of data flow

```
positions: [batch]                 query/key: [batch, heads, seq_len, head_size]
    │                                      │
    ▼                                      │
cos_sin_cache[max_pos, 1, dim]             │
    │                                      │
    ▼                                      ▼
cos_sin = cache[positions]  ──chunk──► cos, sin
  [batch, 1, dim]              [batch, 1, dim/2] each
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
              query = rot(query, cos, sin)   key = rot(key, cos, sin)
```

The key insight: because rotation is applied to both Q and K with the **same** position-dependent angle, the dot product `Q·K` at positions `(i, j)` naturally encodes the **relative** position `(i - j)`, which is what gives RoPE its relative-positional behavior.
