---
audio: false
generated: true
image: false
lang: en
layout: post
title: GEMM in Large Language Models
translated: false
type: note
---

Question: What is **GEMM** in LLMs?

Answer:

**GEMM = General Matrix-Matrix Multiplication.**

It is basically the operation:

[
C = AB
]

where:

* (A \in \mathbb{R}^{M \times K})
* (B \in \mathbb{R}^{K \times N})
* (C \in \mathbb{R}^{M \times N})

In an LLM, **a huge fraction of compute ultimately becomes GEMMs**.

### 1. The simplest example: Linear layer

A Transformer linear layer is:

```python
y = x @ W
```

Suppose:

```text
x: [batch * seq_len, hidden]
W: [hidden, 4 * hidden]
```

For example:

```text
x = [8192, 4096]
W = [4096, 16384]

y = x @ W

y = [8192, 16384]
```

That's a GEMM:

[
[8192 \times 4096] [4096 \times 16384]
\rightarrow
[8192 \times 16384]
]

---

### 2. Transformer FFN is basically GEMM → activation → GEMM

For a standard MLP:

```python
h = x @ W1
h = activation(h)
y = h @ W2
```

So:

[
XW_1 \rightarrow \text{GELU} \rightarrow HW_2
]

Two large GEMMs dominate the compute.

For a SwiGLU block:

```python
a = x @ W_gate
b = x @ W_up
h = silu(a) * b
y = h @ W_down
```

That's **three GEMMs**.

---

### 3. Attention also contains GEMMs

Given:

```python
Q = X @ Wq
K = X @ Wk
V = X @ Wv
```

These are GEMMs.

Then attention has:

[
S = QK^T
]

which is another matrix multiplication.

And:

[
O = \operatorname{softmax}(S)V
]

another matrix multiplication.

So a Transformer layer has lots of matrix multiplications.

---

### 4. Why GPUs are obsessed with GEMM

A GEMM:

[
C_{ij} = \sum_{k=1}^{K} A_{ik}B_{kj}
]

requires roughly:

[
2MNK
]

floating-point operations.

For example:

```text
M = 8192
K = 4096
N = 16384
```

gives:

[
2 \times 8192 \times 4096 \times 16384
\approx 1.1 \times 10^{12}
]

That's **~1.1 TFLOPs of work for one matrix multiplication**.

This is exactly the kind of highly regular computation GPUs are extremely good at.

---

### 5. GEMM vs GEMV

You'll see these terms a lot in LLM inference:

```text
GEMM = matrix × matrix
GEMV = matrix × vector
```

For example, during **training / prefill**:

```text
[sequence, hidden] @ [hidden, hidden]
```

is a GEMM.

During **single-token decode**, you might have:

```text
[1, hidden] @ [hidden, hidden]
```

which is effectively GEMV.

This distinction matters enormously for LLM inference:

```text
Prefill:
large M
→ GEMM
→ high GPU utilization
→ compute-bound

Decode:
M ≈ 1
→ GEMV / skinny GEMM
→ poor GPU utilization
→ often memory-bandwidth-bound
```

This is one reason **LLM decode is fundamentally different from training/prefill**.

### 6. GEMM → Tensor Cores

On modern NVIDIA GPUs, you generally don't want to implement:

```python
C[i,j] += A[i,k] * B[k,j]
```

yourself.

Libraries such as **cuBLAS/cuBLASLt** dispatch GEMMs to highly optimized GPU kernels, which can use **Tensor Cores**.

Conceptually:

```text
PyTorch
   ↓
torch.matmul()
   ↓
cuBLAS / cuBLASLt
   ↓
Tensor Core kernels
   ↓
FP16 / BF16 / FP8 / INT8 / ...
```

And this is why when you look at LLM performance, terms like:

**FLOPS, TFLOPS, Tensor Cores, GEMM, GEMV, MFMA, CUTLASS, cuBLAS, Triton**

keep appearing together.

The important mental model is:

> **A Transformer is largely a machine for turning tensors into a sequence of highly optimized matrix multiplications, with attention, normalization, activation, and memory movement around them.**

For training LLMs, **GEMM is one of the fundamental kernels to understand**.
