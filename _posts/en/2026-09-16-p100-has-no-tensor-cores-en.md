---
audio: false
generated: true
image: false
lang: en
layout: post
title: P100 Has No Tensor Cores
translated: false
type: note
---

**Question:** Does the NVIDIA P100 GPU have Tensor Cores?

**Answer:** No, the P100 does **not** have Tensor Cores.

The NVIDIA Pascal Architecture whitepaper (GP100) documents no matrix/tensor engine at all — only standard CUDA-core FP16/FP32/FP64 SIMD throughput. Tensor Cores were introduced one generation later, in **Volta**.

The V100 (Volta architecture, 2017) was the first GPU to feature Tensor Cores, with 640 of them per GPU, while the P100 (Pascal architecture, 2016) has **0 Tensor Cores**.

Here's a quick comparison:

| Feature | P100 (Pascal) | V100 (Volta) |
| --- | --- | --- |
| Architecture | Pascal | Volta |
| Release Year | 2016 | 2017 |
| Tensor Cores | ❌ None | ✅ 640 |
| CUDA Cores | 3,584 | 5,120 |

So Tensor Cores started with the **V100**, not the P100.

**References:**

- [Benchmarking the NVIDIA V100 GPU and Tensor Cores](https://link.springer.com/chapter/10.1007/978-3-030-10549-5_35)
- [Tesla V100 vs Tesla P100 – Key differences](https://www.linkedin.com/pulse/tesla-v100-vs-p100-key-differences-deep-narayan-prasad)
- [NVIDIA Tesla P100 16GB Specs](https://gpupoet.com/gpu/learn/card/nvidia-tesla-p100)
