---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解开源与闭源AI芯片软件
translated: true
type: note
---

**问题：** 我正准备深入研究开源芯片软件（AMD ROCm 作为开源的 CUDA 替代品）。我想了解 AI 价值链中开源与闭源的差距。接下来我应该了解什么？

**回答：**

好直觉。以下是该领域的真实地图，以及一条具体的学习路径。

---

## AI 芯片软件栈中的开源与闭源差距

```
硬件             AMD（开源）          NVIDIA（闭源）
─────────────────────────────────────────────────────
ISA              GCN/RDNA/CDNA       SM 架构（仅文档）
驱动             amdgpu（内核内）    nvidia.ko（二进制 blob）
计算运行时       ROCm / HIP          CUDA
数学库           rocBLAS/rocFFT      cuBLAS/cuFFT
机器学习原语     MIOpen              cuDNN
编译器           LLVM/AMDGPU         nvcc（ptxas 闭源）
PTX 等价物       AMDGPU ISA（开源）   PTX → SASS（SASS 闭源）
```

**关键洞察：** NVIDIA 真正的护城河不是 CUDA 语言本身，而是 **cuDNN + NCCL + 分析器生态系统**。ROCm 在纸面上匹配，但在以下方面落后：

- 非方阵矩阵乘法（实际工作负载）上的 `hipBLAS` 性能
- 大规模场景下的多节点 `RCCL` 与 `NCCL`
- 分析器（rocprof 与 Nsight——Nsight 明显胜出）

---

## 接下来按顺序需要掌握的内容

### 1. HIP——可移植层

HIP 是 ROCm 的 CUDA 兼容 API。大多数 CUDA 代码可通过 `hipify` 移植：

```bash
hipify-clang my_kernel.cu -o my_kernel.hip.cpp
```

核心心智模型：HIP 调用在 API 级别与 CUDA 调用一一对应。在 AMD 上，它通过 LLVM → AMDGPU 后端编译。在 NVIDIA 上，它实际上直接编译为 CUDA。**同一份源代码，两个目标。** 这才是真正的价值——一次编写，到处运行。

```cpp
// HIP 内核——语法与 CUDA 完全相同
__global__ void saxpy(float* y, float* x, float a, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = a * x[i] + y[i];
}

// 启动——hipLaunchKernelGGL 或 <<<>>> 语法均可
hipLaunchKernelGGL(saxpy, dim3(n/256), dim3(256), 0, 0, d_y, d_x, a, n);
```

### 2. 编译器流水线（真正的差距所在）

```
CUDA 路径：   .cu → nvcc → PTX → SASS（此处为闭源优化）
ROCm 路径：   .hip → clang → LLVM IR → AMDGPU ISA（完全开源）
```

由于 AMD 的后端是上游 LLVM 的一部分，你实际上可以**阅读并修改编译器**。这是 NVIDIA 长期最担心的差距。拉取 LLVM AMDGPU 后端并阅读它：

```bash
git clone https://github.com/llvm/llvm-project
ls llvm/lib/Target/AMDGPU/
# GCNISelDAGToDAG.cpp —— 指令选择
# SIInstrInfo.cpp —— 指令定义
# AMDGPUTargetMachine.cpp —— 入口点
```

### 3. ROCm 上的 Triton——这是你深入理解的最快路径

Triton 可编译为 CUDA 和 ROCm。ROCm 后端现已可用于生产环境。编写 Triton 内核能让你了解位于裸 HIP/CUDA 之上的抽象层，而大多数实际机器学习工作现在都使用这一层：

```python
import triton
import triton.language as tl

@triton.jit
def matmul_kernel(A, B, C, M, N, K, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)
    rm = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    rn = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    rk = tl.arange(0, BLOCK_K)
    A_ptrs = A + rm[:, None] * K + rk[None, :]
    B_ptrs = B + rk[:, None] * N + rn[None, :]
    acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
    for k in range(0, K, BLOCK_K):
        a = tl.load(A_ptrs)
        b = tl.load(B_ptrs)
        acc += tl.dot(a, b)
        A_ptrs += BLOCK_K
        B_ptrs += BLOCK_K * N
    tl.store(C + rm[:, None] * N + rn[None, :], acc)
```

在 ROCm 上运行：`TRITON_ROCM_ISA_VERSION=gfx90a python matmul.py`

### 4. ROCm 性能分析——你的调试界面

```bash
# 基础内核分析
rocprof --stats python train.py

# 硬件计数器模式（类似 Nsight Compute）
rocprof --hip-trace --roctx-trace python train.py

# Omniperf——严肃工具（Nsight Compute 等价物）
pip install omniperf
omniperf profile -- python kernel.py
omniperf analyze -p workloads/kernel/
```

Omniperf 是开源的，能实际显示内存带宽利用率、缓存命中率、波前占用率——与 Nsight 在 NVIDIA 上显示的指标相同。

### 5. ROCm 上的 PyTorch——实用层

PyTorch 对 ROCm 的支持现在是一流的。内部它使用 HIP。有趣的是 `torch.compile`（inductor）如何为 CUDA 和 ROCm 生成不同的内核：

```python
import torch
# 检查 ROCm
print(torch.version.hip)  # 例如 '5.7.0'
print(torch.cuda.get_device_name(0))  # 显示 AMD GPU 名称

# torch.compile 在 ROCm 上工作
model = torch.compile(your_model)
```

ROCm 上的 inductor 后端生成 Triton 内核 → HIP → AMDGPU ISA。整个栈都是可审计的。

---

## 真实的差距评估

| 层 | NVIDIA | AMD ROCm | 差距 |
| --- | --- | --- | --- |
| 内核性能（矩阵乘） | 100% | MI300X 上约 85-95% | 快速缩小 |
| 多 GPU 通信 | NCCL（快速） | RCCL（接近） | 小 |
| 分析器 | Nsight（优秀） | Omniperf（良好） | 中等 |
| 生态系统/库 | 庞大 | 追赶中 | 仍然真实存在 |
| 编译器开放性 | 闭源 | 完全开源 | AMD 胜出 |
| 云端可用性 | 无处不在 | 有限 | NVIDIA 胜出 |

**MI300X 在内存带宽上实际上与 H100 有竞争力**（5.2 TB/s 对 3.35 TB/s）。对于大型模型的推理，AMD 在原始带宽上胜出。

---

## 你的具体下一步行动

```bash
# 1. 安装 ROCm（如果你有 AMD GPU 或使用云）
wget https://repo.radeon.com/amdgpu-install/6.1/ubuntu/jammy/amdgpu-install_6.1_all.deb
# 或者直接使用 Docker：rocm/pytorch:latest

# 2. 对你熟悉的 CUDA 内核运行 hipify
hipify-clang flash_attn_kernel.cu

# 3. 编写一个 Triton 内核，在两种平台上进行基准测试
# 4. 阅读 AMDGPU LLVM 后端
# 5. 使用 rocprof/omniperf 进行分析
```

**值得按顺序阅读的资源：**

- ROCm 文档：`rocm.docs.amd.com` —— HIP 编程指南
- `github.com/ROCm/HIP` —— 阅读 `include/hip/` 头文件
- `github.com/triton-lang/triton` —— `third_party/amd/` 后端
- `github.com/ROCm/omniperf` —— 理解哪些指标重要
- AMD CDNA2/3 白皮书 —— 理解你针对的硬件

这里的开源赌注是真实的。LLVM 后端是上游的，这意味着每一个编译器改进都会使 AMD 受益。从长远来看，这比任何短期的 CUDA 生态系统优势都更为重要。
