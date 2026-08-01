---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Matrix Multiplication Mysteries
translated: false
type: note
---

Question: Introduction to “Strangely Matrix Multiplications” from Thonking.ai

Answer:

This article by Horace He is about a very practical GPU/AI systems question:

**Why can two mathematically equivalent matrix multiplications have wildly different performance on GPUs?** ([Thonking.ai][1])

For LLM engineers, this is extremely relevant because **Transformer inference and training are basically huge numbers of GEMMs (General Matrix Multiplications)**:

```
Attention:
Q = XWq
K = XWk
V = XWv

MLP:
h = XW1
y = hW2
```

Every one of these becomes:

```
[M x K] @ [K x N] = [M x N]
```

The surprising part:

```
2048 x 2048 @ 2048 x 2048
```

can sometimes be faster than:

```
2047 x 2048 @ 2048 x 2048
```

even though the second one has fewer FLOPs. ([Thonking.ai][1])

## 1. Matrix multiplication is not just math

The mathematical operation:

genui{"linear_algebra_optimization":{"type_id":"MATRIX_MULTIPLICATION_ROW_COLUMN_RULE","locale_override":"en-US"}}

```
C = A @ B

C[i,j] = sum(A[i,k] * B[k,j])
```

looks simple.

But GPU execution is not:

```
for i:
    for j:
        for k:
            C[i,j] += A[i,k]*B[k,j]
```

Modern GPU does:

```
Matrix
  |
  v
split into tiles
  |
  v
GPU thread blocks
  |
  v
shared memory
  |
  v
Tensor Cores
```

The GPU wants nice shapes.

---

## 2. Tiling: the hidden reason

Suppose GPU kernel uses tiles:

```
128 x 128
```

It divides:

```
2048 x 2048 matrix

into:

16 x 16 tiles
```

Perfect:

```
2048 / 128 = 16
```

No waste.

But:

```
2047 / 128 = 15.99
```

Now GPU needs:

```
15 full tiles
+
1 partial tile
```

That last tile wastes computation.

Example:

```
real work:

127 x 127


GPU executes:

128 x 128
```

Many GPU operations become masked.

---

## 3. Memory alignment matters

The article explains that the "odd shape" problem is often not the odd number itself, but whether the **innermost dimension** aligns with GPU memory access. ([Thonking.ai][2])

GPU likes:

```
float16 / bfloat16

128 elements
256 bytes
512 bytes
```

because:

```
memory transaction
        |
        v
aligned chunk
```

is efficient.

Bad:

```
2047 elements
```

means:

```
GPU memory:

[128][128][128]...[127]

last load:
misaligned
```

More memory transactions.

---

## 4. Wave quantization

This is another GPU-specific effect.

Example:

GPU:

```
80 SMs
```

Kernel creates:

```
160 blocks
```

Perfect:

```
SM0: block0
SM1: block1
...
SM79:block79

second wave:
all SMs busy again
```

But:

```
161 blocks
```

means:

```
wave 1:
80 blocks

wave 2:
80 blocks

wave 3:
1 block
```

The last wave uses only:

```
1 / 80
```

of the GPU.

Very inefficient.

This creates those strange performance spikes in benchmarks. ([Thonking.ai][1])

---

## 5. Why this matters for vLLM / nano-vLLM

This is exactly why production inference engines care about shapes.

Example:

Qwen:

```
hidden size = 4096
heads = 32
```

Linear layer:

```
[batch,4096]
       @
[4096,12288]

=
[batch,12288]
```

If:

```
batch=1
```

during decoding:

```
[1,4096] @ [4096,12288]
```

This is a very different GPU problem from training:

```
[4096,4096] @ [4096,12288]
```

Training:

* huge matrices
* compute bound

Inference decode:

* tiny batch
* memory bound
* KV cache dominates

This is why vLLM has optimizations like:

* continuous batching
* paged KV cache
* CUDA kernels
* fused operations

---

## 6. The deeper lesson

The article is a good example of a principle in AI systems:

> The algorithm is not only mathematics. The hardware execution model becomes part of the algorithm.

A PyTorch line:

```python
C = A @ B
```

looks like one operation.

But underneath:

```
PyTorch
 |
 v
cuBLAS
 |
 v
CUDA kernel selection
 |
 v
thread blocks
 |
 v
warps
 |
 v
Tensor Core instructions
 |
 v
memory hierarchy
```

The performance depends on all layers.

For someone learning **nano-vLLM / CUDA / AI infra**, this article is exactly the next level after understanding Transformer math:

1. Transformer equations
2. PyTorch implementation
3. CUDA memory model
4. GEMM kernels
5. Tensor Core optimization
6. vLLM scheduling

This is the path from "I can use LLMs" → "I understand why GPT runs fast." ([Thonking.ai][1])

References:

* Horace He, “What Shapes Do Matrix Multiplications Like?” ([Thonking.ai][1])
* Horace He, “Solutions: What Shapes Do Matrix Multiplications Like?” ([Thonking.ai][2])
* NVIDIA, Matrix Multiplication Performance Documentation (referenced by article) ([Thonking.ai][1])

[1]: https://www.thonking.ai/p/what-shapes-do-matrix-multiplications?utm_source=chatgpt.com "What Shapes Do Matrix Multiplications Like? [medium]"
[2]: https://www.thonking.ai/p/answer-key-what-shapes-do-matrix?utm_source=chatgpt.com "Solutions: What Shapes Do Matrix Multiplications Like?"
