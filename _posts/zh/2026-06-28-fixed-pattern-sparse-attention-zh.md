---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 固定模式稀疏注意力
translated: true
type: note
---

以下是论文中关于稀疏/高效注意力的相关工作条目。以下是背景介绍：

**Sparse Transformer (Child et al., 2019)** 是*固定模式*稀疏注意力的奠基性工作。核心问题：完整自注意力的计算复杂度为 O(n²)（n 为序列长度）——每个 token 都关注所有其他 token。对于长序列（展平为数千个 token 的图像、音频、长文档），这在计算和内存上都是不可行的。

关键洞察：不使用密集注意力，而是将**注意力模式分解**为一种固定的、与内容无关的稀疏结构。每个 token 仅关注 O(√n) 个位置，总复杂度为 O(n√n)。

两种分解的注意力头：
- **Strided attention** —— 每个位置关注前 `l` 个位置（局部窗口）以及每隔 `l` 个位置（步长/空洞）。适用于具有周期性结构的数据（如图像），其中 `l ≈ √n` 与行宽相匹配。
- **Fixed attention** —— 特定的列/位置充当路由 token，全局性地聚合和广播信息。更适合没有明显周期性结构的数据（如文本）。

步长模式的简要代码示意：

```python
import torch

def strided_mask(n, l):
    # l ~ sqrt(n); 每个 token i 关注局部窗口 + 步长位置
    idx = torch.arange(n)
    i, j = idx[:, None], idx[None, :]
    local = (i - j >= 0) & (i - j < l)        # 前 l 个位置
    strided = (i >= j) & ((i - j) % l == 0)   # 每隔 l 个位置往回
    return local | strided                     # 因果块稀疏模式
```

“与内容无关”是关键词：稀疏模式在见到数据之前就已固定，完全由位置决定。这正是它区别于后来的*基于内容*的方法（Reformer 的 LSH 分桶、Routing Transformer 的聚类）之处，后者的 token 关注哪些 token 取决于实际的 key/query 值。你的论文很可能是在将自己的方法与这种固定模式基线进行对比——`BlockSparse` 系列正是从这里开始的。

值得了解的是，该论文还贡献了与稀疏性正交的工程部分：通过重计算注意力矩阵来节省内存（将梯度检查点应用于注意力），以及融合的块稀疏 GPU 内核。这些使得该方法不仅具有理论意义，而且实际可行。

需要我继续追溯后续发展——Longformer/BigBird 如何推广了固定模式，或者基于内容的分支是如何分化的吗？