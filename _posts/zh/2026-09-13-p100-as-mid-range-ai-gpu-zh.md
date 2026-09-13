---
audio: false
generated: true
image: false
lang: zh
layout: post
title: P100作为中端AI GPU
translated: true
type: note
---

无需搜索——P100规格早已明确：

| 规格 | Tesla M60 | Tesla P100 | Tesla V100 | RTX 4070 |
| --- | --- | --- | --- | --- |
| 架构 | Maxwell（2015） | Pascal（2016） | Volta（2017） | Ada Lovelace（2023） |
| CUDA核心 | 4,096 | 3,584 | 5,120 | 5,888 |
| **FP32算力** | **~8.1 TFLOPS** | **~10.6 TFLOPS** | **~15.7 TFLOPS** | **29.15 TFLOPS** |
| **FP16算力** | **~8.1 TFLOPS** | **~21.2 TFLOPS** | **~125 TFLOPS** | **~116 TFLOPS** |
| 显存 | 16GB GDDR5 | 16GB HBM2 | 16GB HBM2 | 12GB GDDR6X |
| 显存带宽 | ~160 GB/s | **~732 GB/s** | **~900 GB/s** | 504 GB/s |
| Tensor Core | 无 | 无 | 640（第1代） | 184（第4代） |
| TDP | ~300W | ~250W | ~250W | 200W |

**关键观察：**

- 就FP32而言，P100（~10.6 TFLOPS）略高于M60，但明显落后于V100。
- 与V100一样，P100的**HBM2带宽（~732 GB/s）**是其最大优势——对推理吞吐量非常有利。
- 然而，P100**没有Tensor Core**，因此FP16仅有~21 TFLOPS（原生FP16，非加速），而V100借助Tensor Core可达~125 TFLOPS。对于AI工作负载来说，这是一个显著的差距。

**该价位段AI/LLM用途排名：**

1. 🥇 **V100** — 综合最佳（Tensor Core + HBM2带宽）
2. 🥈 **P100** — 带宽优秀，无Tensor Core，但推理表现依然扎实
3. 🥉 **M60** — 性能最弱；唯一优势是二手价格极低

P100二手价格通常在**400–700元人民币**之间，价格和性能均介于M60与V100之间——如果本地买不到V100，P100是一个合理的中间选择。
