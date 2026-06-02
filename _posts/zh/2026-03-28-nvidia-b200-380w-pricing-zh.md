---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 英伟达 B200 380W 预估定价
translated: true
type: note
---

问题：NVIDIA Blackwell B200 (380W 版本) 的价格是多少？

回答：拥有 **380W TDP** 的 **NVIDIA B200** 是 Blackwell 架构中的特定能效版本，通常专为 PCIe 规格或受功耗限制的 Data Center 环境设计。这与旗舰级的 **SXM** 版本有显著不同，后者的功耗最高可达 **1,000W**。

### B200 (380W PCIe) 的估算价格

由于 NVIDIA 主要通过 **OEM 合作伙伴**（如 Dell、HPE 和 Supermicro）销售这些产品，因此没有固定的 MSRP。然而，根据 2026 年目前的 enterprise 列表和市场数据，以下是估算成本：

* **单卡价格：** 普遍估算在 **$25,000 到 $32,000** 之间。较低的功耗和 PCIe 接口通常使其价格略低于高性能的 1,000W SXM 模块（$35,000–$40,000）。
* **系统集成：** 当作为 4-GPU 或 8-GPU 机架式服务器的一部分购买时，由于批量效应，每张卡的实际成本通常会降至 **$25,000** 左右。

### 核心规格对比 (380W vs. 1,000W)

380W 版本针对 **efficiency**（效率）和 **air-cooling**（风冷）进行了优化，而 1,000W 版本通常需要液冷基础设施。

| 特性 | B200 (380W PCIe) | B200 (1,000W SXM) |
| :--- | :--- | :--- |
| **Form Factor** | **PCIe 5.0 Dual-Slot** | **SXM5 Module** |
| **Max TDP** | **380W** | **1,000W** |
| **VRAM** | **192GB HBM3e** | **192GB HBM3e** |
| **FP4 Performance** | 约 4.5 PFLOPS (估算) | **9.0 PFLOPS** |
| **Cooling** | **Air-cooled** (被动散热) | **Liquid-cooled** / 高级风冷 |

### 价格差异的原因

* **可用性：** 虽然 1,000W 单元被优先供应给大规模的 “AI Factories”，但 380W PCIe 卡在 **enterprise edge** 和 **private cloud** 环境中更为常见。
* **Support Packages：** Enterprise 价格几乎总是包含 3 年或 5 年的 **NVIDIA AI Enterprise** 软件许可，这可能会在基础硬件成本上增加 **$2,000–$4,000**。

参考资料：

* [NVIDIA B200 Specs & Price | Jarvislabs](https://jarvislabs.ai/gpu/nvidia-b200)
* [How much does an NVIDIA B200 GPU cost? | Northflank](https://northflank.com/blog/how-much-does-an-nvidia-b200-gpu-cost)
* [NVIDIA B200 GPU Price Comparison - GPUs.io](https://gpus.io/en/gpus/b200)

您是否需要我查找支持 380W PCIe B200 的特定服务器配置（例如 Dell 或 Supermicro 的机型），以查看完整的系统成本？
