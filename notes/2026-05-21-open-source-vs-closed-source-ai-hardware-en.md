---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open-Source vs Closed-Source AI Hardware
translated: false
type: note
---

**Question:** I'm diving into open-source chip software (AMD ROCm as the open-source CUDA alternative). I want to understand the gap between open-source and closed-source in the AI value chain. What should I know next?

**Answer:**

Good instinct. Here's the map — from where you are to where it gets interesting.

## The AI Value Chain: Open vs Closed Gap (honest assessment)

| Layer | Open Source | Closed Source | Gap |
| --- | --- | --- | --- |
| **ML Frameworks** | PyTorch, JAX | — | Basically closed. PyTorch IS the standard |
| **Compiler/IR** | MLIR, XLA, Triton | cuDNN internals | Medium — Triton closes it fast |
| **Runtime** | ROCm HIP, oneAPI | CUDA runtime | Medium — ROCm ~85% there |
| **Kernel libs** | rocBLAS, MIOpen | cuBLAS, cuDNN | Significant — NVIDIA still wins perf |
| **Hardware uArch** | RISC-V (VexRiscV, CVA6) | NVIDIA SM design | **Huge** — uArch docs still proprietary |
| **Driver** | `amdgpu` (in-kernel) | NVIDIA open kernel (partial) | AMD actually wins here |

**Verdict:** Software stack gap is closeable. Hardware uArch gap is the moat NVIDIA actually has.

---

## What to Actually Study Next (ordered)

### 1. HIP + ROCm internals (you're here)

```bash
# Confirm your ROCm install sees the GPU
rocminfo | grep -A5 "Agent 2"
hipcc --version

# Hello triangle in HIP
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

HIP → CUDA translation is ~95% mechanical. `hipify-clang` converts CUDA → HIP automatically. This is how ROCm bootstrapped.

---

### 2. Triton — the real open-source inflection point

This is where the action is. Triton lets you write GPU kernels in Python that **compile to both CUDA PTX and AMD GCN/RDNA**. OpenAI open-sourced it and it's now in PyTorch core.

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

**Why this matters:** Flash Attention 2, the kernel that makes LLM inference fast, is written in Triton. The gap between ROCm and CUDA is shrinking fastest here.

---

### 3. MLIR + the compiler stack (where open-source is winning)

```
PyTorch/JAX
    ↓ torch.compile / XLA
  Triton IR / StableHLO
    ↓ MLIR passes
  LLVM IR
    ↓
  PTX (NVIDIA) / GCN ISA (AMD) / RISC-V (future)
```

MLIR is Google/LLVM's bet on a unified compiler IR. Every major chip startup (Tenstorrent, Groq, Cerebras) targets MLIR. **This is the layer where open-source actually leads.**

```bash
# Play with MLIR
pip install mlir-python-bindings
# Or build from source for full control
git clone https://github.com/llvm/llvm-project
cd llvm-project && cmake -DLLVM_ENABLE_PROJECTS="mlir" ...
```

---

### 4. Open-source hardware — RISC-V GPU experiments

This is frontier territory. Actual open GPU cores:

- **Vortex** — RISC-V GPGPU, runs OpenCL, tapes out on FPGA

  ```bash
  git clone https://github.com/vortexgpgpu/vortex
  # Runs on Verilator simulation or actual FPGA
  ```

- **NaxRiscv** — out-of-order RISC-V, serious uArch
- **NVDLA** (NVIDIA open-sourced their DLA) — inference accelerator RTL

The gap: open RTL exists, but **process node access** (TSMC 4nm) is the actual moat. Software is solvable. Fab access isn't.

---

## The Real Moat Map

```
cuDNN fused kernels (hand-tuned asm)        ← hardest to replicate
CUDA PTX ISA stability + ecosystem lock-in  ← 15 years of software
NVLink / NVSwitch topology                  ← hardware, needs $$$
HBM allocation + supplier relationships     ← supply chain
```

ROCm closes the software gap. Nobody closes the HBM/NVLink gap without a fab.

---

## Your Learning Path

```
Week 1-2:  HIP kernels, hipify existing CUDA code
Week 3-4:  Triton kernel writing — reimplement softmax, layernorm
Week 5-6:  torch.compile internals, Dynamo/Inductor
Week 7-8:  MLIR basics — write a simple lowering pass
Month 3+:  Vortex RISC-V GPU on Verilator, understand GCN ISA
```

**Key repos to star:**

```bash
# Core
https://github.com/ROCm/ROCm
https://github.com/triton-lang/triton
https://github.com/llvm/llvm-project          # MLIR lives here

# Learn from
https://github.com/tinygrad/tinygrad          # George Hotz's ROCm-first stack
https://github.com/vortexgpgpu/vortex         # Open RISC-V GPU
https://github.com/openxla/xla               # Google's compiler
```

**tinygrad is your best teacher here** — it's a full ML framework that runs on ROCm, written to be readable, and George explicitly built it to understand + fight CUDA lock-in. Read the `runtime/` folder.

---

## Bottom Line

The open-source software stack (ROCm + Triton + MLIR + PyTorch) is **good enough for 90% of workloads** and closing fast. The remaining gap is in hand-tuned kernel libraries (cuDNN) and hardware topology (NVLink). If you're going deep on this, Triton + tinygrad is the fastest path to understanding where the real work happens.

**References:**

- [ROCm GitHub](https://github.com/ROCm/ROCm)
- [Triton Lang](https://github.com/triton-lang/triton)
- [tinygrad — ROCm-first ML framework](https://github.com/tinygrad/tinygrad)
- [Vortex RISC-V GPGPU](https://github.com/vortexgpgpu/vortex)
- [MLIR in LLVM](https://mlir.llvm.org/)
- [Flash Attention in Triton](https://github.com/Dao-AILab/flash-attention)
