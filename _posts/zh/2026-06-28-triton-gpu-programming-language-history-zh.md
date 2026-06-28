---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Triton GPU编程语言历史
translated: true
type: note
---

问题：请介绍一下 GPU 编程语言 Triton 的历史。

回答：

Triton 最初是 **Philippe Tillet 在哈佛大学的博士工作**。基础论文为 *《Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations》*（MAPL 2019）。核心论点：GPU 内核编写处于一个尴尬的极端——CUDA 提供了控制力，但迫使你手动管理共享内存、内存合并和 warp 级调度；高层 DSL 隐藏了硬件细节，但无法表达新颖操作。Triton 的赌注在于一种 **基于 tile 的抽象**：你以数据块（tiles）为单位进行编程，编译器负责处理 tile 内部的内存布局、合并和 SM 调度。

大致时间线：

- **2019** — MAPL 论文。最初实现是一个独立的 C++ 编译器，带有自定义 IR，LLVM 后端目标 PTX。Tillet 是唯一作者。
- **2020** — Tillet 加入 OpenAI。Triton 被重写，带有 Python 嵌入的前端（`@triton.jit` 装饰器）。这是转折点——它从研究原型变成了机器学习工程师实际使用的工具，因为你用类似 Python 的代码编写内核，却能获得 CUDA 级的性能。
- **2021** — OpenAI 通过博文 *《Introducing Triton》* 将其开源。头号演示：一个融合 softmax 和 matmul 的内核，用更少的代码行数媲美 cuBLAS/cuDNN，且无需 CUDA 专业知识。
- **2022–2023** — 编译器在 **MLIR** 之上重新架构（替代了专有 IR）。这在架构上是重大变革——MLIR 的方言系统让 Triton 能够通过逐步抽象层次进行降级（Triton dialect → TritonGPU dialect → LLVM/PTX），并使得多后端支持变得可行。
- **2023** — **PyTorch 2.0 发布 `torch.compile`**，其 GPU 后端 **TorchInductor 生成 Triton 代码**。这使 Triton 从一个小众工具变成了基础设施——突然之间，每个 `torch.compile` 用户都在运行 Triton 内核，无论他们是否知晓。
- **2023–2024** — 后端扩展出 NVIDIA 范围：**AMD（ROCm/HIP）** 支持成熟，Intel GPU 后端，以及 CPU 实验。这对你尤为重要，因为 MI300X 的出现——Triton-on-ROCm 是让你的内核在 RTX 4070 和 MI300X 之间可移植、无需重写 CUDA 的路径。

值得内化的编程模型洞察：在 CUDA 中，你以 **线程** 粒度进行推理（每个线程计算一个元素，你编排网格）。在 Triton 中，你以 **块/tile** 粒度进行推理——单个 `@triton.jit`“程序实例”操作整个 tile，你通过 `tl.load`/`tl.store` 加上掩码来表达加载/存储范围。编译器决定线程映射。这就是为什么一个 Triton 的 matmul 只需约 30 行代码，而一个具有竞争力的 CUDA 版本需要数百行——你把 warp 级调度和共享内存分阶段的工作委托给了编译器。

一个最小化的内核来锚定心智模型——向量加法：

```python
import triton
import triton.language as tl
import torch

@triton.jit
def add_kernel(x_ptr, y_ptr, out_ptr, n, BLOCK: tl.constexpr):
    pid = tl.program_id(0)                      # 我负责哪个 tile
    offs = pid * BLOCK + tl.arange(0, BLOCK)    # 这个 tile 的元素索引
    mask = offs < n                             # 保护尾部未对齐部分
    x = tl.load(x_ptr + offs, mask=mask)
    y = tl.load(y_ptr + offs, mask=mask)
    tl.store(out_ptr + offs, x + y, mask=mask)

def add(x, y):
    out = torch.empty_like(x)
    n = x.numel()
    grid = lambda meta: (triton.cdiv(n, meta["BLOCK"]),)
    add_kernel[grid](x, y, out, n, BLOCK=1024)
    return out
```

注意缺失了什么：没有 `threadIdx`，没有 `__shared__`，没有显式的内存合并。`tl.arange` 配合 `BLOCK` 和 `mask` 就是整个分块的故事。`BLOCK: tl.constexpr` 是编译期特化的参数——Triton 会对其进行自动调优。

如今 Triton 的地位：当 cuBLAS/cuDNN/FlashAttention 尚未覆盖你需要的操作时，Triton 是机器学习中事实上的 **内核编写层**。FlashAttention-2/3、融合 MoE 内核（与你对 DeepSeek v4 MoE 的探索直接相关——专家路由的 gather/scatter 和 grouped GEMM 正是人们在 Triton 中编写的那种操作），以及现代训练栈中大多数自定义融合操作，都是 Triton 或与 Triton 相关的。它之所以战胜“直接写 CUDA”的战略原因在于：它将内核逻辑与硬件特定的调度解耦，因此同一个内核可以在不同 SM 世代乃至不同供应商之间自动调优。

对于你个人的发展轨迹而言：Triton 是目前最具杠杆效应的 GPU 技能，因为（1）它是 `torch.compile` 的基础，（2）它是无需 CUDA 的 NVIDIA 锁定就能编写 MI300X 内核的实用路径，（3）用 Triton 编写融合注意力或 MoE 内核，能让你学到内存层级推理（SRAM 分块、重新计算与物化），这种推理可以迁移到理解 *为什么* FlashAttention 在数学层面有效。

参考文献：

- [Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations (Tillet et al., MAPL 2019)](https://www.eecs.harvard.edu/~htk/publication/2019-mapl-tillet-kung-cox.pdf)
- [Introducing Triton (OpenAI, 2021)](https://openai.com/index/triton/)
- [Triton GitHub repository](https://github.com/triton-lang/triton)
- [Triton tutorials (official docs)](https://triton-lang.org/main/getting-started/tutorials/index.html)

我根据已有信息而非搜索给出了这段历史，因此具体日期请视为近似值——特别是 MLIR 重写和 ROCm 成熟的时间线在多个版本间有所变化。如果你需要，我可以拉取精确的逐版本更新日志或 AMD 后端的当前状态。