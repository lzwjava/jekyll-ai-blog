---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch中的Einsum详解
translated: true
type: note
---

问题：在PyTorch中，`einsum`的含义/作用是什么？

回答：

`torch.einsum` 是爱因斯坦求和约定——一种微型领域特定语言（DSL），用于表达张量索引上的乘积求和运算，无需手动调用`transpose`/`matmul`/`sum`。你只需要指定每个输入张量具有哪些索引，以及输出中保留哪些索引；任何在输入中重复但**不在**输出中的索引都会进行求和（即缩并）。

签名：
```python
torch.einsum(equation, *tensors)
```

核心规则：`'ij,jk->ik'` 表示“对于输出索引(i,k)，对j求和 A[i,j] * B[j,k]”——这就是矩阵乘法。

```python
import torch

A = torch.randn(3, 4)
B = torch.randn(4, 5)

# 标准矩阵乘法
C1 = A @ B
C2 = torch.einsum('ij,jk->ik', A, B)
torch.allclose(C1, C2)  # True
```

具体的前向传播风格示例（批量注意力分数，实际中你日常使用的场景）：
```python
# Q, K: (batch, heads, seq, dim)
Q = torch.randn(2, 8, 10, 64)
K = torch.randn(2, 8, 10, 64)

# scores[b,h,i,j] = sum_d Q[b,h,i,d] * K[b,h,j,d]
scores = torch.einsum('bhid,bhjd->bhij', Q, K)
# 等价于：Q @ K.transpose(-2, -1)
print(scores.shape)  # (2, 8, 10, 10)
```

其他常见模式：
```python
# 批量矩阵乘法
torch.einsum('bij,bjk->bik', A, B)          # == torch.bmm(A, B)

# 外积
torch.einsum('i,j->ij', a, b)               # a[:,None] * b[None,:]

# 迹
torch.einsum('ii->', A)                     # A.trace()

# 转置
torch.einsum('ij->ji', A)                   # A.T

# 逐元素相乘后求和（每批行的点积）
torch.einsum('bi,bi->b', a, b)              # (a*b).sum(-1)

# 对某一轴求和
torch.einsum('ij->i', A)                    # A.sum(dim=1)
```

思维模型：将其视为编写数学表达式的朴素嵌套循环版本，而einsum只需告诉后端哪些循环索引需要保留（输出），哪些需要缩并（求和，即重复但未出现在输出中的索引）。在内部，它会调度到优化的`bmm`/`matmul`/`sum`内核（当有多个缩并时，会通过类似opt_einsum的路径优化），因此其速度并不比手动编写的操作慢——它更是一种提升可读性和正确性的工具，尤其是在处理注意力机制/MoE代码中>=4D的张量时，手动使用`.transpose().reshape().matmul()`链容易出错。

一个需要注意的点：对于超过2个张量或较长的公式，`torch.einsum`会自动寻找缩并顺序，但并非总是选择FLOP最优的路径——对于性能关键的多张量缩并，建议检查`opt_einsum`或通过与手动操作进行基准测试来对比。

参考文献：
- [torch.einsum文档](https://docs.pytorch.org/docs/stable/generated/torch.einsum.html)
- [Einsum is All You Need（Kolter/Rush讲解）](https://rockt.ai/2018/04/30/einsum)