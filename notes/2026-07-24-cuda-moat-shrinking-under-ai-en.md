---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA Moat Shrinking Under AI
translated: false
type: note
---

## Question: Why did Liang Wenfeng say NVIDIA's CUDA moat is losing? Is the argument technically correct?

## Answer:

The core idea is **not that CUDA disappears tomorrow**, but that the **marginal advantage of CUDA may shrink because AI is moving from human-written GPU kernels toward AI-generated optimized code + higher-level compiler stacks**.

However, the quoted article mixes real technical trends with exaggerated claims.

Let's break it down.

---

## 1. Why CUDA became NVIDIA's moat

CUDA's moat is not just "a programming language".

It is a whole stack:

```
AI developer
    |
PyTorch / TensorFlow / JAX
    |
CUDA libraries
    |
cuBLAS / cuDNN / NCCL / TensorRT
    |
CUDA compiler + runtime
    |
NVIDIA GPU hardware
```

The important parts:

### a. Kernel ecosystem

For example:

```python
torch.matmul(A, B)
```

looks simple.

But underneath:

```
torch.matmul
    |
cuBLAS
    |
CUDA kernels
    |
Tensor cores
    |
GPU memory hierarchy
```

NVIDIA spent 15+ years optimizing these.

---

### b. Developer familiarity

Millions of engineers know:

```cpp
__global__ void kernel(...)
{
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
}
```

but not:

* ROCm HIP
* Ascend C
* TPU XLA
* custom accelerator ISA

Migration cost is huge.

---

## 2. Why Liang thinks CUDA moat is weakening

The key argument:

> AI itself can automate the thing that created CUDA's moat.

Historically:

```
Need new hardware support

        ↓

Need CUDA experts

        ↓

Need months of kernel optimization

        ↓

CUDA ecosystem wins
```

But now:

```
New chip

   ↓

LLM generates kernels

   ↓

Compiler optimizes

   ↓

Much faster porting
```

Example:

A human CUDA expert writes:

```cuda
__global__
void fused_attention(...)
```

Maybe takes weeks.

A coding agent can generate:

```python
triton kernel
```

or:

```cpp
hip kernel
```

in minutes, then benchmark automatically.

---

This is the real threat.

Not:

> "CUDA code is useless"

but:

> "The human expertise accumulated around CUDA becomes less scarce."

---

## 3. Why TileLang matters

TileLang is part of a bigger trend:

```
CUDA C++
     |
     |
Triton
     |
     |
Tile abstraction languages
     |
     |
Compiler automatically maps to hardware
```

The future may look more like:

```
Developer writes:

attention(Q,K,V)

        |

Compiler decides:

NVIDIA GPU?
AMD GPU?
Huawei Ascend?
TPU?

        |

Generate optimized kernel
```

Similar to how C replaced assembly.

Nobody writes x86 assembly for normal applications today.

---

## 4. But is CUDA really dying?

No.

The stronger statement is:

> CUDA's absolute dominance may weaken.

Not:

> CUDA disappears.

A good analogy:

### Intel x86

In 2000:

```
x86 = everything
```

Today:

```
ARM
RISC-V
Apple Silicon
```

exist.

But x86 still dominates servers.

---

CUDA could become like x86:

```
less monopoly
still huge ecosystem
```

---

## 5. The "AI writes CUDA" argument has a weakness

Writing kernels is only part of the problem.

The difficult part:

### Hardware architecture knowledge

Example:

H100:

```
132 SM
80GB HBM3
3.35TB/s bandwidth
Transformer Engine
FP8 Tensor Core
NVLink
```

A good kernel needs understanding:

* occupancy
* memory coalescing
* shared memory
* warp scheduling
* tensor core instructions
* communication topology

AI-generated code still needs:

```
generate
   |
benchmark
   |
profile
   |
optimize
   |
repeat
```

The compiler/toolchain matters.

NVIDIA has:

* Nsight
* CUTLASS
* cuBLAS
* TensorRT
* NCCL

This is a huge advantage.

---

## 6. Huawei Ascend 950 / GB300 replacement claim

The article says:

> Huawei 950 supernode equals GB300, 4 cards replace 1

This needs caution.

Hardware comparison is not only FLOPS.

AI cluster performance:

```
Training speed =
compute
× memory bandwidth
× communication
× software efficiency
× reliability
```

Example:

A GPU with:

```
1000 TFLOPS
```

can lose against:

```
800 TFLOPS
```

if:

* compiler is worse
* communication is slower
* kernels are immature

The ecosystem matters.

---

## 7. Why NVIDIA's pricing strategy creates risk

This part is more believable.

NVIDIA currently has:

```
Demand >> supply

        ↓

Very high prices

        ↓

Customers search alternatives
```

This creates motivation:

* Google TPU
* AMD MI300/MI400
* Huawei Ascend
* AWS Trainium
* Cerebras
* Groq

High margins attract competitors.

---

## 8. DeepSeek's role

DeepSeek's contribution is important.

They showed:

```
Less dependence on brute-force GPU scaling
+
better algorithms
+
better kernels
+
better training efficiency
```

Examples:

* MLA (Multi-head Latent Attention)
* MoE optimization
* FP8 training
* custom kernels

The message:

> Better software can reduce hardware dependence.

This directly attacks NVIDIA's "sell more expensive GPUs" model.

---

## My technical view

The most accurate version of Liang's statement:

> "CUDA's moat is not disappearing, but AI-generated programming, compiler stacks, and specialized accelerators are lowering the cost of escaping CUDA."

I would rate the claims:

| Claim                          | Reality             |
| ------------------------------ | ------------------- |
| CUDA moat is weakening         | ✅ Possible          |
| CUDA will collapse soon        | ❌ Exaggerated       |
| AI can generate kernels        | ✅ True              |
| TileLang/Triton reduce lock-in | ✅ True              |
| Huawei 950 equals GB300        | ⚠️ Needs benchmarks |
| NVIDIA is digging its grave    | Marketing language  |

The biggest long-term battle is probably:

```
CUDA ecosystem
        vs
AI compiler ecosystem
```

The winner may not be the company with the best GPU.

It may be the company whose compiler lets AI automatically generate the best kernels for any chip.
