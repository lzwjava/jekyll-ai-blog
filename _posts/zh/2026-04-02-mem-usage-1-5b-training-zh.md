---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 1.5B 模型训练内存使用量
translated: true
type: note
---

1.5B 模型的 77GB 内存分解：

| 组件 | 内存 |
|-----------|--------|
| Weights (bf16) | ~3GB |
| Adam states (2 states × fp32 = m & v) | ~12GB |
| Gradients (fp32) | ~6GB |
| **Activations** (batch=16, seq=1024) | **~56GB** |
| **总计** | **~77GB** |

Activations 主导内存占用——这是正常的。每层中每个序列的每个 token 的中间输出累积得很快。在 seq=1024 和 batch=16 的 1.5B model 上，activations 占用 56GB 是预料之中的。

从技术上讲，你可以拟合更大的 **batch**，因为你有 ~66GB 的余量，但更大的 batch 会按比例增加 activations，你可能会 OOM。当前的 77GB 是这个 GPU 的一个很好的甜蜜点。
