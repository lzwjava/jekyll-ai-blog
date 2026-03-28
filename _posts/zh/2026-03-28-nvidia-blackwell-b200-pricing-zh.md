audio: false
generated: true
image: false
lang: en
layout: post
title: thought
NVIDIA Blackwell B200 Cost and Pricing
translated: false
type: note

问题：NVIDIA Blackwell B200 (380W 版本) 的价格是多少？

回答：带有 **380W TDP** 的 **NVIDIA B200** 是 Blackwell 架构的高能效 PCIe 版本。与功率高达 1,000W 的高功耗 SXM 模块不同，此版本专为标准风冷服务器环境设计。

### 预计购买价格 (2026年)
截至 2026 年初，单卡主要通过 OEM 合作伙伴（如 Supermicro、Dell 和 Gigabyte）提供。虽然 NVIDIA 没有设定消费者 MSRP，但市场挂牌价和企业报价显示了以下范围：

*   **单个 PCIe 卡：** 预计在 **$25,000 至 $32,000** 之间。这比 1,000W SXM 旗舰型号约便宜 20-30%，反映了其较低的峰值性能。
*   **整机 8-GPU 服务器系统：** 完整的机架式服务器（例如 NVIDIA DGX B200）起售价通常在 **$300,000 至 $515,000** 左右，具体取决于 CPU、RAM 和存储配置。

### 云租赁费率 (每 GPU/小时)
对于许多开发者来说，租赁 B200 实例是使用该硬件最便捷的方式。价格虽有波动，但在 2026 年趋于稳定：

| 计费类型 | 价格范围 (每 GPU/小时) | 备注 |
| :--- | :--- | :--- |
| **Spot Instances** | **$2.25 – $3.40** | 最适合非关键、可中断的工作负载。 |
| **On-Demand** | **$4.99 – $6.44** | 无需长期锁定；可在 Runpod 和 Lambda 等平台使用。 |
| **Reserved (1-3 Year)** | **$2.89 – $4.03** | 最适合持续性的企业项目。 |
| **Tier 1 CSPs (AWS/GCP)** | **$14.24 – $18.53** | 成本较高，但包含完整的生态系统集成。 |

### 为什么要选择 380W 版本？
**380W PCIe** 模型受到那些无法支持 1,000W 版本巨大功耗和液冷要求的企业青睐。它仍然配备了 **192GB HBM3e memory** 并支持 **FP4 precision**。与上一代 H100 相比，在推理任务中具有更高的性价（Performance-per-dollar）。

参考资料：
*   [B200 Cloud Pricing: Compare 23+ Providers (2026)](https://getdeploying.com/gpus/nvidia-b200)
*   [NVIDIA B200 Cost Breakdown: Manufacturing vs. ASP](https://siliconanalysts.com/analysis/nvidia-b200-blackwell-cost-breakdown)
*   [NVIDIA B200 Guide: Specs, Benchmarks, and Cloud Pricing](https://www.spheron.network/blog/nvidia-b200-complete-guide/)

如果您正在计划部署，是否需要我为您查找支持这些 380W 卡的风冷服务器机箱的具体技术规格？