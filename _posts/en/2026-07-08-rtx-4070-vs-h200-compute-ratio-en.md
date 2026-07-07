---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4070 vs H200 Compute Ratio
translated: false
type: note
---

Question: **If an RTX 4070 trains for a month, how does its compute compare with an H200?**

Answer:

The right comparison is **total training compute = TFLOPS × time × utilization**, not just the GPU name.

Approximate FP16/BF16 tensor compute:

| GPU                         | FP16/BF16 Tensor TFLOPS | 1 month theoretical compute |
| --------------------------- | ----------------------: | --------------------------: |
| NVIDIA GeForce RTX 4070     |              ~29 TFLOPS |   ~75.2 million TFLOP-hours |
| NVIDIA H200 Tensor Core GPU |             ~990 TFLOPS |   ~2.57 billion TFLOP-hours |

Calculation:

```
RTX 4070:
29 TFLOPS × 24 × 30
= 20,880 TFLOP-hours

H200:
990 TFLOPS × 24 × 30
= 712,800 TFLOP-hours
```

Ratio:

```
712,800 / 20,880 ≈ 34x
```

So:

**1 month on H200 ≈ 34 months (~3 years) on RTX 4070** in raw BF16 tensor compute.

But real LLM training is more complicated:

* H200 has:

  * 141 GB HBM3e
  * ~4.8 TB/s memory bandwidth
  * much larger batch sizes
  * faster communication in multi-GPU clusters

* RTX 4070 has:

  * 12 GB GDDR6X
  * ~500 GB/s bandwidth
  * tiny memory, often forcing gradient checkpointing, smaller batches, slower kernels

For a **small model (10M–1B parameters)**, the gap can be smaller because:

* you may not saturate H200
* data loading and CPU overhead matter
* single GPU efficiency dominates

For a **1B–7B model**, H200 becomes dramatically better because you can use larger batch sizes and optimized kernels.

A practical example:

Training a 1B parameter model from scratch:

* RTX 4070:

  * possible, but slow
  * maybe weeks/months depending on tokens

* H200:

  * can process vastly more tokens/day
  * but the real advantage comes from scaling: multiple H200s + high bandwidth

So your intuition about "simple training, simple models" is actually important. For experimenting with architectures, tokenizers, data pipelines, CUDA kernels:

**RTX 4070 is excellent.**

For pushing serious pretraining runs:

**H200 is a different class — roughly one H200 replaces dozens of consumer GPUs in training throughput.**

A useful mental model:

```
1 × RTX 4070 month
≈ 0.03 × H200 month

1 × H200 month
≈ 34 × RTX 4070 months
≈ 2.8 RTX 4070-years
```

For learning, the 4070 often gives more insight per dollar. For scaling laws and trillion-token experiments, H200 wins.
