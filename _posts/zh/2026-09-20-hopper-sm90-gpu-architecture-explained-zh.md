---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hopper SM90 GPU架构详解
translated: true
type: note
---

**问题：NVIDIA Hopper（SM90）GPU 简介**

**回答：**

NVIDIA Hopper 是 **H100 代 GPU 架构**，于 2022 年推出。对于从 CUDA / 模型训练工作出发的工程师来说，有用的心智模型是：

> **SM90 = Ampere SM80 + 更激进的矩阵计算 + Tensor Memory Accelerator + 异步执行 + FP8 + Transformer Engine。**

旗舰 Hopper GPU 是 **H100**（SXM5 / PCIe），**H200** 后来增加了 HBM3e 容量/带宽，同时保留了 Hopper 架构。

![Image](https://images.openai.com/static-rsc-4/i2ChtU_Ei-R8cC7_jX7aV5UqmkVtCFubgqhCvYSMgLv2YNF-tFkcb2rcpuccCppiqBI9G_fob_Vz3v-Ra0TyWAbd6a5ofX8yp-5Ahy-lLm9q3Wc1GFX1zpD_XPkUChlSEUzF5mTD9GVwzDPjY8xqQOHfOXEMefMXCnt_yqk4jefg7f83Pzv3Am185v_hbOBp?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/LBGpZ6_9RieiVFziH2PdWcI1T6qu_0ySb-l-neyv-c7azYl6yomciGA1HtIaEfCWQAzhv1ULZaU51S23q5cSXSPPzE3KPRslJ8RyEw9ab5JuB3Hbg5zLLbXBg1GWHtMroteWV34W91p7Rp1YBEHqkr-bJnOBzXS8CG4Nwi_yZRUokR-0ACg8MFN3gPDRP_jn?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/L3xvT4LEQDY8-yVCzfpRKrY3qvJAHJYLHjt--2aykSHjVjMqkytuLUg2FH-_DqQlvSJT9DSYJ_kkb_N_IGDze-SNFBBSk4Vgkb26lt1hCJv33tNAfhsPqg-QEO27cvO2zUtMvKup4UwmFco47VvLFCGMl-lyaDXx27cJH_K6Ke6xc6pCJiYpS1UUipx5qj-e?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DuW_N3O6qxuvSVaQeaEiYXXbbXh9gMwmc8Gm8MayhThrar8DCcirQ-qORw9PVEaxiPkViWkUaCb_j7_dYHKdx6Fl-UGZlzFvXseWtZ0yCxCLgCPpgISC7bBY_l8vxrH8Vue-ki_ODZTDpuArt60O9euuMl6e3me6VqaWPPDk86pqQ_3US_N74pLKTewbqps7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/EiOVEGRtg5SyASSNweD6qMlN62GfpvqcEJgNqznVYJ7Icybn6cBY54YJs8m89Y6Fjwzo6XMuQ5BrJLuCNSlHuhRpWlXZqGDeP7B_Dc2OJg4Fd51vj25LyCpSe3CORF9sflZXZXcRIGrShETU_IXtOolyhFsn6PIcCdoEcfCOvagK7pSjOIBqvaTrqvvYbpGV?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/tZUhItHBEHnbdrZREfVcJ0Z4wo6caI6wHJoeSNnHTkYqLaR50Q-Y7nUtGjbvRIywOZ81Kq4sMSEsPCBDp_OgTP-H_swHcGSnpKW1RNRiL5Mw4Z5sCHaMxBUwK3PCVJcUfsQENNIUjnSmHen4aqwtaibGos63FMR7bdt4GYgrb1u3VVvADExGWL65gepBHxHB?purpose=fullsize)

### 1. 层次结构

首先要内化的是硬件层次结构：

```text
H100 GPU
│
├── 8 个 GPC
│   │
│   ├── TPC
│   │   └── SM
│   │       ├── CUDA 核心
│   │       ├── Tensor 核心
│   │       ├── 寄存器
│   │       ├── 共享内存 / L1
│   │       └── 特殊功能 / 加载-存储单元
│   │
│   └── ...
│
├── L2 缓存
│
└── HBM
```

对于 CUDA 编程来说，关键单元仍然是 **SM（流式多处理器）**。

在 Hopper 上，这就是 **SM90**。

一个 CUDA 内核被分解为线程块，线程块被调度到 SM 上：

```text
kernel
  ↓
grid
  ↓
线程块
  ↓
SM90 ── SM90 ── SM90 ── ...
  ↓
warps
  ↓
32 个线程
```

编程模型并没有根本变化：

```cpp
__global__ void saxpy(float *x, float *y) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    y[i] = 2.0f * x[i] + y[i];
}
```

但是 Hopper 极大地改变了 **在一个 SM 内可以异步完成多少工作**。

---

## 2. H100 的基本数据

对于 H100 SXM：

| 属性                   | Hopper H100 |
| --------------------- | ----------: |
| 架构                   |      Hopper |
| 计算能力               |     **9.0** |
| SM 数量                |     **132** |
| CUDA 核心数            |  **16,896** |
| Tensor 核心数          |     **528** |
| HBM                    |        HBM3 |
| HBM 容量               |       80 GB |
| HBM 带宽               |  ~3.35 TB/s |
| L2                     |       50 MB |
| FP8 Tensor             |         是  |
| Transformer Engine     |         是  |
| TMA                    |         是  |
| 线程块簇               |         是  |

一个重要的区别：

**132 个 SM ≠ 132 个独立的 GPU。**

每个 SM 都是一个相当自主的执行引擎，GPU 调度器在其间分配线程块。

---

# 3. SM90 内部到底有什么？

一个有用的简化图：

```text
                    SM90
 ┌──────────────────────────────────────────────┐
 │                                              │
 │  Warp 调度器 / 分发                           │
 │        │                                     │
 │        ├── CUDA 核心                          │
 │        ├── Tensor 核心                        │
 │        ├── 加载/存储                          │
 │        └── SFU                                │
 │                                              │
 │  寄存器文件                                   │
 │                                              │
 │  共享内存 / L1                                │
 │                                              │
 │  Tensor Memory Accelerator (TMA)             │
 │                                              │
 │  异步执行机制                                 │
 │                                              │
 └──────────────────────────────────────────────┘
```

Hopper 最重要的新增功能是 **Tensor 核心、TMA 和异步执行**。

---

# 4. Tensor 核心是 ML 真正的计算引擎

CUDA 核心执行标量/向量类算术运算。

Tensor 核心执行 **矩阵乘加运算**。

从概念上讲：

```text
D = A @ B + C
```

例如：

```text
A: [M × K]
B: [K × N]
C: [M × N]

Tensor 核心
     ↓
D: [M × N]
```

对于 transformer 训练/推理，这几乎直接映射到：

```text
Q @ Kᵀ
attention @ V
X @ W
W_up @ X
W_down @ X
```

这就是为什么 Tensor 核心性能远比原始 CUDA 核心数量对 LLM 更重要。

---

# 5. Hopper 的杀手锏：FP8

Hopper 引入了一流的 **FP8 Tensor 核心** 执行。

常见的 FP8 格式是：

```text
E4M3
E5M2
```

大致来说：

```text
FP32
 ↓
FP16 / BF16
 ↓
FP8
```

您牺牲数值精度/范围来换取大大降低的矩阵计算成本和更低的内存流量。

对于 LLM 工作负载：

```text
权重 / 激活
        ↓
      FP8
        ↓
Tensor Core GEMM
        ↓
 更高的吞吐量
```

Hopper 的 **Transformer Engine** 动态帮助为 transformer 工作负载选择数值格式和缩放策略。

这是 H100 对 LLM 训练如此重要的架构原因之一。

---

# 6. Hopper 的另一个重要特性：TMA

如果您正在编写正式的 CUDA 内核，**TMA — Tensor Memory Accelerator — 可能是您需要学习的最重要的 Hopper 特定特性。**

在 Hopper 之前，常见的 GEMM 策略如下：

```text
全局内存
     ↓
许多线程执行加载
     ↓
寄存器
     ↓
共享内存
     ↓
Tensor 核心
```

线程本身做了大量地址计算和移动。

Hopper 允许您描述多维张量传输，并由专用硬件执行移动：

```text
              TMA
全局内存 ──────────→ 共享内存
         张量传输
```

而不是让每个线程执行：

```cpp
for (...) {
    shared[...] = global[...];
}
```

您基本上可以这样说：

```text
"将这个 2D/3D 张量区域
 从全局内存移动到共享内存。"
```

并让 TMA 机制异步完成。

这很重要，因为现代 GEMM 想要重叠：

```text
        计算
          │
          ▼
      TensorCore
          │
          │
   ┌──────┴──────┐
   │             │
 加载 tile   加载 tile
   │             │
   └──────┬──────┘
          │
       下一个 tile
```

而 Tensor 核心仍在计算中。

---

# 7. Hopper 从根本上讲是关于异步流水线

一个有用的心智模型是：

```text
         时间 →

加载 tile 0 ────────┐
                    │
计算 tile 0         ├──────────
                    │
加载 tile 1         └───────┐
                            │
计算 tile 1                  ├──────────
                            │
加载 tile 2                  └───────┐
                                     │
计算 tile 2                           ├──────
```

而不是：

```text
加载
等待
计算
等待
加载
等待
计算
```

您想要：

```text
加载 ────────────────
      计算 ───────────────
            加载 ────────────────
                  计算 ───────────
```

Hopper 为您提供了更好的原语来构建此流水线。

重要的部分包括：

* `cp.async` 样式的异步内存移动
* **TMA**
* `mbarrier`
* 异步事务管理
* Tensor 核心流水线
* 线程块簇

---

# 8. 线程块簇

Hopper 还扩展了执行层次结构。

以前，有用的心智模型是：

```text
Grid
 └── 线程块
      └── Warps
           └── 线程
```

Hopper 增加了：

```text
Grid
 └── 簇
      ├── 线程块
      ├── 线程块
      ├── 线程块
      └── 线程块
```

簇内的线程块可以更紧密地协作，并使用分布式共享内存机制。

当单个计算需要超出单个 SM 的协作时，这很有用。

对于许多日常 CUDA 内核，您不会用到这个。

对于高性能 GEMM / attention / MoE 内核，它越来越相关。

---

# 9. 内存层次结构

对于 LLM 内核，请这样考虑内存：

```text
                    HBM
                 ~3.35 TB/s
                     │
                     ▼
                    L2
                 50 MB
                     │
                     ▼
              L1 / Shared
               per SM
                     │
                     ▼
                寄存器
```

延迟通常随着您沿层次结构向下移动而减少，容量也会减少。

基本的优化问题是：

> **在隐藏 HBM 延迟的同时，让昂贵的 Tensor 核心保持忙碌。**

例如，一个朴素实现：

```text
HBM → Tensor 核心 → HBM
```

可能会花费大量时间等待内存。

一个好的实现反而尝试做到：

```text
                  ┌───────────────┐
HBM → 共享内存 ────→│ Tensor 核心   │
                  └───────────────┘
                       ↑
                  下一个 tile 加载
```

两侧并发运行。

---

# 10. 为什么 H100 对 transformer 如此出色

以 transformer 线性层为例：

```python
Y = X @ W
```

假设：

```text
X = [batch × sequence, hidden]
W = [hidden, 4 × hidden]
```

这是一个巨大的 GEMM。

Hopper 可以大致按如下方式执行它：

```text
HBM
 │
 │ TMA
 ▼
Shared Memory
 │
 │
 ▼
Tensor 核心
 │
 │ FP8/BF16/FP16
 ▼
累加器
 │
 ▼
输出
```

整个架构都围绕使此流水线高效而进行了大量优化。

这就是为什么 PyTorch、cuBLAS、CUTLASS、FlashAttention 和 Transformer Engine 等框架在 Hopper 上如此重要的原因：**硬件功能强大，以至于内存移动和内核调度成为首要问题。**

---

# 11. SM90 vs SM80

如果您使用过 A100，清晰的比较是：

```text
A100 / Ampere
SM80
 │
 ├── Tensor 核心
 ├── BF16
 ├── FP16
 └── cp.async
```

对比：

```text
H100 / Hopper
SM90
 │
 ├── 更强大的 Tensor 核心
 ├── FP8
 ├── Transformer Engine
 ├── TMA
 ├── mbarrier
 ├── 线程块簇
 └── 更复杂的异步执行
```

所以不要仅仅将 Hopper 视为：

> "A100 但更快。"

更好的心智模型是：

> **Hopper 将内核编程模型改变为显式流水线化的异步张量计算。**

---

# 12. 如果您在 H100 上编写 CUDA

从以下开始：

```bash
nvcc -arch=sm_90 kernel.cu
```

或者，对于可以针对 Hopper 进行 JIT 的 PTX：

```bash
nvcc -arch=compute_90 kernel.cu
```

然后使用以下命令检查您的内核：

```bash
ncu ./your_program
```

我会问的问题是：

```text
1. 我使用了多少 HBM 带宽？
2. Tensor 核心利用率如何？
3. 占用率如何？
4. 寄存器压力大吗？
5. 共享内存带宽呢？
6. 加载是否与计算重叠？
7. Tensor 核心是否因内存而停滞？
8. 指令级 / warp 级并行度如何？
```

对于认真的优化，**Nsight Compute** 变得几乎与 CUDA 源代码本身一样重要。

---

# 13. 最简单的 Hopper 心智模型

如果您只记住这个：

```text
                    H100 / SM90

             ┌──────────────────────┐
             │       HBM3            │
             └──────────┬───────────┘
                        │
                       TMA
                        │
                        ▼
             ┌──────────────────────┐
             │   共享内存/L1         │
             └──────────┬───────────┘
                        │
                异步流水线
                        │
                        ▼
             ┌──────────────────────┐
             │    Tensor 核心       │
             │                      │
             │   FP8 / FP16 / BF16  │
             │        GEMM          │
             └──────────┬───────────┘
                        │
                        ▼
                   寄存器
```

**Hopper 是一台为 Tensor 核心供料的机器。**

性能游戏是：

```text
HBM
 ↓
高效移动 tiles
 ↓
共享内存
 ↓
持续供给 Tensor 核心
 ↓
将下一次内存传输与当前计算重叠
 ↓
重复
```

这是高性能 H100 内核（如 **FlashAttention、融合 MLP、MoE 内核和优化 GEMM**）的基础。

如果您来自训练大型模型，我会按以下顺序学习 Hopper：

```text
SM90 执行模型
    ↓
Tensor Core MMA
    ↓
共享内存 + 寄存器分块
    ↓
异步流水线
    ↓
TMA
    ↓
mbarrier
    ↓
warp 特化内核
    ↓
线程块簇
    ↓
CUTLASS / CuTe
    ↓
FlashAttention / Transformer Engine 内部机制
```

这条路径将您从 **"我了解 CUDA"** 带到 **"我可以推理为什么 H100 内核很快。"**

我还可以构建一个 **从原始 CUDA → TMA → Tensor Core MMA 的最小 SM90 GEMM**，展示了实际的数据移动和指令级流水线。
