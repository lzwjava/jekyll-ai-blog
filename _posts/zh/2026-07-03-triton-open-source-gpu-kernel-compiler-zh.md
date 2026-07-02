---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Triton: 开源GPU内核编译器'
translated: true
type: note
---

以下是 Triton 的介绍：

**Triton**（当前检出版本 v3.8.0）是一个用于编写高性能 GPU 内核的开源语言与编译器。它由 OpenAI 创建（现归属于 triton-lang 组织），位于 CUDA 与 Python 之间——你使用类似 Python 的语法编写内核，编译器会生成优化的 GPU 机器码（NVIDIA 为 PTX，AMD 为 AMDGCN）。

**核心理念：** 不同于在 CUDA C++ 中手动管理线程、共享内存和同步，Triton 让你在 **tile** 级别表达计算。你声明指针块，编译器为你处理分块、内存合并和寄存器分配。

**架构（仓库内容）：**

1. **前端（Python）** — `python/triton/language/core.py` 定义了 DSL：`tl.load`、`tl.store`、`tl.dot`、`tl.program_id`、`tensor` 操作。`@triton.jit` 装饰器将 Python 函数 JIT 编译为 GPU 内核。

2. **编译器（基于 MLIR，C++）** — 核心工作：
   - `lib/Dialect/Triton/` — Triton IR 方言（高级 tile 操作）
   - `lib/Dialect/TritonGPU/` — TritonGPU IR（GPU 特定的布局/调度）
   - `lib/Conversion/TritonToTritonGPU/` — 将 tile 降级为 GPU 特定操作
   - `lib/Conversion/TritonGPUToLLVM/` — 降级为 LLVM IR → PTX/AMDGCN

3. **GPU 后端** — `third_party/nvidia/`（NVIDIA SM80+、WGMMA、张量内存）和 `third_party/amd/`（ROCm、MFMA、WMMA）

4. **运行时** — `python/triton/runtime/` — JIT 编译、自动调优、缓存、内核启动

5. **Proton** — `third_party/proton/` — GPU 性能分析器/诊断工具

6. **Gluon** — `python/triton/experimental/gluon/` — 实验性的低级 DSL，用于细粒度内存布局控制

**你实际编写的代码：**

```python
import triton
import triton.language as tl

@triton.jit
def add_kernel(X, Y, Z, N, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offsets = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offsets < N
    x = tl.load(X + offsets, mask=mask)
    y = tl.load(Y + offsets, mask=mask)
    tl.store(Z + offsets, x + y, mask=mask)
```

这段代码会编译为优化的 PTX，而你无需接触共享内存、线程束调度或内存合并逻辑。

**为什么这对你的职业路径重要：** Triton 是连接 Python 级别 ML 代码与 GPU 硬件的桥梁。理解编译器流水线（TTIR → TTGIR → LLVM IR → PTX）正是区分 ML 工程师与 AI 工程师所需的那种深度 AI 基础设施知识。它也是 Karpathy 式第一性原理思维与真实硬件的交汇点——你需要理解内存层次结构、线程束级原语和 GPU 架构，才能编写出优秀的 Triton 内核。
