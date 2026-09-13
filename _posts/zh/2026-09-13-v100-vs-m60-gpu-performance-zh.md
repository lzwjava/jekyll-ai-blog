---
audio: false
generated: true
image: false
lang: zh
layout: post
title: V100与M60 GPU性能对比
translated: true
type: note
---

**问题：** Tesla V100 的 FP32 计算性能是多少？

**回答：**

无需搜索——V100 的规格是公认的：

| 规格 | Tesla M60 | Tesla V100 | RTX 4070 |
| --- | --- | --- | --- |
| 架构 | Maxwell (2015) | Volta (2017) | Ada Lovelace (2023) |
| CUDA 核心数 | 4,096 | 5,120 | 5,888 |
| **FP32 计算性能** | **~8.1 TFLOPS** | **~15.7 TFLOPS** | **29.15 TFLOPS** |
| **FP16 计算性能** | **~8.1 TFLOPS** | **~125 TFLOPS** | **~116 TFLOPS** |
| 显存 | 16GB GDDR5 | 16GB HBM2 | 12GB GDDR6X |
| 显存带宽 | ~160 GB/s | **900 GB/s** | 504 GB/s |
| Tensor Core | 无 | 640（第1代） | 184（第4代） |
| TDP | ~300W | ~250W | 200W |

**关键观察：**

- 在原始 FP32 性能上，V100（~15.7 TFLOPS）比 M60 大约**快 2 倍**，但仅为 RTX 4070 的 **~54%**。
- V100 **真正的亮点**在于搭载 Tensor Core 的 FP16 性能——约 125 TFLOPS，实际上与 RTX 4070 的 FP16 性能**相当**，且远优于 M60。
- V100 的 **HBM2 显存带宽（900 GB/s）** 是最大的隐藏优势——几乎是 **RTX 4070 的 2 倍**和 **M60 的 5.6 倍**。这对于 LLM 推理至关重要，因为显存带宽通常是瓶颈，而非原始 FLOPS。

**总结：** 对于 AI/LLM 工作负载，800–1000 元人民币的 V100 比 288 元人民币的 M60 更值得购买。尽管在二手市场处于相似价位，但 V100 的带宽和 Tensor Core 优势使其在推理任务中真正更快。
