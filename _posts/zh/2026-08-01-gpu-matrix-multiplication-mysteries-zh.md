---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU矩阵乘法之谜
translated: true
type: note
---

问题：介绍 Thonking.ai 的《奇怪的矩阵乘法》

回答：

这篇文章由 Horace He 撰写，探讨一个非常实际的 GPU/AI 系统问题：

**为什么两个数学上等价的矩阵乘法在 GPU 上的性能可能天差地别？** ([Thonking.ai][1])

对于 LLM 工程师来说，这一点极其相关，因为 **Transformer 的推理和训练本质上就是大量的 GEMM（通用矩阵乘法）**：

```
Attention:
Q = XWq
K = XWk
V = XWv

MLP:
h = XW1
y = hW2
```

每一个都变成：

```
[M x K] @ [K x N] = [M x N]
```

令人惊讶的是：

```
2048 x 2048 @ 2048 x 2048
```

有时比：

```
2047 x 2048 @ 2048 x 2048
```

更快，尽管后者的 FLOPs 更少。([Thonking.ai][1])

## 1. 矩阵乘法不仅仅是数学

数学运算：

```
C = A @ B

C[i,j] = sum(A[i,k] * B[k,j])
```

看起来很简单。

但 GPU 的执行方式并非如此：

```
for i:
    for j:
        for k:
            C[i,j] += A[i,k]*B[k,j]
```

现代 GPU 的执行方式是：

```
矩阵
  |
  v
分割成 tile
  |
  v
GPU 线程块
  |
  v
共享内存
  |
  v
Tensor Cores
```

GPU 喜欢规整的形状。

---

## 2. Tiling：隐藏的原因

假设 GPU kernel 使用 tile：

```
128 x 128
```

它将：

```
2048 x 2048 矩阵

分割为：

16 x 16 个 tile
```

完美：

```
2048 / 128 = 16
```

没有浪费。

但是：

```
2047 / 128 = 15.99
```

现在 GPU 需要：

```
15 个完整 tile
+
1 个部分 tile
```

最后一个 tile 浪费了计算。

示例：

```
实际计算：

127 x 127


GPU 执行：

128 x 128
```

大量 GPU 操作被掩码。

---

## 3. 内存对齐很重要

文章解释，"奇数形状"问题通常不在于奇数本身，而在于**最内层维度**是否与 GPU 内存访问对齐。([Thonking.ai][2])

GPU 喜欢：

```
float16 / bfloat16

128 个元素
256 字节
512 字节
```

因为：

```
内存事务
        |
        v
对齐的块
```

是高效的。

不好的情况：

```
2047 个元素
```

意味着：

```
GPU 内存：

[128][128][128]...[127]

最后一次加载：
未对齐
```

更多内存事务。

---

## 4. Wave 量化

这是另一个 GPU 特有的效应。

示例：

GPU：

```
80 个 SMs
```

Kernel 创建：

```
160 个 block
```

完美：

```
SM0: block0
SM1: block1
...
SM79:block79

第二波：
所有 SMs 再次满载
```

但是：

```
161 个 block
```

意味着：

```
wave 1:
80 个 block

wave 2:
80 个 block

wave 3:
1 个 block
```

最后一波仅使用了：

```
1 / 80
```

的 GPU。

效率极低。

这在基准测试中产生了那些奇怪的性能尖峰。([Thonking.ai][1])

---

## 5. 这对 vLLM / nano-vLLM 的重要性

这正是生产级推理引擎关注形状的原因。

示例：

Qwen：

```
hidden size = 4096
heads = 32
```

线性层：

```
[batch,4096]
       @
[4096,12288]

=
[batch,12288]
```

如果：

```
batch=1
```

在解码期间：

```
[1,4096] @ [4096,12288]
```

这与训练时的 GPU 问题截然不同：

```
[4096,4096] @ [4096,12288]
```

训练：

* 巨大矩阵
* 计算密集型

推理解码：

* 极小 batch
* 内存密集型
* KV cache 占主导

这就是 vLLM 拥有以下优化的原因：

* continuous batching
* paged KV cache
* CUDA kernels
* fused operations

---

## 6. 更深层的启示

本文是 AI 系统中一个原则的很好例证：

> 算法不仅仅是数学。硬件执行模型本身也成为算法的一部分。

一行 PyTorch 代码：

```python
C = A @ B
```

看起来是一个操作。

但底层是：

```
PyTorch
 |
 v
cuBLAS
 |
 v
CUDA kernel 选择
 |
 v
线程块
 |
 v
warps
 |
 v
Tensor Core 指令
 |
 v
内存层级
```

性能取决于所有层级。

对于正在学习 **nano-vLLM / CUDA / AI 基础设施**的人来说，这篇文章正是理解 Transformer 数学之后的下一步：

1. Transformer 等式
2. PyTorch 实现
3. CUDA 内存模型
4. GEMM kernels
5. Tensor Core 优化
6. vLLM 调度

这是从"我会用 LLM"到"我理解 GPT 为什么跑得快"的路径。([Thonking.ai][1])

参考资料：

* Horace He，"矩阵乘法喜欢什么形状？" ([Thonking.ai][1])
* Horace He，"解答：矩阵乘法喜欢什么形状？" ([Thonking.ai][2])
* NVIDIA，矩阵乘法性能文档（文章引用）([Thonking.ai][1])

[1]: https://www.thonking.ai/p/what-shapes-do-matrix-multiplications?utm_source=chatgpt.com "What Shapes Do Matrix Multiplications Like? [medium]"
[2]: https://www.thonking.ai/p/answer-key-what-shapes-do-matrix?utm_source=chatgpt.com "Solutions: What Shapes Do Matrix Multiplications Like?"
