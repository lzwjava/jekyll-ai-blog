---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'CUTLASS: 快速GPU矩阵乘法'
translated: true
type: note
---

问题：什么是CUTLASS，它如何让GPU矩阵乘法变得快速？

答案：

**CUTLASS = CUDA Templates for Linear Algebra Subroutines（线性代数子程序的CUDA模板）。**

它是NVIDIA编写**高性能GPU内核**的库/框架，尤其擅长**GEMM（通用矩阵乘法）**：

\[
C = A \times B
\]

它位于以下层次之间：

```
PyTorch / TensorFlow
        |
      cuBLAS
        |
     CUTLASS
        |
      CUDA
        |
    Tensor Core / SM hardware
```

CUTLASS 提供了底层构建模块，让工程师能够编写性能接近 cuBLAS 但针对特定模型、数据类型和 GPU 架构定制化的内核。（[NVIDIA 文档][1]）

---

## 为什么需要 CUTLASS

一个朴素的 CUDA 矩阵乘法：

```cpp
for (i)
  for (j)
    for (k)
       C[i][j] += A[i][k] * B[k][j];
```

在 GPU 上性能极差。

为什么？

因为：

* 全局内存很慢
* 每个线程做的工作很少
* 没有使用 Tensor Core
* 没有共享内存复用

现代 GPU 的 GEMM 看起来像这样：

```
Global Memory
      |
      v
+-------------+
| Threadblock |
|   128x128   |   <-- CTA tile
+-------------+
      |
      v
 Shared Memory
      |
      v
+-------------+
|   Warp      |
|    64x64    |
+-------------+
      |
      v
 Tensor Core
   mma.sync
```

CUTLASS 为每一层提供了抽象。（[NVIDIA 文档][2]）

---

# 1. 核心思想：分层分块

假设：

```
A = 4096 x 4096
B = 4096 x 4096
```

你不是逐个计算：

```
C[0][0]
C[0][1]
...
```

而是：

```
C 矩阵

+----------------+
|128|128|128|128 |
|---+---+---+---|
|128|128|128|128 |
|---+---+---+---|
|128|128|128|128 |
+----------------+
```

每个 CUDA block 拥有一个分块：

```
CTA tile:

        B
   128 columns

   +-----------+
   |           |
128|     C     |
rows|  tile    |
   |           |
   +-----------+

```

然后：

\[
C_{tile}=A_{tile}\times B_{tile}
\]

---

# 2. 分块内部

对于一个 128x128 的输出分块：

K 维度是流式处理的：

```
A:

128 x K


B:

K x 128


C:

128 x 128
```

将 K 拆分：

```
K=4096

step 0:

A[128 x 32]

B[32 x 128]


step 1:

A[128 x 32]

B[32 x 128]

...
```

累加：

\[
C += A_i B_i
\]

这就是 GEMM 的主循环。

---

# 3. Tensor Core 路径

现代 NVIDIA GPU 不是一次计算一个浮点数。

Tensor Core 指令：

```
mma.sync
```

在硬件中执行类似：

```
16x16x16 矩阵乘法
```

示例：

```
A fragment:

16 x 16

B fragment:

16 x 16


Tensor Core:

A @ B

=

C
```

CUTLASS 自动映射：

```
thread
   |
warp
   |
warpgroup
   |
Tensor Core instruction
```

---

# 4. CUTLASS 概念

重要术语：

## Tile（分块）

矩阵的一个块：

```
128 x 128
```

示例：

```
GemmShape<128,128,32>
```

表示：

```
M = 128
N = 128
K = 32
```

---

## Threadblock（线程块）

一个 CUDA block。

示例：

```
256 个线程
```

拥有：

```
128x128 C 分块
```

---

## Warp tile（线程束分块）

一个 warp（32 个线程）拥有：

```
64x64
```

---

## MMA（矩阵乘法累加）

```
D = A*B + C
```

Tensor Core 操作。

---

## Layout（布局）

非常重要。

GPU 内存是线性的：

```
0 1 2 3 4 5 ...
```

但矩阵是：

```
A[i][j]
```

CUTLASS 需要映射：

```
逻辑坐标

(i,j)

      |
      v

内存地址
```

这正是 CuTe（CUTLASS 3.x）改进的地方。（[NVIDIA 文档][3]）

---

# 5. 为什么 2048 比 2047 快

你之前的问题与此直接相关。

GPU 喜欢：

```
分块大小 = 128
```

对于：

```
2048 / 128 = 16
```

完美：

```
16 x 16 个分块
```

对于：

```
2047 / 128
```

你会得到：

```
15 个完整分块

+

一个部分分块
```

最后一个分块浪费了：

```
128 - 127 个有效元素
```

线程仍然存在。

GPU 执行 warp，而不是单个有用元素。

CUTLASS/cuBLAS 针对这些规则形状进行了优化。（[NVIDIA 文档][2]）

---

# 6. 小型 CUTLASS 示例

概念上：

```cpp
using Gemm = cutlass::gemm::device::Gemm<
    half,                 // A
    RowMajor,
    half,                 // B
    ColumnMajor,
    float                 // accumulator
>;

Gemm gemm;

gemm({
    {M,N,K},
    {A,lda},
    {B,ldb},
    {C,ldc}
});
```

模板参数选择：

* 数据类型
* 内存布局
* 架构
* 指令类型
* 分块策略

CUTLASS 使用 C++ 模板元编程来生成专门化的内核。（[NVIDIA 文档][1]）

---

# 7. 这对 LLM 推理/训练为何重要

Transformer 本质上是：

```
Attention:

Q @ K^T

+

softmax

+

V


MLP:

X @ W1

X @ W2
```

大部分计算：

```
矩阵乘法
```

因此：

```
LLM 性能
        |
        v
快速 GEMM
        |
        v
Tensor Core 利用率
        |
        v
CUTLASS 知识
```

像：

* FlashAttention
* xFormers
* TensorRT-LLM
* vLLM 内核

等项目都在这个领域内。

---

对你来说（因为你已经在做 nano-vLLM/nanoGPT），一个好的学习路径：

```
1. CUDA 基础
   |
2. 编写朴素 matmul 内核
   |
3. 共享内存分块 matmul
   |
4. WMMA Tensor Core 示例
   |
5. CUTLASS GEMM 示例
   |
6. FlashAttention 内核
   |
7. vLLM PagedAttention CUDA 内核
```

CUTLASS 基本上是从**“我理解 PyTorch”**到**“我能编写让 PyTorch 变快的内核”**的桥梁。

参考文献：

* NVIDIA CUTLASS 文档 ([NVIDIA 文档][1])
* CUTLASS GEMM API ([NVIDIA 文档][2])
* CUTLASS 入门指南 ([NVIDIA 文档][4])

[1]: https://docs.nvidia.com/cutlass/latest/index.html?utm_source=chatgpt.com "欢迎来到 CUTLASS — NVIDIA CUTLASS 文档"
[2]: https://docs.nvidia.com/cutlass/latest/media/docs/cpp/gemm_api.html?utm_source=chatgpt.com "CUTLASS GEMM API — NVIDIA CUTLASS 文档"
[3]: https://docs.nvidia.com/cutlass/latest/overview.html?utm_source=chatgpt.com "概述 — NVIDIA CUTLASS 文档"
[4]: https://docs.nvidia.com/cutlass/latest/media/docs/cpp/getting_started.html?utm_source=chatgpt.com "入门指南 — NVIDIA CUTLASS 文档"