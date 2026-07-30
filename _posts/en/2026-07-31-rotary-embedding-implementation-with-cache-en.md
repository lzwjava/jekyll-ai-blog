---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rotary Embedding Implementation with Cache
translated: false
type: note
---

Here's the full file at `/Users/lzwjava/projects/nano-vllm/nanovllm/layers/rotary_embedding.py`:

```python
from functools import lru_cache
import torch
from torch import nn


def apply_rotary_emb(
    x: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor,
) -> torch.Tensor:
    x1, x2 = torch.chunk(x.float(), 2, dim=-1)
    y1 = x1 * cos - x2 * sin
    y2 = x2 * cos + x1 * sin
    return torch.cat((y1, y2), dim=-1).to(x.dtype)


class RotaryEmbedding(nn.Module):

    def __init__(
        self,
        head_size: int,
        rotary_dim: int,
        max_position_embeddings: int,
        base: float,
    ) -> None:
        super().__init__()
        self.head_size = head_size
        assert rotary_dim == head_size
        inv_freq = 1.0 / (base**(torch.arange(0, rotary_dim, 2, dtype=torch.float) / rotary_dim))
        t = torch.arange(max_position_embeddings, dtype=torch.float)
        freqs = torch.einsum("i,j -> ij", t, inv_freq)
        cos = freqs.cos()
        sin = freqs.sin()
        cache = torch.cat((cos, sin), dim=-1).unsqueeze_(1)
        self.register_buffer("cos_sin_cache", cache, persistent=False)

    def forward(
        self,
        positions: torch.Tensor,
        query: torch.Tensor,
        key: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        cos_sin = self.cos_sin_cache[positions]
        cos, sin = cos_sin.chunk(2, dim=-1)
        query = apply_rotary_emb(query, cos, sin)
        key = apply_rotary_emb(key, cos, sin)
        return query, key


@lru_cache(1)
def get_rope(
    head_size: int,
    rotary_dim: int,
    max_position: int,
    base: float,
):
    rotary_emb = RotaryEmbedding(head_size, rotary_dim, max_position, base)
    return rotary_emb
```

**Note:** In the actual file, there is **no trailing comma** after `persistent=False)` — it's clean as shown above.

If you were asking about the trailing comma in your pasted snippet, that would be a harmless syntax error (a stray `,` after `)`). But the file on disk is correct.

---

### How this RoPE implementation works

1. **`__init__`** — Precomputes the full cos/sin table up to `max_position_embeddings`:
   - `inv_freq` = `1 / (base^(2i/dim))` for `i = 0, 2, 4, ...` (standard RoPE frequency bands)
   - `freqs` = outer product of position indices `t` × `inv_freq`
   - `cos`, `sin` = element-wise trig of `freqs`
   - Stored as a buffer `cos_sin_cache` of shape `[max_pos, 1, rotary_dim*2]` (the `unsqueeze_(1)` adds a head dimension)

2. **`forward`** — Looks up precomputed cos/sin for given `positions`, splits into cos/sin halves, and applies the rotation to both query and key.

3. **`apply_rotary_emb`** — Splits `x` into two halves `(x1, x2)` and applies:

   ```
   y1 = x1·cos - x2·sin
   y2 = x2·cos + x1·sin
   ```

   This is the standard 2D rotation per pair of dimensions.

4. **`get_rope`** — A singleton factory cached with `lru_cache` so you only create one RotaryEmbedding per config.
