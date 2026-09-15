---
audio: false
generated: true
image: false
lang: zh
layout: post
title: P100没有张量核心
translated: true
type: note
---

**问题：** NVIDIA P100 GPU 是否拥有 Tensor Cores？

**答案：** 不，P100 **没有** Tensor Cores。

NVIDIA Pascal 架构白皮书（GP100）中完全没有记载任何矩阵/张量引擎——只有标准的 CUDA 核心 FP16/FP32/FP64 SIMD 吞吐能力。Tensor Cores 是在下一代架构 **Volta** 中才引入的。

V100（Volta 架构，2017 年）是首款配备 Tensor Cores 的 GPU，每颗 GPU 拥有 640 个 Tensor Cores，而 P100（Pascal 架构，2016 年）**Tensor Cores 数量为 0**。

以下是快速对比：

| 特性 | P100（Pascal） | V100（Volta） |
|---|---|---|
| 架构 | Pascal | Volta |
| 发布年份 | 2016 | 2017 |
| Tensor Cores | ❌ 无 | ✅ 640 |
| CUDA Cores | 3,584 | 5,120 |

因此，Tensor Cores 始于 **V100**，而非 P100。

**参考资料：**
- [Benchmarking the NVIDIA V100 GPU and Tensor Cores](https://link.springer.com/chapter/10.1007/978-3-030-10549-5_35)
- [Tesla V100 vs Tesla P100 – Key differences](https://www.linkedin.com/pulse/tesla-v100-vs-p100-key-differences-deep-narayan-prasad)
- [NVIDIA Tesla P100 16GB Specs](https://gpupoet.com/gpu/learn/card/nvidia-tesla-p100)