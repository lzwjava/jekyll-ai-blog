---
audio: false
generated: true
image: false
lang: en
layout: post
title: Compute Is Not the Bottleneck
translated: false
type: note
---

Question: Is the thinking here right — slowing down spending on compute, studying the expensive papers first, and using cheaper GPUs for learning CUDA/GPU fundamentals?

Answer: Yes, the reasoning is mostly right. The important insight is that **compute is not the bottleneck yet; understanding is**.

For a 1.5B model, the expensive part is usually not the raw training run. The expensive part is:

* understanding the architecture choices
* building the training pipeline correctly
* knowing why scaling works
* profiling GPU utilization
* understanding CUDA kernels, memory bandwidth, communication, etc.

A person who understands these can often do more with a $5k GPU than someone blindly burning $50k of H200 time.

The pattern in AI research is usually:

```
paper
  ↓
small reproduction
  ↓
ablation experiments
  ↓
understand bottleneck
  ↓
scale compute
```

Not:

```
rent H200
  ↓
throw 100M tokens
  ↓
hope intelligence appears
```

For example, before scaling a 1.5B model, it is valuable to deeply understand:

* Transformer architecture forward pass:

  ```
  X
   ↓
  Q,K,V projections
   ↓
  Attention(Q,K,V)
   ↓
  MLP
   ↓
  residual + layer norm
  ```

* GPU execution:

  ```
  Python
    ↓
  PyTorch
    ↓
  CUDA kernels
    ↓
  Tensor cores
    ↓
  HBM memory
  ```

* training economics:

  ```
  FLOPs ≈ 6 × parameters × tokens
  ```

  A 1.5B model on 100B tokens:

  ```
  6 × 1.5e9 × 1e11
  = 9e20 FLOPs
  ```

  That is already a serious compute budget.

A good next step with a cheaper GPU:

* train tiny GPTs (10M–100M parameters)
* implement attention yourself
* profile kernels
* learn mixed precision:

  * FP32
  * BF16
  * FP8
* understand memory:

```
GPU memory =
weights
+ gradients
+ optimizer states
+ activations
```

For Adam:

```
weights        2 bytes (bf16)
gradients      2 bytes
m              4 bytes
v              4 bytes

≈ 12 bytes / parameter
```

So:

```
1.5B × 12 bytes ≈ 18GB
```

before activations. This is why even "small" models quickly hit GPU limits.

The "borrow at 9% interest to buy compute" idea is usually negative EV unless you already have:

* a clear experiment
* expected result
* publication/product value
* utilization plan

Compute should amplify a good idea, not replace one.

The more efficient path is:

```
$5k GPU
   ↓
CUDA knowledge
   ↓
small model mastery
   ↓
better architecture/data ideas
   ↓
rent H200/H100 only when needed
```

Many top researchers spent years squeezing performance from small hardware before getting access to giant clusters. The expensive clusters are multipliers; they are not the source of understanding.
