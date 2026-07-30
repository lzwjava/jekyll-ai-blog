---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'torch.arange: 均匀间隔的一维张量'
translated: true
type: note
---

问题：`torch.arange` 的功能是什么？

回答：与 Python 的 `range` / NumPy 的 `arange` 相同——返回一个在 `[start, end)` 区间内均匀分布的一维张量。

```python
import torch

torch.arange(5)                  # tensor([0, 1, 2, 3, 4])
torch.arange(2, 10, 2)           # tensor([2, 4, 6, 8])   start, end, step
torch.arange(0, 1, 0.25)         # tensor([0.0000, 0.2500, 0.5000, 0.7500])

# dtype/device 会影响后续操作
torch.arange(5, dtype=torch.float32, device='cuda')
```

函数签名：`torch.arange(start=0, end, step=1, dtype=None, device=None)`。`end` 是开区间，与 `torch.linspace` 不同（后者默认包含端点）。

实际应用场景：构建 RoPE/位置编码的位置索引、因果掩码构造、KV 缓存的索引。

```python
# 经典用法：RoPE 的位置索引
seq_len = 8
pos = torch.arange(seq_len)  # tensor([0,1,...,7])

# 因果掩码
mask = torch.arange(seq_len)[None, :] <= torch.arange(seq_len)[:, None]
```

一个注意事项：使用浮点数 `step` 时，在接近 `end` 处可能会累积舍入误差，因此对于分数步长，`linspace` 通常比 `arange` 更安全。

参考文档：
- [torch.arange — PyTorch 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.arange.html)