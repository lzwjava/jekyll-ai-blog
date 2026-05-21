---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源与闭源AI硬件
translated: true
type: note
---

**问题：** 我正在深入探索开源芯片软件（AMD ROCm 作为开源 CUDA 替代方案）。我想了解 AI 价值链中开源与闭源之间的差距。接下来我应该了解什么？

**回答：**

直觉不错。下面是一张地图——从你目前的位置到真正有意思的地方。

## AI 价值链：开源与闭源的差距（真实评估）

| 层级 | 开源 | 闭源 | 差距 |
|---|---|---|---|
| **ML 框架** | PyTorch, JAX | — | 基本闭合。PyTorch 就是标准 |
| **编译器/IR** | MLIR, XLA, Triton | cuDNN 内部实现 | 中等 — Triton 正在快速缩小差距 |
| **运行时** | ROCm HIP, oneAPI | CUDA 运行时 | 中等 — ROCm 约完成 85% |
| **内核库** | rocBLAS, MIOpen | cuBLAS, cuDNN | 显著 — NVIDIA 性能仍占优 |
| **硬件微架构** | RISC-V (VexRiscV, CVA6) | NVIDIA SM 设计 | **巨大** — 微架构文档仍为专有 |
| **驱动** | `amdgpu`（内核内） | NVIDIA 开源内核（部分） | AMD 实际在此处领先 |

**结论：** 软件栈差距是可填补的。硬件微架构差距才是 NVIDIA 真正的护城河。

---

## 接下来实际应该学什么（按顺序）

### 1. HIP + ROCm 内部机制（你目前所在位置）

```bash
# 确认你的 ROCm 安装能识别 GPU
rocminfo | grep -A5 "Agent 2"
hipcc --version

# HIP 中的 Hello triangle
cat << 'EOF' > vec_add.hip
#include <hip/hip_runtime.h>
#include <stdio.h>

__global__ void vecAdd(float* a, float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}

int main() {
    int n = 1 << 20;
    float *d_a, *d_b, *d_c;
    hipMalloc(&d_a, n*4); hipMalloc(&d_b, n*4); hipMalloc(&d_c, n*4);
    hipLaunchKernelGGL(vecAdd, dim3(n/256), dim3(256), 0, 0, d_a, d_b, d_c, n);
    hipFree(d_a); hipFree(d_b); hipFree(d_c);
}
EOF
hipcc vec_add.hip -o vec_add && ./vec_add
```

HIP → CUDA 翻译约 95% 是机械性的。`hipify-clang` 可自动将 CUDA 转换为 HIP。这就是 ROCm 启动的方式。

---

### 2. Triton —— 真正的开源转折点

这才是关键所在。Triton 让你可以用 Python 编写 GPU 内核，这些内核**能同时编译为 CUDA PTX 和 AMD GCN/RDNA**。OpenAI 将其开源，现在它已进入 PyTorch 核心。

```python
import triton
import triton.language as tl

@triton.jit
def matmul_kernel(A, B, C, M, N, K, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    # tile over M dimension
    rm = pid * BLOCK + tl.arange(0, BLOCK)
    rn = tl.arange(0, BLOCK)
    rk = tl.arange(0, BLOCK)
    acc = tl.zeros((BLOCK, BLOCK), dtype=tl.float32)
    for k in range(0, K, BLOCK):
        a = tl.load(A + rm[:, None]*K + (rk[None,:]+k))
        b = tl.load(B + (rk[:,None]+k)*N + rn[None,:])
        acc += tl.dot(a, b)
    tl.store(C + rm[:,None]*N + rn[None,:], acc)
```

**为什么这很重要：** Flash Attention 2（使 LLM 推理变快的内核）就是用 Triton 编写的。ROCm 和 CUDA 之间的差距在这里缩小得最快。

---

### 3. MLIR + 编译器栈（开源正在获胜的地方）

```
PyTorch/JAX
    ↓ torch.compile / XLA
  Triton IR / StableHLO
    ↓ MLIR passes
  LLVM IR
    ↓
  PTX (NVIDIA) / GCN ISA (AMD) / RISC-V (未来)
```

MLIR 是 Google/LLVM 在统一编译器 IR 上的赌注。每个主要的芯片初创公司（Tenstorrent, Groq, Cerebras）都瞄准 MLIR。**这一层是开源实际领先的地方。**

```bash
# 玩玩 MLIR
pip install mlir-python-bindings
# 或者从源码构建以获得完全控制
git clone https://github.com/llvm/llvm-project
cd llvm-project && cmake -DLLVM_ENABLE_PROJECTS="mlir" ...
```

---

### 4. 开源硬件 —— RISC-V GPU 实验

这是前沿领域。实际的开源 GPU 核心：

- **Vortex** —— RISC-V GPGPU，运行 OpenCL，已流片至 FPGA
  ```bash
  git clone https://github.com/vortexgpgpu/vortex
  # 在 Verilator 仿真或实际 FPGA 上运行
  ```
- **NaxRiscv** —— 乱序执行 RISC-V，严肃的微架构
- **NVDLA**（NVIDIA 开源了其 DLA）—— 推理加速器 RTL

差距：开源 RTL 存在，但**工艺节点访问**（台积电 4nm）才是真正的护城河。软件是可解决的。芯片制造访问则不行。

---

## 真正的护城河地图

```
cuDNN 融合内核（手工调优的汇编）                     ← 最难复制
CUDA PTX ISA 稳定性 + 生态系统锁定                    ← 15 年软件积累
NVLink / NVSwitch 拓扑                              ← 硬件，需要 $$$$
HBM 分配 + 供应商关系                                ← 供应链
```

ROCm 弥合了软件差距。没有人能在没有晶圆厂的情况下弥合 HBM/NVLink 差距。

---

## 你的学习路径

```
第 1-2 周：  HIP 内核，用 hipify 处理现有 CUDA 代码
第 3-4 周：  Triton 内核编写 —— 重新实现 softmax, layernorm
第 5-6 周：  torch.compile 内部机制，Dynamo/Inductor
第 7-8 周：  MLIR 基础 —— 编写一个简单的 lowering pass
第 3 个月+：  在 Verilator 上运行 Vortex RISC-V GPU，理解 GCN ISA
```

**需要加星标的关键仓库：**

```bash
# 核心
https://github.com/ROCm/ROCm
https://github.com/triton-lang/triton
https://github.com/llvm/llvm-project          # MLIR 在此

# 学习用
https://github.com/tinygrad/tinygrad          # George Hotz 的以 ROCm 为先的框架
https://github.com/vortexgpgpu/vortex         # 开源 RISC-V GPU
https://github.com/openxla/xla               # 谷歌的编译器
```

**tinygrad 是你最好的老师** —— 它是一个完整的 ML 框架，运行在 ROCm 上，代码可读性强，George 明确构建它来理解和对抗 CUDA 锁定。阅读 `runtime/` 目录。

---

## 总结

开源软件栈（ROCm + Triton + MLIR + PyTorch）对于 **90% 的工作负载已经足够好**，并且正在快速追赶。剩下的差距在于手工调优的内核库（cuDNN）和硬件拓扑（NVLink）。如果你要深入研究，Triton + tinygrad 是理解真正工作在何处发生的最快路径。

**参考文献：**

- [ROCm GitHub](https://github.com/ROCm/ROCm)
- [Triton Lang](https://github.com/triton-lang/triton)
- [tinygrad — 以 ROCm 为先的 ML 框架](https://github.com/tinygrad/tinygrad)
- [Vortex RISC-V GPGPU](https://github.com/vortexgpgpu/vortex)
- [MLIR in LLVM](https://mlir.llvm.org/)
- [Flash Attention in Triton](https://github.com/Dao-AILab/flash-attention)