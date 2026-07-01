---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B200 计算能力为 sm_100
translated: true
type: note
---

问题：NVIDIA B200 的计算能力是 sm_80 吗？

答案：

不是。B200（Blackwell 数据中心 GPU）的计算能力为 **sm_100**（计算能力 10.0）。

相关架构的快速对照表：

| GPU | 架构 | 计算能力 | `-arch` 标志 |
| ----- | ------ | ---------- | -------------- |
| A100 | Ampere | 8.0 | `sm_80` |
| RTX 30xx | Ampere | 8.6 | `sm_86` |
| RTX 40xx（你的 4070） | Ada Lovelace | 8.9 | `sm_89` |
| H100 / H200 | Hopper | 9.0 | `sm_90` / `sm_90a` |
| B100 / B200 | Blackwell | 10.0 | `sm_100` / `sm_100a` |
| RTX 50xx（消费级 Blackwell） | Blackwell | 12.0 | `sm_120` |

因此，`sm_80` 对应的是 **A100**（及其他 GA100 类部件）。B200 需要 `sm_100`，编译时需要 CUDA 12.8 或更高版本。

注意消费级与数据中心 Blackwell 的区别：数据中心 B200 是 `sm_100`，但消费级 RTX 50 系列 Blackwell 是 `sm_120` —— 两者功能集不同（例如，`sm_100a` 等 `a` 变体暴露了架构特定功能，如用于前沿 GEMM 内核的第五代 Tensor Core / tcgen05 指令）。

如果你正在 MI300X 机器上为 B200 编译代码——这是不可能的，因为 MI300X 是 AMD/ROCm 平台。对于 AMD MI300X，等效的目标是 `gfx942`。
