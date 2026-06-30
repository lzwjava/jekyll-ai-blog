---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA面向AI的演进
translated: true
type: note
---

问题：CUDA 多年来是如何演变的？

让我先理清当前状态，再梳理时间线。问题：CUDA 多年来是如何演变的——其历史上主要的架构和编程模型转变有哪些？

答案：

CUDA 的演变沿着两条交织的脉络展开：**硬件**（每代 GPU 架构增加新功能）和**编程模型**（如何表达并行性）。以下是从模型训练者视角梳理的主线——实际影响你编写的代码和获得的 FLOPs 的变化。

## 概览

```
2006  CUDA 1.0      SIMT 模型诞生——线程、块、网格、共享内存
2008  CUDA 2.x      双精度（Tesla）、原子操作
2010  CUDA 3.x      Fermi：真正的 L1/L2 缓存、ECC、统一地址空间
2012  CUDA 5.x      Kepler：动态并行、GPUDirect
2014  CUDA 6.x      统一内存（cudaMallocManaged）
2016  CUDA 8.x      Pascal：NVLink、FP16、页迁移统一内存
2017  CUDA 9.x      Volta：张量核心、独立线程调度、协作组
2018  CUDA 10.x     Turing：INT8/INT4 张量核心、RT 核心
2020  CUDA 11.x     Ampere：TF32、BF16、稀疏性、异步拷贝（cp.async）、CUDA Graphs 成熟
2022  CUDA 12.x     Hopper：FP8、TMA、线程块集群、wgmma、分布式共享内存
2025  CUDA 13.x     Blackwell：FP4/FP6、瓦片编程模型（cuTile）、放弃 pre-Turing
```

对 AI 而言，最重要的转折点是 **Volta（2017）引入张量核心**——专用的矩阵乘法单元。此后的一切都是为了更好地喂饱它们。

## 对 ML 重要的编程模型转变

**1. SIMT（2006 至今）：基础**

你从单个线程的视角编写内核；硬件以 32 线程为一组同步执行 warp。这是你训练 GPT-2 时使用的思维模型。

```cuda
__global__ void saxpy(int n, float a, float* x, float* y) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;  // 全局线程索引
    if (i < n) y[i] = a * x[i] + y[i];
}
// 启动：saxpy<<<(n+255)/256, 256>>>(n, 2.0f, d_x, d_y);
```

**2. 张量核心（Volta，2017）：AI 的转折点**

不再是每个线程执行一次 FMA，而是整个 warp 协作执行矩阵乘加运算。`wmma` API（后来是 `mma`，Hopper 上是 `wgmma`）暴露了这一功能。这就是为什么 H100 的 BF16 算力约 1000 TFLOPS，而 CUDA 核心只有几十 TFLOPS——你的 transformer 中的 `Q @ K^T` 就在这里运行。

```cuda
#include <mma.h>
using namespace nvcuda::wmma;
fragment<matrix_a, 16, 16, 16, half, row_major> a_frag;
fragment<matrix_b, 16, 16, 16, half, col_major> b_frag;
fragment<accumulator, 16, 16, 16, float> c_frag;
fill_fragment(c_frag, 0.0f);
load_matrix_sync(a_frag, a, 16);
load_matrix_sync(b_frag, b, 16);
mma_sync(c_frag, a_frag, b_frag, c_frag);   // 在张量核心上执行 16x16x16 MMA
store_matrix_sync(c, c_frag, 16, mem_row_major);
```

**3. 异步 + 内存层次结构（Ampere→Hopper，2020–2022）**

瓶颈变成了*喂饱*张量核心，而非计算本身。因此 CUDA 增加了：
- `cp.async`（Ampere）：将数据从全局内存拷贝到共享内存，无需经过寄存器，并与计算重叠。这是 FlashAttention 流水线化的核心。
- **TMA**（Hopper）：一个硬件 DMA 引擎，通过单条指令执行批量异步张量拷贝——程序员只需传递一个描述符，无需计算每个线程的地址。
- **线程块集群 + 分布式共享内存**（Hopper）：同一 SM 集群上的块可以读取彼此的共享内存。

**4. 更低精度（不断下降的趋势）**

```
FP32 → TF32（Ampere）→ FP16/BF16 → FP8（Hopper）→ FP4/FP6（Blackwell）
```

每降低一半精度，吞吐量大约翻倍，内存占用减半。DeepSeek-v3/v4 能在 FP8 下训练，完全是因为 Hopper 将 FP8 张量核心作为一等公民。Blackwell 的 FP4 正在推动当前推理成本的急剧下降。

**5. CUDA Graphs（11.x）：消除启动开销**

对于小型内核（在 LLM 解码中很常见，每个 token 由一系列小操作组成），每次启动的 CPU 开销占主导地位。Graphs 一次性捕获一个序列，然后作为单个提交重放——对推理来说是一个重大胜利。

**6. 瓦片编程（CUDA 13.1，2025）：最新的转变**

最近的变化在概念上是自 SIMT 以来最大的。CUDA 从一开始就采用基于 SIMT 的线程并行模型；CUDA 13.0 为互补的基于瓦片的编程模型奠定了基础。CUDA 13.1 推出了 CUDA Tile——一种基于瓦片的编程模型，用于抽象包括张量核心在内的专用硬件，同时提供了 Python DSL（cuTile）和新的瓦片 IR。

动机：SIMT 提供了最大程度的控制，但编写高性能代码需要相当大的努力，尤其是在多个 GPU 架构之间。瓦片编程则相反——你指定数据块（瓦片）以及对这些瓦片的计算，编译器和运行时负责将逐元素执行映射到硬件上。这是 NumPy/Triton 的思维模型原生融入 CUDA。PTX 确保了 SIMT 程序的可移植性，而 CUDA Tile IR 则通过原生支持基于瓦片的程序扩展了平台。这是 NVIDIA 对 Triton 抢占市场份额的直接回应。

## 近期版本放弃的内容（与你的硬件相关）

CUDA 13.x 提高了门槛：CUDA Toolkit 13.0 移除了对 Maxwell、Pascal 和 Volta 的离线编译和库支持——你仍然可以使用 12.x 工具包为它们构建，但更新的工具包无法再针对它们。CUDA 13.0 支持 Turing 到 Blackwell，包括 GB200/GB300 NVL72 和 RTX 5000 系列。Linux 上的驱动最低要求提升至 ≥580.65.06；对于 CUDA 12，你应保持在 525 到 580 之间。

你的 **RTX 4070（Ada，SM 8.9）** 在 12.x 和 13.x 上都完全受支持——Ada 舒适地处于 Turing 到 Blackwell 的窗口内。你的 **MI300X** 则完全是另一套技术栈（ROCm/HIP），但概念上的演变是平行的：张量等效的矩阵核心、低精度、异步拷贝。

## 主线

如果用一句话概括 20 年的发展：**CUDA 最初暴露原始的 SIMT 控制，然后逐步增加专用的矩阵乘法硬件（张量核心）和喂饱它的异步内存机制，同时稳步降低精度——现在又增加了更高层次的瓦片抽象，让你不再手动编写喂数据逻辑。** Triton 和 cuTile 押注的是同一件事：大多数为 ML 编写 GPU 内核的人希望以瓦片而非线程的思维来工作。

对于你的发展路径，关键点在于：理解**内存层次结构 + 异步拷贝**（这是 FlashAttention 快速运行的 80% 原因），理解**张量核心瓦片形状**（为什么矩阵乘法希望维度是 16/64 的倍数），并关注 **cuTile 与 Triton**——这是内核编写的发展方向。

参考文献：

- [CUDA Toolkit 13.0 的新增重要内容 — NVIDIA](https://developer.nvidia.com/blog/whats-new-and-important-in-cuda-toolkit-13-0/)
- [NVIDIA CUDA 13.1 通过 CUDA Tile 赋能下一代 GPU 编程 — NVIDIA](https://developer.nvidia.com/blog/nvidia-cuda-13-1-powers-next-gen-gpu-programming-with-nvidia-cuda-tile-and-performance-gains/)
- [NVIDIA 随 CUDA 13.1 发布 CUDA Tile — TechPowerUp](https://www.techpowerup.com/343740/nvidia-announces-cuda-tile-with-cuda-13-1)
- [NVIDIA CUDA Toolkit 13.0 已发布 — ServeTheHome](https://www.servethehome.com/nvidia-cuda-toolkit-13-0-is-out/)
- [CUDA Toolkit 13.0 发布说明 — NVIDIA](https://docs.nvidia.com/cuda/archive/13.0.3/cuda-toolkit-release-notes/index.html)