---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DGX Spark 价格 $4,699
translated: true
type: note
---

问题：NVIDIA DGX Spark 的价格是多少？

让我查一下当前定价。问题：NVIDIA DGX Spark 的价格是多少？

答案：

**NVIDIA DGX Spark（Founders Edition）** 目前的建议零售价（MSRP）为 **4,699 美元**。该价格于 2026 年 2 月从 3,999 美元上调至 4,699 美元——涨幅约 18%——原因是全球内存供应紧张。此次涨价未伴随任何硬件变更。

背景价格历史：

- 2025 年 CES（Project Digits 发布）：2,999 美元
- GTC 预订/上市（2025 年 10 月）：3,999 美元
- 2026 年 2 月至今：4,699 美元

更便宜的 OEM 替代方案（采用相同的 GB10 内部配置，通常为 1TB SSD 而非 4TB）：

- ASUS Ascent GX10 —— 约 3,266 美元
- Dell Pro Max GB10、MSI EdgeXpert、Acer Veriton GN100、HP 系列

注意：某些渠道（如 Amazon/Microcenter）在更新前可能仍显示 3,999 美元。

针对您的使用场景——鉴于您已拥有 MI300X（192GB）和 RTX 4070——Spark 的实际瓶颈值得指出：273 GB/s 的内存带宽是大型模型性能的根本限制。MI300X 的 HBM3（约 5.3 TB/s）在训练方面远胜一筹；Spark 仅在 CUDA 原生开发的人机工程学和外形尺寸上占优。

参考文献：

- [NVIDIA DGX Spark 美国市场页面](https://marketplace.nvidia.com/en-us/enterprise/personal-ai-supercomputers/dgx-spark/)
- [Tom's Hardware —— 价格上调至 4,699 美元](https://www.tomshardware.com/desktops/mini-pcs/nvidia-dgx-spark-gets-18-percent-price-increase-as-memory-shortages-bite-founders-edition-now-usd4-699-up-from-usd3-999)
- [ToolHalla —— DGX Spark 2026 完整指南](https://toolhalla.ai/blog/nvidia-dgx-spark-complete-guide-2026)
