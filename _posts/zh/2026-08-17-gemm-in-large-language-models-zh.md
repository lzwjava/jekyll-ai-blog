---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型中的GEMM
translated: true
type: note
---

问题：什么是LLM中的**GEMM**？

答案：

**GEMM = 通用矩阵乘法（General Matrix-Matrix Multiplication）**。

它本质上是如下运算：

\[
C = AB
\]

其中：

* \(A \in \mathbb{R}^{M \times K}\)
* \(B \in \mathbb{R}^{K \times N}\)
* \(C \in \mathbb{R}^{M \times N}\)

在LLM中，**绝大部分计算最终都归结为GEMM**。

### 1. 最简单的例子：线性层

Transformer的线性层是：

```python
y = x @ W
```

假设：

```text
x: [batch * seq_len, hidden]
W: [hidden, 4 * hidden]
```

例如：

```text
x = [8192, 4096]
W = [4096, 16384]

y = x @ W

y = [8192, 16384]
```

这就是一个GEMM：

\[
[8192 \times 4096] [4096 \times 16384]
\rightarrow
[8192 \times 16384]
\]

---

### 2. Transformer FFN 基本上是 GEMM → 激活函数 → GEMM

对于标准MLP：

```python
h = x @ W1
h = activation(h)
y = h @ W2
```

因此：

\[
XW_1 \rightarrow \text{GELU} \rightarrow HW_2
\]

两个大型GEMM占据了主要计算量。

对于SwiGLU块：

```python
a = x @ W_gate
b = x @ W_up
h = silu(a) * b
y = h @ W_down
```

那是**三个GEMM**。

---

### 3. 注意力机制也包含GEMM

给定：

```python
Q = X @ Wq
K = X @ Wk
V = X @ Wv
```

这些都是GEMM。

然后注意力有：

\[
S = QK^T
\]

这是另一个矩阵乘法。

以及：

\[
O = \operatorname{softmax}(S)V
\]

又是一个矩阵乘法。

所以一个Transformer层包含大量矩阵乘法。

---

### 4. 为什么GPU如此看重GEMM

一个GEMM：

\[
C_{ij} = \sum_{k=1}^{K} A_{ik}B_{kj}
\]

大约需要：

\[
2MNK
\]

次浮点运算。

例如：

```text
M = 8192
K = 4096
N = 16384
```

得到：

\[
2 \times 8192 \times 4096 \times 16384
\approx 1.1 \times 10^{12}
\]

这就是**约1.1 TFLOPs的计算量，仅一次矩阵乘法**。

而这正是GPU极其擅长的规则化高密度计算。

---

### 5. GEMM vs GEMV

在LLM推理中你会经常看到这些术语：

```text
GEMM = 矩阵 × 矩阵
GEMV = 矩阵 × 向量
```

例如，在**训练 / prefill** 阶段：

```text
[sequence, hidden] @ [hidden, hidden]
```

是GEMM。

在**单token解码**阶段，你可能遇到：

```text
[1, hidden] @ [hidden, hidden]
```

这实际上是GEMV。

这种区别对LLM推理影响巨大：

```text
Prefill:
大 M
→ GEMM
→ GPU利用率高
→ 计算受限

Decode:
M ≈ 1
→ GEMV / 瘦GEMM
→ GPU利用率低
→ 通常受内存带宽限制
```

这就是**LLM解码与训练/prefill本质不同**的原因之一。

### 6. GEMM → Tensor Core

在现代NVIDIA GPU上，通常不需要自己实现：

```python
C[i,j] += A[i,k] * B[k,j]
```

像 **cuBLAS/cuBLASLt** 这样的库会将GEMM派发给高度优化的GPU内核，这些内核可以使用 **Tensor Core**。

概念上：

```text
PyTorch
   ↓
torch.matmul()
   ↓
cuBLAS / cuBLASLt
   ↓
Tensor Core kernels
   ↓
FP16 / BF16 / FP8 / INT8 / ...
```

这就是为什么当你查看LLM性能时，以下术语：

**FLOPS, TFLOPS, Tensor Cores, GEMM, GEMV, MFMA, CUTLASS, cuBLAS, Triton**

会反复同时出现。

重要的心智模型是：

> **Transformer在很大程度上是一种将张量转化为一系列高度优化的矩阵乘法（同时伴随注意力、归一化、激活和内存移动）的机器。**

对于训练LLM，**GEMM是需要理解的核心内核之一**。