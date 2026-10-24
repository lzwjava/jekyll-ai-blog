---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVFP4：布莱克威尔的4位格式
translated: true
type: note
---

**问题：** 什么是NVFP4——简介？

**答案：**

## 什么是NVFP4？

NVFP4是一种创新的4-bit浮点格式，随NVIDIA Blackwell GPU架构引入。它专门设计用于最大化AI推理效率，同时保持模型准确性。

---

### 位布局

基本的FP4 E2M1格式包含1位符号、2位指数和1位尾数。这仅提供15个可表示的值——远少于FP8或BF16——使得缩放策略至关重要。

---

### 关键创新：两级缩放

仅凭原始的FP4过于粗糙，无法实用。NVFP4通过两级缩放系统解决了这个问题：

1. **块缩放（FP8）：** 每16个FP4 E2M1值共享一个FP8（E8M0）缩放因子。
2. **张量缩放（FP32）：** 可选的外部FP32缩放跨越多个块，实现对激活值的两级缩放。

这提供了跨越FP8动态范围的256个不同的缩放值，使得NVFP4能够表示介于MXFP4的2的幂次网格点之间的值。

---

### 与MXFP4的区别

MXFP4是多供应商联盟标准（OCP MX系列）。NVFP4是NVIDIA为Blackwell选择的格式，但该联盟并未采纳。主要区别：NVFP4使用更小的块（16个元素），而MXFP4使用32个元素，从而实现更细粒度的量化。如果你发布一个量化为NVFP4的模型检查点，AMD MI300硬件需要将其重新打包为MXFP4才能原生执行。

---

### 硬件性能

Blackwell的NVFP4张量核心在相同硬件上的吞吐量是FP8的2倍——而FP8已经是BF16的2倍。因此，NVFP4 → FP8 → BF16在B100/B200上构成了4倍 → 2倍 → 1倍的吞吐量阶梯。

在生产推理中：Blackwell上的峰值吞吐量显示NVFP4相对于FP8运行在3.0倍。

第五代张量核心提供原生NVFP4支持，并带有硬件加速缩放，实现20 PetaFLOPS的FP4性能。

---

### 准确性

FP4仅用16个级别编码每个值。直到最近，这还仅可用于存储；随着NVIDIA的NVFP4格式和Blackwell硬件，它现在支持大模型的完整生命周期——训练、推理，甚至长视频生成——精度接近16位。

例如，在MMLU基准测试中，准确性几乎没有变化：从FP8量化到FP4时，MMLU仅从90.8%下降到90.7%。

---

### 软件生态系统

TensorRT Model Optimizer提供全面的FP4量化工作流程，而vLLM等框架添加了早期NVFP4支持。像DeepSeek-R1、Llama 3.1和FLUX等模型的预量化检查点也在Hugging Face上可用。

---

### 总结表

| 特征 | FP4 (E2M1) | MXFP4 | NVFP4 |
| --- | --- | --- | --- |
| 位宽 | 4 | 4 | 4 |
| 块大小 | 无 | 32 | 16 |
| 块缩放 | 无 | FP8 (E8M0) | FP8 (E4M3) |
| 张量缩放 | 可选 | 无 | 可选 FP32 |
| 准确性 | 较低 | 中等 | 较高 |
| 硬件 | 通用 | 多供应商 | Blackwell原生 |

**参考：**

- [Introducing NVFP4 for Efficient and Accurate Low-precision Inference (Edge AI & Vision)](https://www.edge-ai-vision.com/2025/07/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/)
- [NVFP4 Concept Reference — ZeroEntropy](https://www.zeroentropy.dev/concepts/nvfp4/)
- [The Impact of NVFP4 For LLM Inference — Nota AI](https://blog.nota.ai/insights/nvidia-blackwell-nvfp4)
- [Pushing Intelligence to 4-bit — NVIDIA Research](https://research.nvidia.com/labs/eai/blogs/pushing-intelligence-to-4-bit/)
- [Getting started with NVFP4 inference on NVIDIA DGX B200 — Macnica](https://www.macnica.co.jp/en/business/semiconductor/articles/nvidia/148013/)
