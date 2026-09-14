---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tensor Core加速Transformer性能
translated: true
type: note
---

Question: **为什么 Tensor Cores 对现代深度学习如此重要？**

答案：因为 **Transformer 本质上就是巨型矩阵乘法**，而 Tensor Cores 是专门用于以比普通 CUDA cores 高得多的吞吐量执行这些乘法的专用硬件。

重要的区别在于：

```text
CUDA core:
    标量/向量算术

Tensor Core:
    矩阵 × 矩阵 + 累加
```

### 1. Transformer 中实际发生的事情

以单个线性层为例：

$$
Y = XW
$$

假设：

```text
X: [4096, 4096]
W: [4096, 4096]
```

这大约相当于：

$$
2 \times 4096^3 \approx 1370 \text{ 亿 FLOPs}
$$

而 Transformer 会**一次又一次**地执行这个操作，跨越许多层和 token。

Attention 有更多的矩阵乘法：

$$
QK^T
$$

$$
\text{softmax}(QK^T)V
$$

MLP 还有几个：

$$
XW_1,\quad XW_2
$$

所以 GEMM 主导了计算量。

---

## 2. CUDA cores 可以做这件事，但 Tensor Cores 处理 GEMM 简直是小事一桩

从概念上讲，CUDA core 做的事情类似于：

```python
for i:
    for j:
        for k:
            C[i,j] += A[i,k] * B[k,j]
```

而 Tensor Cores 拥有硬件指令，可以有效地在**单次操作中执行小型矩阵乘加块**。

例如，概念上：

```text
       A              B
   ┌───────┐       ┌───────┐
   │       │       │       │
   │  16×16│   ×   │  16×16│
   │       │       │       │
   └───────┘       └───────┘
          \           /
           \         /
            ┌───────┐
            │  C    │
            └───────┘
```

具体的块尺寸/指令因 GPU 架构和数据类型而异，但关键思想在于硬件是专门围绕稠密矩阵运算构建的。

---

## 3. 疯狂之处在于吞吐量

这就是你的 P100 问题关键所在。

大致来看：

```text
P100
  FP32 CUDA:       ~10 TFLOPS
  Tensor Cores:     0

V100
  FP32 CUDA:       ~15.7 TFLOPS
  FP16 Tensor:    ~125 TFLOPS
```

Tensor Core 的确切数字取决于你讨论的是稠密/稀疏模式、累加类型、时钟等，但重要的数量级差异是：

```text
P100:  ~10 TFLOP/s
V100: ~100+ TFLOP/s Tensor Core
```

这就是为什么 **V100 不只是一个"稍微快一点的 P100"。**

对于 Tensor Cores 所针对的工作负载而言，它几乎是不同级别的机器。

---

# 4. 为什么 FP16 使其特别强大

现代神经网络通常不需要每个中间计算都是 FP32。

你通常可以这样做：

```text
权重        FP16/BF16
激活        FP16/BF16
GEMM        FP16/BF16
累加        FP32
```

概念上：

$$
C_{FP32} = \sum A_{FP16}B_{FP16}
$$

这非常有用，因为神经网络训练对降低精度有异常的容忍度。

Tensor Cores 就是专门围绕这一点设计的。

所以不再是这样：

```text
FP32 GEMM
  ↓
CUDA cores
  ↓
~10 TFLOP/s
```

而是变成：

```text
FP16/BF16 GEMM
      ↓
 Tensor Cores
      ↓
~100+ TFLOP/s
```

这就是现代 GPU 成为如此强大的 AI 加速器的根本原因。

---

# 5. 为什么你的 P100 特别不适合现代 LLM 训练

P100 是 Pascal 架构。

```text
Pascal P100
    │
    ├── FP32 CUDA cores
    ├── FP16 CUDA 算术
    └── 无 Tensor Cores
```

V100 是 Volta 架构：

```text
Volta V100
    │
    ├── FP32 CUDA cores
    ├── FP16 算术
    └── Tensor Cores  ← 巨大升级
```

然后：

```text
Turing
  ↓
Ampere
  ↓
Hopper
  ↓
Blackwell
```

Tensor Core 能力变得越来越复杂：

```text
FP16
 ↓
BF16
 ↓
TF32
 ↓
FP8
 ↓
FP4 / 更新的低精度
```

所以如果你在训练 LLM，相关的比较不仅仅是：

```text
"有多少个 CUDA cores？"
```

而更接近于：

```text
有效训练吞吐量
    ≈
Tensor-Core GEMM 吞吐量
    ×
内存带宽
    ×
软件效率
```

---

# 6. 一个有用的心智模型

把 CUDA cores 看作**通用 ALU**。

Tensor Cores 就像是说：

> "我知道你整天都要做巨型矩阵乘法。这里有一个专门用于生产矩阵乘积的工厂。"

对于 LLM：

```text
                 Transformer
                     │
          ┌──────────┴──────────┐
          │                     │
       Attention              MLP
          │                     │
      Q @ Kᵀ, P @ V          X @ W
          │                     │
          └──────────┬──────────┘
                     ↓
                   GEMM
                     ↓
               Tensor Cores
```

这就是为什么 Tensor Cores 如此重要。

---

## 7. 但有一个重要的注意事项：内存带宽

Tensor Cores 不是魔法。

如果你的操作是**内存受限**的，拥有 10 倍的 Tensor Core FLOPS 并不一定意味着速度快 10 倍。

例如：

```text
GPU 计算能力：
    1000 TFLOP/s

但内存系统只能供给：
    100 GB/s

→ Tensor Cores 闲置
```

这就是为什么 LLM 性能涉及以下几个方面的协同配合：

* 计算吞吐量
* HBM 带宽
* 缓存
* kernel 融合
* 算术强度
* 量化
* 批大小
* 序列长度

这也是为什么你的 P100 尽管缺少 Tensor Cores 但仍然有趣的原因：**732 GB/s 的 HBM2 带宽对于 ¥400 来说仍然相当不错。**

但对于**大型 GEMM**，V100 的 Tensor Cores 完全改变了局面。

### 总结

如果你在做：

```text
CUDA 编程
FP32 科学计算
内存带宽实验
便宜的 16GB GPU 实验
```

P100 @ ¥400 = **很棒的玩具**。

如果你在做：

```text
LLM 训练
LLM 微调
大型 FP16/BF16 GEMM
```

那么：

```text
P100  ← 🐢
V100  ← 🚀
A100  ← 🚀🚀🚀
H100  ← 🚀🚀🚀🚀
```

即使它们的原始 CUDA-core 数量看起来没有明显差异。

我还可以详细分解**一个实际的 `torch.matmul()` 从 Python → CUDA kernel → Tensor Core 指令**的过程，这将使 P100 和 V100 的差异变得非常具体。
