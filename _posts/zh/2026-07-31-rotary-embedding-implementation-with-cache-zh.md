---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 带缓存的旋转嵌入实现
translated: true
type: note
---

来自 `/Users/lzwjava/projects/nano-vllm/nanovllm/layers/rotary_embedding.py` 的完整文件：

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

**注意：** 在实际文件中，`persistent=False)` 后面**没有**尾随逗号——如上所示是干净的。

如果你问的是粘贴片段中的尾随逗号，那将是一个无害的语法错误（`后多余的 `,`）。但磁盘上的文件是正确的。

---

### 此 RoPE 实现的工作原理：

1. **`__init__`** —— 预先计算直到 `max_position_embeddings` 的完整余弦/正弦表：
   - `inv_freq` = `1 / (base^(2i/dim))`，其中 `i = 0, 2, 4, ...`（标准 RoPE 频率段）
   - `freqs` = 位置索引 `t` 与 `inv_freq` 的外积
   - `cos`, `sin` = `freqs` 的逐元素三角值
   - 存储为缓冲区 `cos_sin_cache`，形状为 `[max_pos, 1, rotary_dim*2]`（`unsqueeze_(1)` 增加一个头维度）

2. **`forward`** —— 根据给定的 `positions` 查找预计算的余弦/正弦，拆分为余弦/正弦两半，并对 query 和 key 应用旋转。

3. **`apply_rotary_emb`** —— 将 `x` 拆分为两半 `(x1, x2)` 并应用：
   ```
   y1 = x1·cos - x2·sin
   y2 = x2·cos + x1·sin
   ```
   这是每对维度的标准二维旋转。

4. **`get_rope`** —— 一个单例工厂，通过 `lru_cache` 缓存，因此每个配置只创建一个 `RotaryEmbedding` 实例。