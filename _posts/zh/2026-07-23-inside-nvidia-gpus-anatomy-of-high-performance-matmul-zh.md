---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达GPU内部：高性能矩阵乘法内核剖析
translated: true
type: note
---

## 问题

介绍 Aleksa Gordić 的博客 **"Inside NVIDIA GPUs: Anatomy of high performance matmul kernels"**。

## 回答

这篇博客深入探讨了**现代 GPU 如何在硬件层面实际执行矩阵乘法 (matmul)**，尤其针对 AI 工作负载。它解释了为什么短短几行 PyTorch 代码：

```python
C = A @ B
```

背后隐藏着大量的工程细节。([LZWJava][1])

对于 LLM 来说，这是最重要的话题之一，因为**Transformer 基本上就是 matmul 机器**：

* 线性层：
  [
  Y = XW
  ]
* 注意力投影：
  [
  Q=XW_Q,\ K=XW_K,\ V=XW_V
  ]
* MLP 层：
  [
  XW_1,\ XW_2
  ]

大多数训练/推理的 FLOPs 都发生在这些矩阵乘法中。([Hatena Bookmark][2])

---

# 1. 基本问题

矩阵乘法：

[
C = A \times B
]

其中：

* A: (M \times K)
* B: (K \times N)
* C: (M \times N)

朴素算法：

```python
for i in range(M):
    for j in range(N):
        C[i,j] = 0
        for k in range(K):
            C[i,j] += A[i,k] * B[k,j]
```

复杂度：

[
O(MKN)
]

对于 LLM：

```
hidden size = 4096
batch = 2048

4096 x 4096 权重矩阵
```

意味着每次前向传播都有数十亿次乘加运算。

---

# 2. 为什么 GPU matmul 很难

一个朴素的 CUDA 内核：

```
GPU 线程
    加载 A
    加载 B
    乘法
    写入 C
```

速度极慢。

为什么？

因为 GPU 计算速度远快于内存。

示例：

H100：

```
Tensor Core 计算：
~1000+ TFLOPS

HBM 带宽：
~3 TB/s
```

GPU 可以执行数万亿次运算，但等待内存会严重拖累性能。

关键思路：

> 更少地移动数据。更多地计算。

---

# 3. GPU 内存层次结构

文章解释了层次结构：

```
              慢
               |
        全局内存 (HBM)
               |
            L2 缓存
               |
      共享内存 / L1
               |
          寄存器
               |
         Tensor Core
               |
              快
```

一个优秀的内核会尝试：

```
HBM
 ↓
共享内存
 ↓
寄存器
 ↓
Tensor Core
```

并多次重用数据。

([LZWJava][1])

---

# 4. 分块：核心优化

不计算：

```
整个矩阵
```

而是分成块：

```
A:

+---+---+
|块 |块 |
+---+---+

B:

+---+---+
|块 |块 |
+---+---+
```

一个 CUDA 块计算一个输出块：

```
C 块 = A 块 × B 块
```

示例：

```
128x128 输出块

加载：
A[128x32]
B[32x128]

计算

加载下一个块

计算
```

这使数据保留在快速内存中。

---

# 5. 线程束级编程

NVIDIA GPU 架构：

```
GPU
 |
 +-- SM (流式多处理器)
       |
       +-- 线程束
             |
             +-- 32 个线程
```

一个线程束执行相同的指令：

```
线程0 \
线程1  \
线程2   ---> 相同指令
...
线程31 /
```

高性能内核会仔细映射：

```
矩阵块
      |
      v
线程束
      |
      v
线程
```

---

# 6. Tensor Core

现代 NVIDIA GPU 不再逐个相乘数字。

它们有专门的硬件：

```
Tensor Core:

A 矩阵片段
        +
B 矩阵片段

        |
        v

矩阵乘累加

C += A @ B
```

硬件指令大致为：

```
D = A * B + C
```

称为 MMA：

(矩阵乘累加)

([Google Research][3])

例如：

FP16：

```
16x16x16 矩阵乘法
```

在一次硬件操作中完成。

---

# 7. PTX 和 SASS

堆栈：

```
PyTorch

   ↓

CUDA 内核

   ↓

PTX

   ↓

SASS

   ↓

GPU 指令
```

PTX：

NVIDIA 的虚拟汇编语言。

示例：

```
mma.sync
```

意思是：

"执行 Tensor Core 矩阵乘法"

SASS：

真正的 GPU 机器码。

博客深入到这一层。([Hatena Bookmark][2])

---

# 8. 异步流水线

现代 GPU 重叠执行：

```
加载下一个块
        |
        |
        v
计算当前块
```

而不是：

```
加载
等待
计算
等待
加载
等待
```

一个高性能内核变成了流水线：

```
阶段 0：
HBM -> 共享内存

阶段 1：
共享内存 -> 寄存器

阶段 2：
Tensor Core 计算

阶段 3：
写入结果
```

这就是为什么优化后的内核看起来几乎像硬件设计。

---

# 9. 与 FlashAttention / Triton 的关系

这篇文章有助于理解：

* FlashAttention
* Triton 内核
* CUTLASS
* cuBLAS
* vLLM 内核
* DeepSpeed 内核

它们都使用相同的原理：

1. 分块数据
2. 最大化重用
3. 最小化内存移动
4. 利用 Tensor Core

FlashAttention 基本上是：

> "不单独优化 matmul，而是围绕 GPU 内存层次结构优化整个注意力计算。"

---

# 10. 为什么这对 LLM 工程师很重要

在 PyTorch 层面：

```python
output = model(input)
```

看起来很简单。

但底层：

```
Transformer
 |
线性层
 |
GEMM
 |
cuBLAS 内核
 |
Tensor Core MMA
 |
FP16/BF16 乘累加
 |
GPU 寄存器
```

从：

```
30% GPU 利用率
```

到：

```
90% GPU 利用率
```

之间的差距通常取决于内核工程。

---

对于在 RTX 4070 或 MI300X 上训练 GPT-2/nanoGPT 的人来说，这是介于：

```
"我懂 PyTorch"
```

和：

```
"我理解为什么 H100/MI300X 能达到 1000+ TFLOPS"
```

之间缺失的一层。

这篇文章本质上是一本**从 LLM 工程师视角编写的 GPU 架构教科书章节**。([LZWJava][1])

参考文献：

* [Inside NVIDIA GPUs: Anatomy of high performance matmul kernels - Aleksa Gordić](https://www.aleksagordic.com/blog/matmul?utm_source=chatgpt.com)
* [Mixed-input matrix multiplication performance optimizations - Google Research](https://research.google/blog/mixed-input-matrix-multiplication-performance-optimizations/?utm_source=chatgpt.com)

[1]: https://lzwjava.github.io/gpu-matrix-multiplication-kernels-en?utm_source=chatgpt.com "High-Performance GPU Matrix Multiplication Kernels"
[2]: https://b.hatena.ne.jp/entry/s/www.aleksagordic.com/blog/matmul?utm_source=chatgpt.com "[B!] Inside NVIDIA GPUs: Anatomy of high performance matmul kernels - Aleksa Gordić"
[3]: https://research.google/blog/mixed-input-matrix-multiplication-performance-optimizations/?utm_source=chatgpt.com "Mixed-input matrix multiplication performance optimizations"