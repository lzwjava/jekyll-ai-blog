---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA Support for Tesla P100
translated: false
type: note
---

Question: What CUDA version does the NVIDIA Tesla P100 support?

Answer:

The **Tesla P100 is Pascal, Compute Capability 6.0 (`sm_60`)**. ([NVIDIA Developer][1])

The important distinction is:

| Thing                            | P100          |
| -------------------------------- | ------------- |
| Architecture                     | Pascal        |
| Compute capability               | **6.0**       |
| First CUDA toolkit               | CUDA **8.0**  |
| Latest toolkit with P100 support | **CUDA 12.x** |
| `nvcc` target                    | `sm_60`       |
| PTX target                       | `compute_60`  |

NVIDIA's current compatibility matrix lists Pascal (`6.0/6.1`) as supported through **CUDA 12.x**. ([NVIDIA Docs][2])

So, for example:

```bash
nvcc -arch=sm_60 foo.cu
```

or:

```bash
nvcc -gencode arch=compute_60,code=sm_60 foo.cu
```

### But there's a catch for modern ML

If you're asking because you're trying to run **PyTorch / vLLM / FlashAttention / modern LLM software** on a P100, **CUDA 12.x support does not mean modern ML libraries support `sm_60`**.

CUDA 12.8 is effectively the end of the line for Pascal development: NVIDIA says Pascal/Volta/Maxwell are now feature-complete, and the **next major CUDA release removes offline compiler support** for those architectures. ([NVIDIA Developer][3])

In practice, I'd target:

```text
P100
  ↓
sm_60
  ↓
CUDA 11.8 / 12.x
  ↓
older PyTorch/CUDA stack
```

rather than blindly installing the newest CUDA/PyTorch stack.

If you're trying to run a specific **PyTorch version or LLM framework on P100**, I can map out the exact working `CUDA + PyTorch + driver` combination.

[1]: https://developer.nvidia.com/cuda/gpus/legacy?utm_source=chatgpt.com "Legacy CUDA GPU Compute Capability | NVIDIA Developer"
[2]: https://docs.nvidia.com/datacenter/tesla/drivers/cuda-toolkit-driver-and-architecture-matrix.html?utm_source=chatgpt.com "CUDA Toolkit, Driver, and Architecture Matrix — NVIDIA Data Center Drivers"
[3]: https://developer.nvidia.com/blog/cuda-toolkit-12-8-delivers-nvidia-blackwell-support?utm_source=chatgpt.com "CUDA Toolkit Now Available for NVIDIA Blackwell | NVIDIA Technical Blog"
