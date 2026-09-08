---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 特斯拉M60 14美元定价原因
translated: true
type: note
---

问题：为什么一块 NVIDIA Tesla M60 16GB GPU 只卖 320 元人民币（约 44 美元）——这个价格真实吗？

回答：

是的，320 元（约 44 美元）确实便宜，但对于 2026 年的这张卡来说并不意外。原因如下：

**M60 确实老旧，且对现代 AI 工作负载有限制：**
- 基于 **Maxwell 架构（GM204/GK210——实际上是 Maxwell，不是 Kepler）**，发布于 **2015 年**——已超过 10 年
- 不支持 **FP16 Tensor Core**（该技术在 2017 年的 Volta 架构中才引入）
- 仅支持 **CUDA Compute 5.2**，许多现代 AI 框架正在或已经放弃该版本
- **仅支持 PCIe**，无 NVLink 实现多 GPU 带宽
- 最初设计用于 **VMware vGPU / Citrix 虚拟化**，而非训练工作负载

**为什么供应量大且价格低：**
- 数据中心正在**大规模退役** M60 显卡，升级至 A100/H100/H200 代硬件
- 中国二手 GPU 市场充斥着 M60、K80、P100 等退役数据中心显卡
- 在 **华强北** 或二手平台（闲鱼）上，320 元是这类显卡的典型**批发/批量价格**

**花 320 元实际能得到什么：**
| 特性 | 数值 |
|---|---|
| 显存 | 16GB GDDR5（2×8GB 颗粒） |
| FP32 性能 | 约 7.4 TFLOPS |
| FP16 | 无加速 |
| 功耗 | 约 300W——需要合适的供电支持 |
| 驱动支持 | 仍可工作在 CUDA 11.x–12.x（有限制） |

**总结：** 对于**轻量推理、旧模型微调或虚拟机虚拟化**来说，这是一个合理的便宜选择——但不要指望它能与现代 AI 训练中甚至二手 RTX 3090 竞争。这个价格反映了其年代久远以及数据中心退役带来的大量供应。

---

参考：
- [NVIDIA Tesla M60 规格 — TechPowerUp](https://www.techpowerup.com/gpu-specs/tesla-m60.c2760)
- [NVIDIA Tesla M60 数据表](https://images.nvidia.com/content/pdf/grid/data-sheet/nvidia-tesla-m60-datasheet.pdf)