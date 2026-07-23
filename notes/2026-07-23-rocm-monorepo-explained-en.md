---
audio: false
generated: true
image: false
lang: en
layout: post
title: ROCm Monorepo Explained
translated: false
type: note
---

## Question: What is the ROCm monorepo and how should we understand it?

## Answer:

AMD ROCm (Radeon Open Compute platform) is AMD's **open GPU software stack**, analogous to NVIDIA CUDA.

The important point: **ROCm is not one library. It is an ecosystem.**

The GitHub repository `ROCm/ROCm` is a **meta repository**. It does not contain the entire implementation of ROCm. Instead, it acts like a **map/index/build manifest** that connects hundreds of ROCm components.

A mental model:

```
                AI Frameworks
                     |
        +------------+-------------+
        |                          |
     PyTorch                  TensorFlow
        |
        |
       HIP
 (CUDA-like programming layer)
        |
        |
    ROCr / ROCclr
 (GPU runtime layer)
        |
        |
    HSA Runtime
 (hardware abstraction)
        |
        |
     AMD GPU
 MI300X / MI250 / MI210 / Radeon
```

---

## 1. HIP — AMD's CUDA alternative

The most important ROCm component is **HIP**.

CUDA:

```cpp
__global__ void add(float *a, float *b) {
    int i = threadIdx.x;
    a[i] += b[i];
}
```

HIP:

```cpp
__global__ void add(float *a, float *b) {
    int i = hipThreadIdx_x;
    a[i] += b[i];
}
```

HIP tries to make CUDA code portable.

Example:

```
CUDA code
    |
    | hipify
    v
HIP code
    |
    v
AMD GPU
```

A lot of PyTorch AMD support works because PyTorch CUDA kernels can be translated into HIP.

---

## 2. Math libraries

CUDA has:

```
cuBLAS
cuFFT
cuRAND
cuSPARSE
```

ROCm equivalents:

| NVIDIA   | AMD ROCm  |
| -------- | --------- |
| cuBLAS   | rocBLAS   |
| cuFFT    | rocFFT    |
| cuRAND   | rocRAND   |
| cuSPARSE | rocSPARSE |
| cuSOLVER | rocSOLVER |

Example:

Matrix multiplication:

```
C = A × B
```

AI training spends enormous time here.

PyTorch:

```python
torch.matmul(a,b)
```

eventually becomes:

```
PyTorch
  |
ATen
  |
rocBLAS
  |
HIP
  |
GPU Matrix Core
```

---

## 3. Compiler stack

ROCm has its own compiler infrastructure:

```
C++ / HIP source
        |
        v
      clang
        |
        v
    LLVM backend
        |
        v
    AMD GCN / CDNA ISA
        |
        v
      GPU
```

Important pieces:

### ROCm Compiler Support

Provides:

* clang HIP compiler
* LLVM patches
* device libraries

Example:

```bash
hipcc hello.cpp
```

is AMD's equivalent of:

```bash
nvcc hello.cu
```

---

## 4. GPU runtime

The runtime manages:

* GPU memory
* kernel launching
* synchronization
* queues

NVIDIA:

```
CUDA Runtime
      |
CUDA Driver
      |
GPU
```

AMD:

```
HIP Runtime
      |
ROCr Runtime
      |
HSA
      |
GPU
```

HSA = Heterogeneous System Architecture.

AMD designed this around CPU + GPU integration.

---

## 5. Communication: RCCL

For AI clusters, this is critical.

NVIDIA:

```
NCCL
```

AMD:

```
RCCL
```

Example:

Training GPT:

```
GPU0              GPU1

layer gradients

     |
     v

 all-reduce

     |
     v

 synchronized weights
```

PyTorch distributed:

```python
torch.distributed.all_reduce()
```

On NVIDIA:

```
NCCL
```

On AMD:

```
RCCL
```

For MI300X clusters, RCCL is a core component.

---

## 6. Profiling and debugging

Like NVIDIA Nsight:

AMD has:

### rocprofiler

Performance counters:

```
GPU utilization
memory bandwidth
kernel time
cache behavior
```

Example:

```bash
rocprof ./train.py
```

### roctracer

Tracing:

```
PyTorch
 |
HIP kernel
 |
GPU execution timeline
```

Useful for finding:

* slow kernels
* CPU bottlenecks
* synchronization issues

---

## 7. Deep learning stack

Modern AI:

```
User
 |
PyTorch
 |
torch-mlir / ATen
 |
HIP
 |
MIOpen
 |
rocBLAS
 |
ROCm
 |
MI300X
```

Equivalent NVIDIA stack:

```
PyTorch
 |
CUDA
 |
cuDNN
 |
cuBLAS
 |
CUDA Driver
 |
H100
```

---

## 8. Why ROCm matters for AI

Historically:

```
NVIDIA:
CUDA ecosystem advantage
---------------------------------
GPU
CUDA
cuDNN
TensorRT
NCCL
PyTorch support
Developer tools
```

AMD had:

```
GPU
+
hardware advantage
-
software ecosystem gap
```

ROCm is AMD's attempt to close this gap.

For example:

### MI300X

Hardware:

```
192GB HBM3
5.3 TB/s bandwidth
```

Software:

```
ROCm
 |
PyTorch
 |
DeepSpeed
 |
Megatron
 |
vLLM
```

Without ROCm, MI300X cannot compete with H100/H200.

---

## 9. How to think about ROCm repo as an engineer

The repo is like a Linux kernel umbrella repo.

You usually don't modify it directly.

You interact with:

AI developer:

```
pip install torch
```

then:

```
torch.version.hip
```

Kernel developer:

```
HIP C++ kernels
```

Compiler developer:

```
LLVM / clang
```

Performance engineer:

```
rocprof
```

Cluster engineer:

```
RCCL + Kubernetes
```

---

## 10. Relationship with your MI300X / PyTorch work

For your use case (training GPT-style models):

```
nanoGPT
 |
PyTorch
 |
ROCm PyTorch build
 |
HIP
 |
rocBLAS
 |
MIOpen
 |
RCCL (multi GPU)
 |
MI300X
```

Most of your code stays unchanged:

```python
device="cuda"
```

even on AMD.

PyTorch exposes:

```python
torch.cuda.is_available()
```

because HIP intentionally mimics CUDA APIs.

Example:

```python
import torch

print(torch.cuda.is_available())
print(torch.version.hip)
```

Output on AMD:

```
True
6.2.x
```

---

## Summary

ROCm is essentially:

```
AMD GPU equivalent of CUDA

          ROCm
           |
 +---------+----------+
 |         |          |
 HIP    Libraries   Tools
 |         |          |
CUDA    BLAS       Profiler
API     FFT        Debugger

           |
        PyTorch

           |
        MI300X
```

For AI infrastructure, the two biggest pieces to understand are:

1. **HIP** → CUDA compatibility layer
2. **RCCL** → multi-GPU training communication

The ROCm monorepo is the "table of contents" connecting all these pieces together.
