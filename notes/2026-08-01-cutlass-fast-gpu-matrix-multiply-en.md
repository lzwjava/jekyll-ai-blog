---
audio: false
generated: true
image: false
lang: en
layout: post
title: "CUTLASS: Fast GPU Matrix Multiply"
translated: false
type: note
---

Question: What is CUTLASS and how does it make GPU matrix multiplication fast?

Answer:

**CUTLASS = CUDA Templates for Linear Algebra Subroutines.**

It is NVIDIA's library/framework for writing **high-performance GPU kernels**, especially **GEMM (General Matrix Multiply)**:

[
C = A \times B
]

It sits between:

```
PyTorch / TensorFlow
        |
      cuBLAS
        |
     CUTLASS
        |
      CUDA
        |
    Tensor Core / SM hardware
```

CUTLASS exposes the low-level building blocks so engineers can write kernels close to cuBLAS performance but customized for specific models, data types, and GPU architectures. ([NVIDIA Docs][1])

---

## Why CUTLASS exists

A naive CUDA matrix multiplication:

```cpp
for (i)
  for (j)
    for (k)
       C[i][j] += A[i][k] * B[k][j];
```

has terrible GPU performance.

Why?

Because:

* global memory is slow
* each thread does little work
* no Tensor Core usage
* no shared memory reuse

A modern GPU GEMM looks like this:

```
Global Memory
      |
      v
+-------------+
| Threadblock |
|   128x128   |   <-- CTA tile
+-------------+
      |
      v
 Shared Memory
      |
      v
+-------------+
|   Warp      |
|    64x64    |
+-------------+
      |
      v
 Tensor Core
   mma.sync
```

CUTLASS provides abstractions for every level. ([NVIDIA Docs][2])

---

# 1. The key idea: hierarchical tiling

Suppose:

```
A = 4096 x 4096
B = 4096 x 4096
```

You don't calculate:

```
C[0][0]
C[0][1]
...
```

one element at a time.

Instead:

```
C matrix

+----------------+
|128|128|128|128 |
|---+---+---+---|
|128|128|128|128 |
|---+---+---+---|
|128|128|128|128 |
+----------------+
```

Each CUDA block owns a tile:

```
CTA tile:

        B
   128 columns

   +-----------+
   |           |
128|     C     |
rows|  tile    |
   |           |
   +-----------+

```

Then:

[
C_{tile}=A_{tile}\times B_{tile}
]

---

# 2. Inside a tile

For a 128x128 output tile:

The K dimension is streamed:

```
A:

128 x K


B:

K x 128


C:

128 x 128
```

Break K:

```
K=4096

step 0:

A[128 x 32]

B[32 x 128]


step 1:

A[128 x 32]

B[32 x 128]

...
```

Accumulation:

[
C += A_i B_i
]

This is the GEMM main loop.

---

# 3. Tensor Core path

Modern NVIDIA GPUs don't multiply one float at a time.

Tensor Core instruction:

```
mma.sync
```

does something like:

```
16x16x16 matrix multiply
```

in hardware.

Example:

```
A fragment:

16 x 16

B fragment:

16 x 16


Tensor Core:

A @ B

=

C
```

CUTLASS maps:

```
thread
   |
warp
   |
warpgroup
   |
Tensor Core instruction
```

automatically.

---

# 4. CUTLASS concepts

The important vocabulary:

## Tile

A chunk of matrix:

```
128 x 128
```

Example:

```
GemmShape<128,128,32>
```

means:

```
M = 128
N = 128
K = 32
```

---

## Threadblock

A CUDA block.

Example:

```
256 threads
```

owns:

```
128x128 C tile
```

---

## Warp tile

A warp:

```
32 threads
```

owns:

```
64x64
```

---

## MMA

Matrix multiply accumulate:

```
D = A*B + C
```

Tensor Core operation.

---

## Layout

Very important.

GPU memory is linear:

```
0 1 2 3 4 5 ...
```

but matrix is:

```
A[i][j]
```

CUTLASS needs mapping:

```
logical coordinate

(i,j)

      |
      v

memory address
```

This is what CuTe (CUTLASS 3.x) improves. ([NVIDIA Docs][3])

---

# 5. Why 2048 is faster than 2047

Your previous question connects directly.

GPU likes:

```
tile size = 128
```

For:

```
2048 / 128 = 16
```

perfect:

```
16 x 16 tiles
```

For:

```
2047 / 128
```

you get:

```
15 full tiles

+

one partial tile
```

The last tile wastes:

```
128 - 127 valid elements
```

Threads still exist.

GPU executes warps, not individual useful elements.

CUTLASS/cuBLAS are optimized around these regular shapes. ([NVIDIA Docs][2])

---

# 6. Tiny CUTLASS example

Conceptually:

```cpp
using Gemm = cutlass::gemm::device::Gemm<
    half,                 // A
    RowMajor,
    half,                 // B
    ColumnMajor,
    float                 // accumulator
>;

Gemm gemm;

gemm({
    {M,N,K},
    {A,lda},
    {B,ldb},
    {C,ldc}
});
```

The template parameters choose:

* datatype
* memory layout
* architecture
* instruction type
* tile policy

CUTLASS uses C++ template metaprogramming to generate specialized kernels. ([NVIDIA Docs][1])

---

# 7. Why this matters for LLM inference/training

Transformers are basically:

```
Attention:

Q @ K^T

+

softmax

+

V


MLP:

X @ W1

X @ W2
```

Most compute:

```
matrix multiplication
```

Therefore:

```
LLM performance
        |
        v
fast GEMM
        |
        v
Tensor Core utilization
        |
        v
CUTLASS knowledge
```

Projects like:

* FlashAttention
* xFormers
* TensorRT-LLM
* vLLM kernels

all live in this world.

---

A good learning path for you (because you are already doing nano-vLLM/nanoGPT):

```
1. CUDA basics
   |
2. write naive matmul kernel
   |
3. shared-memory tiled matmul
   |
4. WMMA Tensor Core example
   |
5. CUTLASS GEMM example
   |
6. FlashAttention kernel
   |
7. vLLM PagedAttention CUDA kernels
```

CUTLASS is basically the bridge from **"I understand PyTorch"** to **"I can write the kernels that make PyTorch fast."**

References:

* NVIDIA CUTLASS Documentation ([NVIDIA Docs][1])
* CUTLASS GEMM API ([NVIDIA Docs][2])
* CUTLASS Getting Started Guide ([NVIDIA Docs][4])

[1]: https://docs.nvidia.com/cutlass/latest/index.html?utm_source=chatgpt.com "Welcome to CUTLASS — NVIDIA CUTLASS Documentation"
[2]: https://docs.nvidia.com/cutlass/latest/media/docs/cpp/gemm_api.html?utm_source=chatgpt.com "CUTLASS GEMM API — NVIDIA CUTLASS Documentation"
[3]: https://docs.nvidia.com/cutlass/latest/overview.html?utm_source=chatgpt.com "Overview — NVIDIA CUTLASS Documentation"
[4]: https://docs.nvidia.com/cutlass/latest/media/docs/cpp/getting_started.html?utm_source=chatgpt.com "Getting Started — NVIDIA CUTLASS Documentation"
