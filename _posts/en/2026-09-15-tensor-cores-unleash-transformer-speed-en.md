---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tensor Cores Unleash Transformer Speed
translated: false
type: note
---

Question: **Why are Tensor Cores so important for modern deep learning?**

Answer: Because **transformers are basically giant matrix multiplications**, and Tensor Cores are specialized hardware for doing those multiplications at much higher throughput than ordinary CUDA cores.

The important distinction is:

```text
CUDA core:
    scalar/vector arithmetic

Tensor Core:
    matrix × matrix + accumulate
```

### 1. What actually happens in a transformer

Take one linear layer:

$$
Y = XW
$$

Suppose:

```text
X: [4096, 4096]
W: [4096, 4096]
```

That's roughly:

$$
2 \times 4096^3 \approx 137 \text{ billion FLOPs}
$$

And a transformer does this **over and over**, across many layers and tokens.

Attention has more matrix multiplications:

$$
QK^T
$$

$$
\text{softmax}(QK^T)V
$$

and the MLP has several more:

$$
XW_1,\quad XW_2
$$

So GEMM dominates the compute.

---

## 2. CUDA cores can do it, but Tensor Cores eat GEMMs for breakfast

Conceptually, a CUDA core does something like:

```python
for i:
    for j:
        for k:
            C[i,j] += A[i,k] * B[k,j]
```

Tensor Cores instead have hardware instructions that effectively perform **small matrix multiply-accumulate tiles** in one operation.

For example, conceptually:

```text
       A              B
   ┌───────┐       ┌───────┐
   │       │       │       │
   │  16×16│   ×   │  16×16│
   │       │       │       │
   └───────┘       └───────┘
          \           /
           \         /
            ┌───────┐
            │  C    │
            └───────┘
```

The exact tile dimensions/instructions vary by GPU architecture and datatype, but the key idea is that the hardware is built specifically around dense matrix operations.

---

## 3. The insane part is the throughput

This is where your P100 question matters.

Very roughly:

```text
P100
  FP32 CUDA:       ~10 TFLOPS
  Tensor Cores:     0

V100
  FP32 CUDA:       ~15.7 TFLOPS
  FP16 Tensor:    ~125 TFLOPS
```

The exact Tensor Core number depends on whether you're talking about dense/sparse modes, accumulation type, clock, etc., but the important order-of-magnitude difference is:

```text
P100:  ~10 TFLOP/s
V100: ~100+ TFLOP/s Tensor Core
```

That's why **V100 isn't merely "a slightly faster P100."**

For the workloads Tensor Cores target, it's almost a different class of machine.

---

# 4. Why FP16 makes this especially powerful

Modern neural networks generally don't need every intermediate calculation to be FP32.

You can often do:

```text
weights        FP16/BF16
activations    FP16/BF16
GEMM           FP16/BF16
accumulation   FP32
```

Conceptually:

$$
C_{FP32} = \sum A_{FP16}B_{FP16}
$$

This is enormously useful because neural-network training is unusually tolerant of reduced precision.

Tensor Cores are designed around exactly this.

So instead of:

```text
FP32 GEMM
  ↓
CUDA cores
  ↓
~10 TFLOP/s
```

you get:

```text
FP16/BF16 GEMM
      ↓
 Tensor Cores
      ↓
~100+ TFLOP/s
```

That's the fundamental reason modern GPUs became such powerful AI accelerators.

---

# 5. Why your P100 specifically sucks for modern LLM training

P100 is Pascal.

```text
Pascal P100
    │
    ├── FP32 CUDA cores
    ├── FP16 CUDA arithmetic
    └── NO Tensor Cores
```

V100 is Volta:

```text
Volta V100
    │
    ├── FP32 CUDA cores
    ├── FP16 arithmetic
    └── Tensor Cores  ← huge upgrade
```

Then:

```text
Turing
  ↓
Ampere
  ↓
Hopper
  ↓
Blackwell
```

Tensor Core capability keeps getting more sophisticated:

```text
FP16
 ↓
BF16
 ↓
TF32
 ↓
FP8
 ↓
FP4 / newer low precision
```

So if you're training an LLM, the relevant comparison isn't simply:

```text
"How many CUDA cores?"
```

It's much closer to:

```text
effective_training_throughput
    ≈
Tensor-Core GEMM throughput
    ×
memory bandwidth
    ×
software efficiency
```

---

# 6. A useful mental model

Think of CUDA cores as **general-purpose ALUs**.

Tensor Cores are like saying:

> "I know you are going to multiply enormous matrices all day. Here's a factory specifically designed to manufacture matrix products."

For an LLM:

```text
                 Transformer
                     │
          ┌──────────┴──────────┐
          │                     │
       Attention              MLP
          │                     │
      Q @ Kᵀ, P @ V          X @ W
          │                     │
          └──────────┬──────────┘
                     ↓
                   GEMM
                     ↓
               Tensor Cores
```

That's why Tensor Cores matter so much.

---

## 7. But there's an important caveat: memory bandwidth

Tensor Cores aren't magic.

If your operation is **memory-bound**, having 10× more Tensor Core FLOPS doesn't necessarily make it 10× faster.

For example:

```text
GPU computes:
    1000 TFLOP/s

but memory system can only feed it:
    100 GB/s

→ Tensor Cores sit idle
```

This is why LLM performance involves a dance between:

* compute throughput
* HBM bandwidth
* cache
* kernel fusion
* arithmetic intensity
* quantization
* batch size
* sequence length

And this is also why your P100 is interesting despite lacking Tensor Cores: **732 GB/s HBM2 bandwidth is still pretty damn good for ¥400.**

For **large GEMMs**, though, V100's Tensor Cores completely change the equation.

### The punchline

If you're doing:

```text
CUDA programming
FP32 scientific compute
memory-bandwidth experiments
cheap 16GB GPU experiments
```

P100 @ ¥400 = **great toy**.

If you're doing:

```text
LLM training
LLM fine-tuning
large FP16/BF16 GEMMs
```

then:

```text
P100  ← 🐢
V100  ← 🚀
A100  ← 🚀🚀🚀
H100  ← 🚀🚀🚀🚀
```

even when their raw CUDA-core counts don't look dramatically different.

I can also break down **one actual `torch.matmul()` from Python → CUDA kernel → Tensor Core instruction**, which makes the P100 vs V100 difference very concrete.
