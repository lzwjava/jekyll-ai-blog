---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch unsqueeze 详解
translated: true
type: note
---

问题：`unsqueeze` 在 PyTorch 中有什么作用？

答案：在指定位置插入一个大小为 1 的维度。它是 `squeeze` 的逆操作。不会复制数据，仅改变视图（步幅的元数据变化）。

```python
import torch

x = torch.arange(6).reshape(2, 3)  # 形状 [2, 3]

x.unsqueeze(0).shape   # [1, 2, 3]  -> 在前面插入
x.unsqueeze(1).shape   # [2, 1, 3]  -> 在中间插入
x.unsqueeze(-1).shape  # [2, 3, 1]  -> 在末尾插入
x.unsqueeze(2).shape   # [2, 3, 1]  -> 此处等同于 -1
```

索引语义：对于维度为 `n` 的张量，`dim` 的有效范围是 `[-(n+1), n]`。新维度会在输出形状中该索引位置*之前*插入。

常见用途——为单个样本添加批次维度：

```python
img = torch.randn(3, 224, 224)      # C, H, W
batch = img.unsqueeze(0)            # [1, 3, 224, 224]
```

或者广播对齐，例如为每行添加偏置：

```python
a = torch.randn(4, 5)
b = torch.randn(4)
c = a + b.unsqueeze(1)  # b: [4] -> [4,1]，与 [4,5] 进行广播
```

这是一个视图操作 —— `x.unsqueeze(0).data_ptr() == x.data_ptr()` 结果为 `True`。由于在自动求导图中仅相当于一次形状重塑，梯度可以正常传播。

参考文档：

- [torch.unsqueeze 官方文档](https://docs.pytorch.org/docs/stable/generated/torch.unsqueeze.html)
