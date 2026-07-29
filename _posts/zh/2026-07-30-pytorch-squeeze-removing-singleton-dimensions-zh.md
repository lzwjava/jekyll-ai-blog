---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'PyTorch squeeze: 移除单维度'
translated: true
type: note
---

问题：`squeeze` 在 PyTorch 中有什么作用？

回答：移除大小为 1 的维度。是 `unsqueeze` 的逆操作。也是视图操作，不复制数据。

```python
import torch

x = torch.randn(1, 3, 1, 4)  # 形状 [1, 3, 1, 4]

x.squeeze().shape       # [3, 4]     -> 移除所有大小为 1 的维度
x.squeeze(0).shape      # [3, 1, 4]  -> 仅移除维度 0（如果它大小为 1）
x.squeeze(2).shape      # [1, 3, 4]  -> 仅移除维度 2
x.squeeze(1).shape      # [1, 3, 1, 4] -> 无操作，维度 1 大小为 3，不是 1
```

注意：在 batch size 为 1 时调用不带参数的 `squeeze()` 可能会静默地移除 batch 维度。

```python
batch = torch.randn(1, 5)  # 1 个样本，5 个特征
batch.squeeze().shape      # [5] -> batch 维度消失，现在看起来像是非批量的
```

这会让在损失函数和循环中假设固定张量秩（rank）的人踩坑——例如，当 batch size 为 1 时，在 `squeeze()` 之后遍历 "batch" 会得到一个标量/一维张量，而不是一个单行列表。在生产代码中最好使用显式的 `squeeze(dim)` 形式，或者仅当你确定要移除的维度就是该维度时才使用 `squeeze(0)`。

常见搭配：用 `unsqueeze` 添加一个维度以进行广播，然后在操作后使用 `squeeze` 移除它。

```python
x = torch.randn(4, 5)
w = torch.randn(5)
out = (x * w.unsqueeze(0)).sum(dim=1, keepdim=True)  # [4,1]
out = out.squeeze(1)  # [4]
```

参考：
- [torch.squeeze docs](https://docs.pytorch.org/docs/stable/generated/torch.squeeze.html)