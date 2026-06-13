---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TileLang：Python风格的GPU内核领域特定语言
translated: true
type: note
---

**问题：** 什么是 `tile-ai/tilelang`？

**回答：**

TileLang 是一种 **Python 风格的 DSL，用于编写高性能 GPU/CPU 内核**，基于 TVM 作为编译器后端。可以将其视为介于编写原始 CUDA/HIP（繁琐、不可移植）和使用 cuBLAS/CUTLASS（不透明、不灵活）之间的"中间地带"——既能获得接近底层的控制力，又能享受 Python 的易用性。

**6.5k 星标，597 个复刻**——该项目正在获得切实的发展势头。

---

### 它解决的问题

手工编写如 FlashAttention、GEMM 或 MLA 的 CUDA 内核需要处理：

- 手工管理 tile/block/thread 层级
- 共享内存布局、bank 冲突
- 异步拷贝、流水线（Hopper 上的 TMA）
- warp 级矩阵乘法内在函数（WMMA/WGMMA）

TileLang 抽象了所有这些内容，同时仍允许您表达关键的算法决策（tile 大小、swizzle、流水线阶段）。

---

### 核心抽象

```python
with T.Kernel(T.ceildiv(N, block_N), T.ceildiv(M, block_M), threads=128) as (bx, by):
    A_shared = T.alloc_shared((block_M, block_K), dtype)   # 共享内存
    C_local  = T.alloc_fragment((block_M, block_N), accum_dtype)  # 寄存器 tile

    T.clear(C_local)

    for ko in T.Pipelined(T.ceildiv(K, block_K), num_stages=3):  # 异步流水线
        T.copy(A[by * block_M, ko * block_K], A_shared)  # 并行化 gmem->smem
        T.copy(B[ko * block_K, bx * block_N], B_shared)
        T.gemm(A_shared, B_shared, C_local)  # 分派到 CuTe/HIP 内在函数

    T.copy(C_local, C[by * block_M, bx * block_N])
```

关键原语：

- `T.Kernel(...)` — 网格启动
- `T.alloc_shared` / `T.alloc_fragment` — 共享内存和寄存器 tile
- `T.Pipelined(...)` — 带 `num_stages` 的软件流水线
- `T.copy(...)` — 并行化异步拷贝（映射到 Hopper 上的 TMA）
- `T.gemm(...)` — tile 级矩阵乘法（分派到 WGMMA / WMMA / MatrixCore）
- `T.Parallel(...)` — 对 tile 执行逐元素操作
- `T.use_swizzle(panel_size=10)` — L2 缓存 swizzle

---

### 为什么它对您特别重要

您曾在 **MI300X** 上训练过 GPT-2——TileLang 明确支持 MI300X，提供 `Async Copy` 支持，甚至拥有 **AMD MI300X 的 FlashMLA 实现**，可媲美手工优化的汇编代码（Aiter）。如果您想为训练任务编写自定义注意力或 MoE 路由内核，这将非常实用。

DeepSeek MLA 解码内核仅需 **80 行 Python 代码**，性能即可与 H100 上的 FlashMLA 相匹配——这正是该 DSL 所追求的编程效率与性能之间的平衡。

---

### 技术栈

- **编译器后端：** Apache TVM（使用大量修改的分支作为子模块）
- **目标平台：** CUDA（NVIDIA H100/A100/V100/4090/3090）、HIP（AMD MI250/MI300X）、Apple Metal、WebGPU、华为昇腾 NPU
- **新后端（2025 年 12 月）：** CuTe DSL — 编译为 NVIDIA CUTLASS CuTe
- **SMT 集成：** 将 Z3 定理证明器嵌入 TVM Arith，用于符号正确性验证
- **编程语言：** 50% Python，48% C++

---

### TileLang 与其他方案对比

| | TileLang | Triton | CUTLASS/CuTe | 原始 CUDA |
|---|---|---|---|---|
| 抽象级别 | Tile | Block/warp | 线程块 | 线程 |
| 可移植性 | CUDA+HIP+Metal | 主要是 CUDA | 仅 CUDA | 仅 CUDA |
| 异步流水线控制 | ✅ 显式 | ✅ | ✅ | 手动 |
| AMD 支持 | ✅ MI300X | 部分 | ❌ | HIP |
| Python 风格 | ✅ | ✅ | ❌ | ❌ |

与 Triton 的主要区别：TileLang 为您提供 **显式的共享内存布局控制和每个线程的操作**（对去量化 GEMM 至关重要），而 Triton 则将其抽象化。它还被用作 **Microsoft BitBLAS** 和 **AttentionEngine** 的后端。

---

### 在您的 RTX 4070 上快速尝试

```bash
pip install tilelang
```

然后运行 README 中的 GEMM 示例——它应该能在 CUDA 上干净地进行 JIT 编译和基准测试。

对于 AMD Dev Cloud 上的 MI300X：

```bash
pip install tilelang -f https://tile-ai.github.io/whl/nightly  # 使用 nightly 版本以获取最新的 ROCm 修复
```

---

**参考资料：**

- [tile-ai/tilelang GitHub](https://github.com/tile-ai/tilelang)
- [TileLang Puzzles（学习练习）](https://github.com/tile-ai/tilelang-puzzles)
- [FlashMLA AMD MI300X 示例](https://github.com/tile-ai/tilelang/blob/main/examples/deepseek_mla/amd/README.md)
- [Microsoft BitBLAS（使用 TileLang）](https://github.com/microsoft/BitBLAS)
