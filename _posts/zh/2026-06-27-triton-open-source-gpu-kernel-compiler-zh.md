---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Triton：开源GPU内核编译器
translated: true
type: note
---

这是Triton的介绍：

**Triton**（你当前版本为v3.8.0）是一个开源的语言+编译器，用于编写高性能的GPU内核。由OpenAI创建（现属于triton-lang组织），它介于CUDA和Python之间——你可以用类似Python的语法编写内核，编译器会生成优化的GPU机器码（NVIDIA的PTX，AMD的AMDGCN）。

**核心思想：** 与CUDA C++中手动管理线程、共享内存和同步不同，Triton让你在*tile*级别表达计算。你声明指针块，编译器为你处理分块、内存合并和寄存器分配。

**架构（仓库内容）：**

1. **前端（Python）** — `python/triton/language/core.py`定义了DSL：`tl.load`、`tl.store`、`tl.dot`、`tl.program_id`、`tensor`操作。`@triton.jit`装饰器将Python函数JIT编译成GPU内核。

2. **编译器（基于MLIR，C++）** — 核心部分：
   - `lib/Dialect/Triton/` — Triton IR方言（高层tile操作）
   - `lib/Dialect/TritonGPU/` — TritonGPU IR（GPU特定的布局/调度）
   - `lib/Conversion/TritonToTritonGPU/` — 将tile降级为GPU特定操作
   - `lib/Conversion/TritonGPUToLLVM/` — 降级为LLVM IR → PTX/AMDGCN

3. **GPU后端** — `third_party/nvidia/`（NVIDIA SM80+，WGMMA，张量内存）和`third_party/amd/`（ROCm，MFMA，WMMA）

4. **运行时** — `python/triton/runtime/` — JIT编译、自动调优、缓存、内核启动

5. **Proton** — `third_party/proton/` — GPU性能分析/诊断工具

6. **Gluon** — `python/triton/experimental/gluon/` — 实验性的底层DSL，用于细粒度的内存布局控制

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

这段代码会编译成优化的PTX，而你无需接触共享内存、warp调度或内存合并逻辑。

**为什么这对你的发展路径很重要：** Triton是连接Python级ML代码和GPU硬件的*桥梁*。理解编译器流水线（TTIR → TTGIR → LLVM IR → PTX）正是区分ML工程师和AI工程师所需的深层AI基础设施知识。这也是Karpathy式第一性原理思维与真实硬件相遇的地方——你需要理解内存层次结构、warp级原语和GPU架构才能编写优秀的Triton内核。