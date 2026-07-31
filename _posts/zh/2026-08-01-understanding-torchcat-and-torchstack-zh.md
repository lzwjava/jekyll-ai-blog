---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解 torch.cat 和 torch.stack
translated: true
type: note
---

问题：`torch.cat` 是做什么的？

答案：将一个张量序列沿现有维度进行拼接。不会创建新维度（与 `torch.stack` 不同）。所有张量除了拼接维度外，其他维度上的形状必须匹配。

```python
import torch

a = torch.randn(2, 3)
b = torch.randn(2, 3)

torch.cat([a, b], dim=0).shape  # torch.Size([4, 3])  -> 堆叠行
torch.cat([a, b], dim=1).shape  # torch.Size([2, 6])  -> 堆叠列
```

实际中你会遇到的常见用途：

```python
# KV cache 追加（自回归解码）
k_cache = torch.cat([k_cache, k_new], dim=seq_dim)

# 沿 batch 维度拼接以实现多 GPU 聚合
gathered = torch.cat(tensor_list, dim=0)

# 跳跃连接（U-Net 等）—— 按通道拼接，而非相加
x = torch.cat([up_features, skip_features], dim=1)
```

注意事项：`cat` 要求现有维度匹配（例如，将两个 `(2,3)` 在 dim 0 上拼接 → `(4,3)`）。`stack` 要求 *所有* 维度匹配，并新增一个维度（`(2,3)` + `(2,3)` 在 dim 0 上 → `(2,2,3)`）。如果你在构建 KV cache 或进行跳跃连接，使用 `cat`；如果你将独立的相同形状张量批处理成一个新的前导维度，使用 `stack`。

参考资料：

- [torch.cat — PyTorch 文档](https://pytorch.org/docs/stable/generated/torch.cat.html)
- [torch.stack — PyTorch 文档](https://pytorch.org/docs/stable/generated/torch.stack.html)
