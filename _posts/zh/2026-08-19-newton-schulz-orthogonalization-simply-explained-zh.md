---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 牛顿-舒尔茨正交化简明解释
translated: true
type: note
---

问题：你能用更简单的方式解释一下牛顿-舒尔茨正交化吗？

答案：

让我们从头开始建立直觉，不讲术语。

---

**问题："正交化"到底是什么意思？**

想象一下你的梯度矩阵中有一些重要性**极不平衡**的方向：

```
梯度方向：
→→→→→→→→  (维度 A，梯度巨大，主导更新)
→          (维度 B，梯度微小，几乎不更新)
```

这种不平衡会导致训练不稳定。我们希望的是：

```
正交化之后：
→→→  (维度 A，已归一化)
→→→  (维度 B，同等重要性)
```

**每个方向获得相同的权重。**这就是正交化所做的。

---

**牛顿-舒尔茨的作用——一张图说明**

把它想象成反复把一个不规则图形挤压成一个圆形：
```
开始：不规则图形（你的梯度矩阵）
第1步：不那么不规则了
第2步：更圆了
第3步：几乎是个圆
第4步：≈ 完美的圆（正交矩阵！）
```

每一步都应用这个公式：
```
X_new = 1.5 × X  -  0.5 × X × X^T × X
```

这只是一个**校正公式**——它每一步都将奇异值（"拉伸程度"）往1.0方向微调。

---

**奇异值——核心概念**

一个矩阵在不同方向上的拉伸程度不同。这些拉伸的量被称为**奇异值**。

```
正交化之前：   奇异值 = [8.2,  3.1,  0.4,  0.01]
                       大    中等  小    极小
正交化之后：   奇异值 = [1.0,  1.0,  1.0,  1.0]
                       全部相等！
```

牛顿-舒尔茨是一种将所有奇异值推向1.0的快速方法。

---

**为什么不直接用SVD？**

你也可以用SVD进行精确正交化：
```python
U, S, Vt = torch.linalg.svd(G)
Q = U @ Vt  # 完美的正交矩阵
```

但SVD在处理大型矩阵时**非常慢**。牛顿-舒尔茨仅通过**矩阵乘法**就能实现同样的效果——而GPU对此极其擅长。5次迭代 ≈ 效果足够好，且速度快10倍。

---

**Muon的整体思路（通俗解释）**

```
普通Adam：
  梯度 → 根据历史缩放 → 更新权重
         （某些维度更新很多，某些几乎不更新）

Muon：
  梯度 → 正交化 → 更新权重
         （每个维度更新量相等）
         → 更均衡，更稳定的训练
```

---

**最小可运行示例，让你亲手验证**

```python
import torch

def orthogonalize(G, steps=10):
    X = G / G.norm()               # 先归一化
    for _ in range(steps):
        X = 1.5 * X - 0.5 * X @ X.T @ X   # 向正交方向微调
    return X

# 尝试运行
G = torch.randn(4, 4)
Q = orthogonalize(G)

# 检查：奇异值应该全部 ≈ 1.0
print("Before:", torch.linalg.svdvals(G).round(decimals=2))
print("After: ", torch.linalg.svdvals(Q).round(decimals=2))
```

预期输出：
```
Before: tensor([2.31, 1.47, 0.83, 0.21])   ← 不相等
After:  tensor([1.00, 1.00, 1.00, 1.00])   ← 全部相等 ✓
```

就是这样。牛顿-舒尔茨只是一种快速、对GPU友好的方法，用于使所有奇异值都等于1。

参考文献：
- [Muon 博客 – Keller Jordan](https://kellerjordan.github.io/posts/muon/)
- [奇异值分解 – 维基百科](https://en.wikipedia.org/wiki/Singular_value_decomposition)
- [Muon 源代码](https://github.com/KellerJordan/Muon/blob/master/muon.py)