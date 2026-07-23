---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Inside NVIDIA GPUs: Anatomy of High Performance Matmul Kernels"
translated: false
type: note
---

## Question:

Intro to Aleksa Gordić's **"Inside NVIDIA GPUs: Anatomy of high performance matmul kernels"** blog.

## Answer:

This blog is a deep dive into **how modern GPUs actually execute matrix multiplication (matmul)** at the hardware level, especially for AI workloads. It explains why a few lines of PyTorch:

```python
C = A @ B
```

hide an enormous amount of engineering. ([LZWJava][1])

For LLMs, this is one of the most important topics because **Transformers are mostly matmul machines**:

* Linear layers:
  [
  Y = XW
  ]
* Attention projections:
  [
  Q=XW_Q,\ K=XW_K,\ V=XW_V
  ]
* MLP layers:
  [
  XW_1,\ XW_2
  ]

Most training/inference FLOPs happen inside these matrix multiplications. ([Hatena Bookmark][2])

---

# 1. The basic problem

Matrix multiplication:

[
C = A \times B
]

where:

* A: (M \times K)
* B: (K \times N)
* C: (M \times N)

Naive algorithm:

```python
for i in range(M):
    for j in range(N):
        C[i,j] = 0
        for k in range(K):
            C[i,j] += A[i,k] * B[k,j]
```

Complexity:

[
O(MKN)
]

For an LLM:

```
hidden size = 4096
batch = 2048

4096 x 4096 weight matrices
```

means billions of multiply-add operations every forward pass.

---

# 2. Why GPU matmul is hard

A naive CUDA kernel:

```
GPU thread
    load A
    load B
    multiply
    write C
```

is extremely slow.

Why?

Because GPU compute is much faster than memory.

Example:

H100:

```
Tensor Core compute:
~1000+ TFLOPS

HBM bandwidth:
~3 TB/s
```

The GPU can do trillions of operations, but waiting for memory kills performance.

The key idea:

> Move data less. Compute more.

---

# 3. The GPU memory hierarchy

The article explains the hierarchy:

```
              slow
               |
        Global Memory (HBM)
               |
             L2 Cache
               |
     Shared Memory / L1
               |
          Registers
               |
            Tensor Core
               |
              fast
```

A good kernel tries:

```
HBM
 ↓
Shared memory
 ↓
Registers
 ↓
Tensor Core
```

and reuses data many times.

([LZWJava][1])

---

# 4. Tiling: the core optimization

Instead of computing:

```
whole matrix
```

split into blocks:

```
A:

+---+---+
|tile|tile|
+---+---+

B:

+---+---+
|tile|tile|
+---+---+
```

A CUDA block computes one output tile:

```
C tile = A tile × B tile
```

Example:

```
128x128 output tile

load:
A[128x32]
B[32x128]

compute

load next tile

compute
```

This keeps data in fast memory.

---

# 5. Warp-level programming

NVIDIA GPU architecture:

```
GPU
 |
 +-- SM (Streaming Multiprocessor)
       |
       +-- Warp
             |
             +-- 32 threads
```

A warp executes the same instruction:

```
thread0 \
thread1  \
thread2   ---> same instruction
...
thread31 /
```

High performance kernels carefully map:

```
matrix tile
      |
      v
warp
      |
      v
thread
```

---

# 6. Tensor Cores

Modern NVIDIA GPUs don't multiply individual numbers.

They have special hardware:

```
Tensor Core:

A matrix fragment
        +
B matrix fragment

        |
        v

Matrix Multiply Accumulate

C += A @ B
```

The hardware instruction is roughly:

```
D = A * B + C
```

called MMA:

(Matrix Multiply Accumulate)

([Google Research][3])

For example:

FP16:

```
16x16x16 matrix multiply
```

happens in one hardware operation.

---

# 7. PTX and SASS

The stack:

```
PyTorch

   ↓

CUDA kernel

   ↓

PTX

   ↓

SASS

   ↓

GPU instructions
```

PTX:

NVIDIA's virtual assembly language.

Example:

```
mma.sync
```

means:

"execute tensor core matrix multiply"

SASS:

real GPU machine code.

The blog goes down to this level. ([Hatena Bookmark][2])

---

# 8. Async pipelines

Modern GPUs overlap:

```
Load next tile
        |
        |
        v
Compute current tile
```

instead of:

```
load
wait
compute
wait
load
wait
```

A high-performance kernel becomes a pipeline:

```
Stage 0:
HBM -> shared memory

Stage 1:
shared -> registers

Stage 2:
Tensor Core compute

Stage 3:
write result
```

This is why optimized kernels look almost like hardware designs.

---

# 9. Relationship to FlashAttention / Triton

This article helps understand:

* FlashAttention
* Triton kernels
* CUTLASS
* cuBLAS
* vLLM kernels
* DeepSpeed kernels

They all use the same principles:

1. tile data
2. maximize reuse
3. minimize memory movement
4. exploit Tensor Cores

FlashAttention is basically:

> "Instead of optimizing matmul alone, optimize the entire attention computation around GPU memory hierarchy."

---

# 10. Why this matters for LLM engineers

At the PyTorch level:

```python
output = model(input)
```

looks simple.

But underneath:

```
Transformer
 |
Linear layer
 |
GEMM
 |
cuBLAS kernel
 |
Tensor Core MMA
 |
FP16/BF16 multiply accumulate
 |
GPU registers
```

The difference between:

```
30% GPU utilization
```

and

```
90% GPU utilization
```

is usually kernel engineering.

---

For someone training GPT-2/nanoGPT on RTX 4070 or MI300X, this is the missing layer between:

```
"I know PyTorch"
```

and

```
"I understand why H100/MI300X achieves 1000+ TFLOPS"
```

The article is essentially a **GPU architecture textbook chapter written from the perspective of an LLM engineer**. ([LZWJava][1])

References:

* [Inside NVIDIA GPUs: Anatomy of high performance matmul kernels - Aleksa Gordić](https://www.aleksagordic.com/blog/matmul?utm_source=chatgpt.com)
* [Mixed-input matrix multiplication performance optimizations - Google Research](https://research.google/blog/mixed-input-matrix-multiplication-performance-optimizations/?utm_source=chatgpt.com)

[1]: https://lzwjava.github.io/gpu-matrix-multiplication-kernels-en?utm_source=chatgpt.com "High-Performance GPU Matrix Multiplication Kernels"
[2]: https://b.hatena.ne.jp/entry/s/www.aleksagordic.com/blog/matmul?utm_source=chatgpt.com "[B!] Inside NVIDIA GPUs: Anatomy of high performance matmul kernels - Aleksa Gordić"
[3]: https://research.google/blog/mixed-input-matrix-multiplication-performance-optimizations/?utm_source=chatgpt.com "Mixed-input matrix multiplication performance optimizations"
