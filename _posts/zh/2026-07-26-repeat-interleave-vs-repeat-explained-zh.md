---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重复交错与重复解释
translated: true
type: note
---

问题：作为通用张量操作（非GQA专用），`torch.repeat_interleave` 的作用是什么？

答案：

它在移动到下一个元素之前，*原地*重复维度上的每个元素 — 与 `repeat` 不同，后者会平铺整个序列。

```python
import torch

x = torch.tensor([1, 2, 3])

x.repeat_interleave(2)
# tensor([1, 1, 2, 2, 3, 3])   <- 每个元素重复2次，然后下一个元素

x.repeat(2)
# tensor([1, 2, 3, 1, 2, 3])   <- 整个序列平铺2次
```

**带 `dim` 参数** — 沿着该维度重复切片，保持其他维度不变：

```python
x = torch.tensor([[1, 2],
                   [3, 4]])

x.repeat_interleave(2, dim=0)
# tensor([[1, 2],
#         [1, 2],
#         [3, 4],
#         [3, 4]])   <- 每个行在下一行之前复制

x.repeat_interleave(2, dim=1)
# tensor([[1, 1, 2, 2],
#         [3, 3, 4, 4]])   <- 每个列在下一列之前复制
```

**每个元素的重复次数**（不仅仅是标量）— 你可以传入一个张量，指定每个元素重复多少次：

```python
x = torch.tensor([1, 2, 3])
x.repeat_interleave(torch.tensor([1, 2, 3]))
# tensor([1, 2, 2, 3, 3, 3])
```

这就是为什么它是GQA头扩展的正确工具 — 你希望KV头0 → 0,0,0,0，KV头1 → 1,1,1,1（块相邻重复），而不是 `repeat` 会给出的重新平铺的 `0,1,2,3,0,1,2,3` 模式。