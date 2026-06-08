---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch矩阵乘法的形状广播
translated: true
type: note
---

问题：PyTorch 的 `@` 运算符（矩阵乘法）如何智能地确定输出形状，特别是在批量注意力计算中，例如 `(B, nh, T, T) @ (B, nh, T, hs) → (B, nh, T, hs)`？

答案：

PyTorch 的 `@` 运算符（矩阵乘法）使用**广播规则 + 维度收缩逻辑**，能够自动处理批量运算。以下是实际发生的过程：

## matmul 广播规则

```python
# 规则：A @ B 将 A 的最后一个维度与 B 的倒数第二个维度进行收缩
# 所有前置维度像 NumPy 一样进行广播

# 以你的注意力计算为例：
# att:  (B, nh, T, T)   <- 最后一个维度是 T（待收缩的维度）
# v:    (B, nh, T, hs)  <- 倒数第二个维度是 T（待收缩的维度）
# 结果： (B, nh, T, hs)

# 实际发生的过程：
# 1. 将 (B, nh) 视为进行广播的批量维度
# 2. 对每个 (b, h) 对，执行：(T, T) @ (T, hs) = (T, hs)
# 3. 将结果堆叠回：(B, nh, T, hs)
```

**收缩维度** (T) 是隐式的：
- `att` 舍弃其最后一个维度 T
- `v` 舍弃其倒数第二个维度 T
- 这两个 T 必须匹配（它们确实匹配），并且会被**收缩掉**

剩余的维度**从左到右堆叠**：
- 来自 `att`：(B, nh, T) —— "行"维度
- 来自 `v`：(hs) —— "列"维度
- 结果：(B, nh, T, hs)

## 为什么这样可行（数学原理）

标准矩阵乘法：`A[m, n] @ B[n, k] = C[m, k]`

在你的例子中：
- `att` 的形状为 `(B, nh, T, T)` —— 将其视为 **一批 (B×nh) 个矩阵**，每个为 (T, T)
- `v` 的形状为 `(B, nh, T, hs)` —— 将其视为 **一批 (B×nh) 个矩阵**，每个为 (T, hs)

PyTorch 会展平批量维度，执行 `(B*nh, T, T) @ (B*nh, T, hs) = (B*nh, T, hs)`，然后重新调整形状回来。

## 底层实现

```python
import torch

# 最小示例
B, nh, T, hs = 2, 4, 3, 8

att = torch.randn(B, nh, T, T)  # (2, 4, 3, 3)
v = torch.randn(B, nh, T, hs)    # (2, 4, 3, 8)

# @ 的内部操作（简化版）：
# 1. 重塑为 (B*nh, T, T) 和 (B*nh, T, hs)
# 2. 使用批量 GEMM（通用矩阵乘法）
# 3. 重塑回 (B, nh, T, hs)

y = att @ v  # (2, 4, 3, 8) ✓

# 验证收缩结果：
print(y.shape)  # torch.Size([2, 4, 3, 8])

# 手动验证（较慢，但展示逻辑）：
y_manual = torch.zeros(B, nh, T, hs)
for b in range(B):
    for h in range(nh):
        y_manual[b, h] = att[b, h] @ v[b, h]  # (T, T) @ (T, hs) = (T, hs)

assert torch.allclose(y, y_manual)
```

## 为什么说它"智能"

真正的巧妙之处在于**你无需手动重塑**。PyTorch 的 `matmul`：
1. 推断批量维度（除最后两个维度外的所有前置维度）
2. 验证收缩维度是否匹配（T == T）
3. 调用优化的 GEMM 内核进行批量运算
4. 返回结果，无需你编写循环

与显式循环对比（底层实际发生的过程）：
```python
# 如果没有 @ 的智能特性，你需要这样写：
y = torch.zeros(B, nh, T, hs)
for b in range(B):
    for h in range(nh):
        y[b, h] = att[b, h] @ v[b, h]  # ← 你需要编写这段代码

# 使用 @，一行代码处理所有操作：
y = att @ v  # ← 编译器自动处理批量循环
```

`@` 运算符是 `torch.matmul()` 的轻量封装，它会调度到优化的 BLAS/cuBLAS 例程（或自定义 CUDA 内核）。它实际上并不是动态确定形状——而是**遵循固定规则**（批量广播 + 收缩最后/倒数第二个维度），这些规则恰好完美适用于注意力计算。