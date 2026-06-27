---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SM80+计算能力含义
translated: true
type: note
---

问题：NVIDIA SM80+ 是什么意思？SM 版本像苹果的型号（如 A1728）吗？

回答：

不——这恰恰相反，它不是随意的营销或型号编号。SM 代表 **Streaming Multiprocessor 架构版本**，该数字编码了 GPU 的**计算能力**。这是一个结构化的、有序的版本号（主版本.次版本），而不是像苹果 `A1728` 那样的 SKU 标识符。

`SM80` = `sm_80` = 计算能力 **8.0**。编码格式为 `SM<主版本><次版本>`：

- `sm_70` → 7.0 → Volta (V100)
- `sm_75` → 7.5 → Turing (RTX 20xx, T4)
- `sm_80` → 8.0 → Ampere **数据中心** (A100)
- `sm_86` → 8.6 → Ampere **消费级** (RTX 30xx，你的 RTX 4070 实际上是 `sm_89`)
- `sm_89` → 8.9 → Ada Lovelace (RTX 40xx — **你的 4070**)
- `sm_90` → 9.0 → Hopper (H100)
- `sm_100` → 10.0 → Blackwell (B100/B200)

你的 MI300X 是 AMD 的，因此它使用 `gfx942` (CDNA3) —— 一个完全独立的 ISA 命名空间。

**“SM80+” 意味着计算能力 ≥ 8.0。** 它是一个特性门槛。标记为 SM80+ 的代码或内核需要 Ampere 中引入的硬件特性，其中最重要的是：

- **`cp.async`** —— 异步全局→共享内存复制（绕过寄存器）。这是使 FlashAttention 和现代 GEMM 流水线加速的关键。
- **第三代 Tensor Core**，支持 `bf16`、`tf32` 和异步 `mma` 指令。
- **更大的共享内存**（A100 上每个 SM 最高 164 KB）。
- **异步屏障**（`mbarrier`）。

这就是为什么许多 Triton/CUDA 内核（FlashAttention-2、许多融合内核）会注明“需要 SM80+” —— 它们会生成 Turing 上根本不存在的 `cp.async` PTX 指令。

与苹果型号编号的关键区别在于：这里的大小顺序**具有语义含义且单调递增**。`sm_89 > sm_80` 告诉你 Ada 是 Ampere 特性的超集。而 `A1728` 与 `A1864` 之间什么也看不出来——它们只是注册 ID。

两个实际中的微妙之处：

1. **更高的编号 ≠ 严格的超集。** `sm_86`/`sm_89`（消费级）比 `sm_80`（A100）**更新**，但 **Tensor Core FLOPs 更少，共享内存也更小**。次版本号有时会去掉仅数据中心才有的特性。因此“SM80+”保护的是一个特性**基线**，而不是性能层级。

2. **二进制 vs PTX。** 编译 CUDA 时，你可以指定真实架构（`-arch=sm_89`，生成 SASS 二进制），也可以指定虚拟架构（`-arch=compute_80`，生成 PTX，然后通过 JIT 向前兼容新 GPU）。PyTorch 以 fat binary 形式发布，包含 `TORCH_CUDA_ARCH_LIST="8.0;8.6;8.9;9.0"`。

在你的设备上快速检查：

```bash
# 你的 RTX 4070 → 应该输出 8.9
nvidia-smi --query-gpu=compute_cap --format=csv,noheader

# 在 Python 中
python -c "import torch; print(torch.cuda.get_device_capability())"  # (8, 9)

# AMD MI300X — 完全不同的命名空间
rocminfo | grep gfx   # gfx942
```

所以：SM80 与苹果型号编号的关系，就像**语义化版本号与序列号的关系**。这个数字*就是*能力规格本身。
