---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA与张量核心详解
translated: true
type: note
---

**问题：** RTX 4070 这类 GPU 上的 CUDA 核心与 Tensor 核心有什么区别？

**答案：**

它们是每个流式多处理器（SM）内部物理上不同的执行单元，针对不同粒度的数学运算构建：

- **CUDA 核心** = 标量 FP32/INT32 ALU。一个线程每时钟周期执行一次融合乘加（FMA）：`d = a * b + c`，操作对象为*标量*。
- **Tensor 核心** = 矩阵乘积累加（MMA）单元。整个*warp*（32个线程）协作执行一条指令，对小的*矩阵块*（例如 FP16 下的 16×16×16）计算 `D = A @ B + C`。

**在您的 RTX 4070（AD104，Ada 架构）上的布局：**

```
46 个 SM
├── 128 个 CUDA 核心 / SM  → 总共 5,888 个
└── 4 个 Tensor 核心 / SM  → 总共 184 个（第 4 代）
```

**为什么 Tensor 核心数量少 32 倍却快约 4 倍**

在约 2.48 GHz 加速频率下的吞吐量计算：

```python
# CUDA 核心：每个核心每时钟 1 次 FMA = 2 FLOPs
fp32 = 5888 * 2 * 2.48e9          # ≈ 29.2 TFLOPS

# Tensor 核心：每个核心每时钟约 256 次 FP16 FLOPs（密集）
fp16_tc = 184 * 256 * 2.48e9      # ≈ 116.8 TFLOPS
```

每个 Tensor 核心包含一个硬连线的 FP16 乘法器网格加上一个加法树，因此一条指令完成了数百次标量 FMA 的工作。这和 CPU 上 AVX-512 对标量的技巧类似，但针对的是*矩阵*而非向量，且宽度高一个数量级。

**在指令集层次上的表现**

一个 CUDA 核心执行每线程的 SASS 指令，例如：

```
FFMA R4, R2, R3, R4 ;   // 一条标量 fp32 fma，一个线程
```

一个 Tensor 核心执行 warp 级的 PTX 指令，例如：

```
mma.sync.aligned.m16n8k16.row.col.f32.f16.f16.f32
    {d0,d1,d2,d3}, {a0,a1,a2,a3}, {b0,b1}, {c0,c1,c2,c3};
```

单条 `mma.sync` 完成一次 16×8×16 矩阵乘法——2048 次乘加——矩阵块的碎片分散在 32 个线程的寄存器中。“线程”不再是独立的标量通道，而是成为集体矩阵操作的寄存器存储。

**直接编程（WMMA API）：**

```cpp
#include <mma.h>
using namespace nvcuda::wmma;

__global__ void tc_gemm(half *A, half *B, float *C) {
    fragment<matrix_a, 16, 16, 16, half, row_major> a;
    fragment<matrix_b, 16, 16, 16, half, col_major> b;
    fragment<accumulator, 16, 16, 16, float> acc;

    fill_fragment(acc, 0.0f);
    load_matrix_sync(a, A, 16);
    load_matrix_sync(b, B, 16);
    mma_sync(acc, a, b, acc);          // 命中 Tensor 核心
    store_matrix_sync(C, acc, 16, mem_row_major);
}
```

实际上你不需要自己写这些——cuBLAS/cuDNN/CUTLASS 会处理，PyTorch 则通过它们路由。

**在 4070 工作站上亲自验证：**

```python
import torch, time

x = torch.randn(4096, 4096, device='cuda')

def bench(a, b, n=50):
    torch.cuda.synchronize(); t = time.time()
    for _ in range(n): a @ b
    torch.cuda.synchronize()
    return 2 * 4096**3 * n / (time.time() - t) / 1e12

print(f"fp32 (CUDA cores):   {bench(x, x):.1f} TFLOPS")
h = x.half()
print(f"fp16 (tensor cores): {bench(h, h):.1f} TFLOPS")
```

预期结果大约为 ~25 对比 ~90+ TFLOPS（由于内存带宽限制，你无法达到峰值——AD104 的 504 GB/s 在此规模下往往是实际瓶颈）。

**关键限制——Tensor 核心只能做矩阵乘法。** Transformer 前向传播中的其他一切——softmax、LayerNorm、GELU、残差相加、嵌入查找——都在 CUDA 核心上运行。这就是内核融合（如 FlashAttention 将 softmax 融合进 MMA 流水线）如此重要的原因：一旦矩阵乘法交由 Tensor 核心处理，瓶颈就变成了 CUDA 核心上的逐元素操作以及它们之间的内存往返。

一个与您 nanoGPT 训练相关的细微差别：在 GeForce 显卡上（与 H100/MI300X 级别不同），FP16 带 FP32 累加的运行速度是*一半*的 FP16 带 FP16 累加。PyTorch AMP 为了稳定性使用 FP32 累加，因此您在 4070 上的有效 Tensor 核心峰值约为 ~58 TFLOPS，而不是 ~117。BF16 有相同特性。而您的 MI300X 没有这种限制——它的 1216 个矩阵核心可以全速进行 FP16/BF16 带 FP32 累加（约 1300 TFLOPS 密集）。