---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding Open vs Closed AI Chip Software
translated: false
type: note
---

**Question:** I'm about to dive into open-source chip software (AMD ROCm as the open-source CUDA equivalent). I want to understand the open vs closed source gap in the AI value chain. What should I know next?

**Answer:**

Good instinct. Here's the honest map of the landscape, then a concrete learning path.

---

## The Open vs Closed Gap in AI Chip Software Stack

```
Hardware         AMD (open)          NVIDIA (closed)
─────────────────────────────────────────────────────
ISA              GCN/RDNA/CDNA       SM architecture (docs only)
Driver           amdgpu (in kernel)  nvidia.ko (blob)
Compute runtime  ROCm / HIP          CUDA
Math libs        rocBLAS/rocFFT      cuBLAS/cuFFT
ML primitives    MIOpen              cuDNN
Compiler         LLVM/AMDGPU         nvcc (ptxas closed)
PTX equiv        AMDGPU ISA (open)   PTX → SASS (SASS closed)
```

**Key insight:** NVIDIA's real moat isn't CUDA the language — it's **cuDNN + NCCL + the profiler ecosystem**. ROCm matches on paper but lags on:
- `hipBLAS` performance on non-square matmuls (the real workload)
- Multi-node `RCCL` vs `NCCL` at scale
- Profiler (rocprof vs Nsight — Nsight wins badly)

---

## What to Grok Next, in Order

### 1. HIP — The Portability Layer

HIP is ROCm's CUDA-compatible API. Most CUDA code ports with `hipify`:

```bash
hipify-clang my_kernel.cu -o my_kernel.hip.cpp
```

Key mental model: HIP calls map 1:1 to CUDA calls at the API level. Under the hood on AMD it compiles through LLVM → AMDGPU backend. On NVIDIA it literally compiles as CUDA. **Same source, two targets.** This is the real value — write once.

```cpp
// HIP kernel — identical syntax to CUDA
__global__ void saxpy(float* y, float* x, float a, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) y[i] = a * x[i] + y[i];
}

// Launch — hipLaunchKernelGGL or <<<>>> syntax both work
hipLaunchKernelGGL(saxpy, dim3(n/256), dim3(256), 0, 0, d_y, d_x, a, n);
```

### 2. The Compiler Pipeline (Where the Real Gaps Are)

```
CUDA path:   .cu → nvcc → PTX → SASS (closed optimizations here)
ROCm path:   .hip → clang → LLVM IR → AMDGPU ISA (fully open)
```

Because AMD's backend is upstream LLVM, you can actually **read and modify the compiler.** This is the gap NVIDIA fears most long-term. Pull the LLVM AMDGPU backend and read it:

```bash
git clone https://github.com/llvm/llvm-project
ls llvm/lib/Target/AMDGPU/
# GCNISelDAGToDAG.cpp — instruction selection
# SIInstrInfo.cpp — instruction definitions
# AMDGPUTargetMachine.cpp — the entry point
```

### 3. Triton on ROCm — This is Your Fastest Path to Deep Understanding

Triton compiles to both CUDA and ROCm. The ROCm backend is now production-usable. Writing Triton kernels teaches you the abstraction layer that sits above raw HIP/CUDA and is what most real ML work uses now:

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

Run this on ROCm: `TRITON_ROCM_ISA_VERSION=gfx90a python matmul.py`

### 4. ROCm Profiling — Your Debugging Surface

```bash
# Basic kernel profiling
rocprof --stats python train.py

# Hardware counter mode (like Nsight Compute)
rocprof --hip-trace --roctx-trace python train.py

# Omniperf — the serious tool (Nsight Compute equivalent)
pip install omniperf
omniperf profile -- python kernel.py
omniperf analyze -p workloads/kernel/
```

Omniperf is open source and actually shows you memory bandwidth utilization, cache hit rates, wavefront occupancy — the same metrics Nsight shows on NVIDIA.

### 5. PyTorch on ROCm — The Practical Layer

PyTorch's ROCm support is now first-class. Internally it uses HIP. The interesting bit is how `torch.compile` (inductor) generates kernels differently for CUDA vs ROCm:

```python
import torch
# Check ROCm
print(torch.version.hip)  # e.g. '5.7.0'
print(torch.cuda.get_device_name(0))  # shows AMD GPU name

# torch.compile works on ROCm
model = torch.compile(your_model)
```

The inductor backend on ROCm generates Triton kernels → HIP → AMDGPU ISA. Full stack is auditable.

---

## The Honest Gap Assessment

| Layer | NVIDIA | AMD ROCm | Gap |
|---|---|---|---|
| Kernel perf (matmul) | 100% | ~85-95% on MI300X | Closing fast |
| Multi-GPU comms | NCCL (fast) | RCCL (close) | Small |
| Profiler | Nsight (excellent) | Omniperf (good) | Medium |
| Ecosystem/libs | Huge | Catching up | Still real |
| Compiler openness | Closed | Fully open | AMD wins |
| Cloud availability | Everywhere | Limited | NVIDIA wins |

**MI300X is actually competitive with H100 on memory bandwidth** (5.2 TB/s vs 3.35 TB/s). For inference on large models, AMD wins on raw bandwidth.

---

## Your Concrete Next Steps

```bash
# 1. Install ROCm (if you have AMD GPU or use cloud)
wget https://repo.radeon.com/amdgpu-install/6.1/ubuntu/jammy/amdgpu-install_6.1_all.deb
# Or just use Docker: rocm/pytorch:latest

# 2. Run hipify on a CUDA kernel you know
hipify-clang flash_attn_kernel.cu

# 3. Write a Triton kernel, benchmark on both
# 4. Read the AMDGPU LLVM backend
# 5. Profile with rocprof/omniperf
```

**Resources worth reading in order:**

- ROCm docs: `rocm.docs.amd.com` — the HIP programming guide
- `github.com/ROCm/HIP` — read the `include/hip/` headers
- `github.com/triton-lang/triton` — `third_party/amd/` backend
- `github.com/ROCm/omniperf` — understand what metrics matter
- AMD CDNA2/3 whitepapers — understand the hardware you're targeting

The open source bet here is real. The LLVM backend being upstream means every compiler improvement benefits AMD. Long-term this matters more than any short-term CUDA ecosystem advantage.