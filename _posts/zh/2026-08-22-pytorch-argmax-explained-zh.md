---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch argmax 详解
translated: true
type: note
---

**问题：** `torch.argmax` 在 PyTorch 中有什么作用？

**答案：**

`torch.argmax` 返回张量中**最大值所在的索引**——不是数值本身，而是其位置。

**函数签名：**

```python
torch.argmax(input, dim=None, keepdim=False)
```

**参数：**

- `input` — 输入张量
- `dim` — 沿该维度进行规约。若为 `None`，则在展平后的张量上操作
- `keepdim` — 是否保持规约后的维度

**示例：**

```python
import torch

x = torch.tensor([3, 1, 4, 1, 5, 9, 2, 6])
torch.argmax(x)  # → tensor(5)  (数值9的索引)
```

```python
# 沿指定维度操作
x = torch.tensor([[1, 3, 2],
                   [4, 0, 5]])

torch.argmax(x, dim=0)  # → tensor([1, 0, 1])  (每列最大值所在的行索引)
torch.argmax(x, dim=1)  # → tensor([1, 2])     (每行最大值所在的列索引)
```

**常见用例——分类任务：**

```python
logits = model(inputs)          # 形状: [batch, num_classes]
preds = torch.argmax(logits, dim=1)  # 每个样本的预测类别索引
```

它本质上是 NumPy 中 `np.argmax` 在 PyTorch 中的对应实现。

参考资料：

- [torch.argmax — PyTorch 官方文档](https://pytorch.org/docs/stable/generated/torch.argmax.html)