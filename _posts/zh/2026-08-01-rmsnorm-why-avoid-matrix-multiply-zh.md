---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'RMSNorm: 为何避免矩阵乘法'
translated: true
type: note
---

## 为什么不用 `@`（矩阵乘法）？

RMSNorm 的两个步骤既不是线性变换，也不涉及 `@` 执行的“求和收缩”：

**1. 归一化：每个 token 的缩放，而非每个 token 的矩阵乘法**

```python
var = x.pow(2).mean(dim=-1, keepdim=True)          # 形状 (N, 1)，N = token 数量
x.mul_(torch.rsqrt(var + self.eps))                # 每个 token 被其自身的标量缩放
```

归一化因子 `1/√(var+eps)` 是一个**作用于整行所有特征的单一标量**。`@` 执行的是**对收缩维度的求和**——这里完全没有求和。如果你强行用 `@`，就需要构建一个 `diag(scale)` 对角矩阵，形状为 `(N, N)`：

- 计算：`diag(s) @ x` 的时间复杂度是 O(N²)（N 为 token 数）；而逐元素乘法是 O(N)
- 内存：多出一个 O(N²) 的对角矩阵，语义上毫无意义

**2. 权重缩放：对角线性映射，而非完整矩阵**

```python
x = x.to(orig_dtype).mul_(self.weight)   # weight 形状 (hidden,)，按列广播
```

数学上，`x * weight` 等价于 `x @ diag(weight)`——一个**对角**矩阵乘积。使用 `@` 意味着要生成一个 `(hidden, hidden)` 的对角矩阵并执行 O(hidden²) 的矩阵乘法，而逐元素乘法只需 O(hidden)。

如果你想要真正的矩阵乘法，那应该用 `nn.Linear`（一个完全可学习的矩阵）。RMSNorm 的权重被刻意限制为“每维一个增益”，因此 Hadamard（逐元素）乘积才是其内在形式。

## 为什么用 `mul_`（原地操作）而不是 `mul`？

```python
x = x.float()                       # 新的 fp32 副本
...
x = x.to(orig_dtype).mul_(self.weight)
```

- **少一次分配**：`mul` 返回新张量，`mul_` 原地改写，不产生临时变量。在推理路径上，每个 token 每层都要经过这一步，每次避免的分配都意味着更少的内核启动和内存抖动。
- **安全性**：此时 `x` 已经是 `x.float()` / `x.to(orig_dtype)` 新创建的副本，没有外部引用，因此原地修改不会破坏调用方的原始张量。
- **数值精度**：统计量在 fp32 中计算，然后结果在权重缩放前转回原始 dtype。权重缩放是精度安全的（乘以常数因子），因此可以在原地完成。

## 总结

`@` 是求和收缩（矩阵乘法）；RMSNorm 是逐点缩放（按行的归一化因子，按列的权重）。使用 `@` 相当于乘以一个巨大的对角矩阵——这是 O(n²) 的浪费，而实际只需 O(n)。`mul_` 则原地执行逐点缩放，节省了内存和分配开销。