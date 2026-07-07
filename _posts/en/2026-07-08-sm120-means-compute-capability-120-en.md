---
audio: false
generated: true
image: false
lang: en
layout: post
title: SM120 Means Compute Capability 12.0
translated: false
type: note
---

Question: What does SM120 mean in NVIDIA GPU terminology? Is SM the Streaming Multiprocessor, and do engineers call H200/RTX4070 "SM120"?

Answer:

Your understanding is close, but there are two related meanings:

## 1. SM = Streaming Multiprocessor

Yes, **SM stands for Streaming Multiprocessor**. It is the fundamental execution unit inside an NVIDIA GPU.

A GPU is roughly:

```
GPU
 ├── SM 0
 │    ├── CUDA cores
 │    ├── Tensor cores
 │    ├── registers
 │    ├── shared memory
 │    └── warp schedulers
 │
 ├── SM 1
 │    └── ...
 │
 └── SM N
```

CUDA schedules work at the SM level. A CUDA kernel launches thread blocks, and thread blocks are assigned to SMs.

([NVIDIA Docs][1])

---

## 2. But "SM120" usually means Compute Capability 12.0

When NVIDIA engineers say:

```
sm_120
SM120
```

they usually mean **CUDA Compute Capability 12.0**, not "the GPU has 120 streaming multiprocessors".

The naming:

```
sm_<major><minor>

sm_80  = Compute Capability 8.0
sm_86  = Compute Capability 8.6
sm_89  = Compute Capability 8.9
sm_90  = Compute Capability 9.0
sm_120 = Compute Capability 12.0
```

CUDA compiler targets are named this way. ([NVIDIA Developer][2])

Example:

```bash
nvcc kernel.cu -arch=sm_120
```

means:

"compile this CUDA kernel optimized for Blackwell compute capability 12.0."

---

## 3. Your examples are mixed

### RTX 4070

Ada Lovelace:

```
Architecture: Ada
Compute Capability: 8.9
CUDA target: sm_89
```

So:

```
RTX 4070 -> SM89
```

not SM120.

---

### H200

Hopper:

```
Architecture: Hopper
Compute Capability: 9.0
CUDA target: sm_90
```

So:

```
H200 -> SM90
```

not SM120.

---

### RTX 5090 / RTX PRO Blackwell

Blackwell consumer/workstation:

```
Architecture: Blackwell
Compute Capability: 12.0
CUDA target: sm_120
```

So:

```
RTX 5090 -> SM120
```

([NVIDIA Developer][2])

---

The engineer shorthand is basically:

| GPU       | Architecture         | CUDA target |
| --------- | -------------------- | ----------- |
| RTX 4090  | Ada                  | sm_89       |
| RTX 4070  | Ada                  | sm_89       |
| H100/H200 | Hopper               | sm_90       |
| B200      | Blackwell datacenter | sm_100      |
| RTX 5090  | Blackwell consumer   | sm_120      |

([NVIDIA Developer][2])

---

For AI kernel development, this matters because libraries like **PyTorch, FlashAttention, Triton, CUTLASS, vLLM** compile specialized kernels for these targets.

Example:

```bash
TORCH_CUDA_ARCH_LIST="8.9;9.0;12.0"
```

means:

"build kernels for Ada, Hopper, and Blackwell."

A kernel compiled only for `sm_89` may run on newer GPUs through PTX JIT, but it will not necessarily use new hardware features like Blackwell FP4/Tensor Core instructions. ([NVIDIA Developer][3])

So NVIDIA engineers saying "SM120" are speaking the CUDA compiler/hardware capability language, not literally counting SM units.

[1]: https://docs.nvidia.com/cuda/archive/12.8.0/pdf/Blackwell_Tuning_Guide.pdf?utm_source=chatgpt.com "Blackwell Tuning Guide"
[2]: https://developer.nvidia.com/cuda/gpus?utm_source=chatgpt.com "CUDA GPU Compute Capability | NVIDIA Developer"
[3]: https://developer.nvidia.com/blog/nvidia-blackwell-and-nvidia-cuda-12-9-introduce-family-specific-architecture-features/?utm_source=chatgpt.com "NVIDIA Blackwell and NVIDIA CUDA 12.9 Introduce Family-Specific Architecture Features | NVIDIA Technical Blog"
