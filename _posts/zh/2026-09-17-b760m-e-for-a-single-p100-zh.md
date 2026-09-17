---
audio: false
generated: true
image: false
lang: zh
layout: post
title: P100 PEG最大链路速度Gen3
translated: true
type: note
---

问题：**MSI PRO B760M-E 能否与 NVIDIA Tesla P100 良好配合？**

回答：**可以。在搭建这个 P100 平台时，我会选择 B760M-E 而非旧的 A68HM-E。** 关键在于 B760M-E 为 P100 提供了一个现代 CPU 直连的 **PCIe 4.0 x16 插槽**，并且拥有更新的 UEFI/PCIe 平台。微星明确标注主插槽为 CPU 直连的 PCIe 4.0 x16。([微星][1])

### [MSI PRO B760M-E](https://www.newegg.com/msi-motherboards-intel/p/1JW-001M-00GY8?item=9SIC3DRKN71786&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$100.88*

### 针对你的 P100，我会这样配置

```text
CPU:       Intel 12代/13代/14代
GPU:       Tesla P100 PCIe
插槽:      CPU PCIe x16
PCIe 代:  初始设为 Gen3
CSM:       关闭
UEFI:      开启
```

P100 是 **PCIe Gen3 x16** 设备，因此在 B760 的 Gen4 x16 插槽上运行是向后兼容的；如果在 POST 或资源分配上遇到问题，你也可以明确强制设为 Gen3。

### 对我之前回答的一个修正

我不会盲目为 P100 **开启 Above 4G Decoding**。

微星有一份旧但明确的 Tesla/GRID 常见问题说明，指出对于其 Tesla/GRID 配置，**Above 4G Decoding 应禁用**，因为它可能阻止正常显示。([微星加拿大][2])

因此对于 **Tesla P100 特别而言**，我会从以下设置开始：

```text
Above 4G Decoding = 禁用
```

如果 B760M-E 仍然报告 PCI 资源耗尽，那么我们可以尝试开启它，而不是假设应该开启。

### B760M-E 的限制

该主板配置较为基础：

```text
B760M-E
├── 1 × PCIe 4.0 x16   ← P100
├── 1 × PCIe 3.0 x1
├── 1 × M.2
└── 4 × SATA
```

微星确认只有 **一个 x16 插槽** 和一个 x1 插槽。([微星][1])

对于 **单块 P100**，这完全没问题。

如果你有计划类似以下配置：

```text
P100 × 2
P100 × 4
P100 + 10GbE 网卡
P100 + 多个 NVMe 转接卡
```

那么我 **不推荐** 使用 B760M-E。你需要一块拥有更多物理 PCIe 插槽且通道拓扑更好的主板。

### DDR4 与 DDR5 的选择

实际上有两个版本：

**B760M-E DDR5**

```text
2 × DDR5
最大 128 GB
```

([微星][1])

**B760M-E DDR4**

```text
2 × DDR4
最大 64 GB
```

([微星][3])

对于 P100 计算主机，**如果你本就需要购买内存，我会选择 DDR5 版本**。但如果你已经拥有 32/64 GB DDR4，那么 DDR4 版本也完全合理。

### 一个重要事项：CPU

不要因为插槽支持就往这块主板里塞昂贵的 i9。对于单块 P100 的计算主机，类似以下配置：

```text
i5-12400
i5-13400
i5-13500
```

更为合理。

GPU 负责实际的 CUDA 工作；你主要需要 CPU 来喂数据、处理存储/网络 I/O、编译和任务编排。

**所以：B760M-E + i5 + P100 = 合理且实惠的计算主机。**

与你当前的 A68HM-E 相比，架构差异非常显著：

```text
A68HM-E
   ↓
旧的 FM2+ 平台
   ↓
PCI 资源分配问题
   ↓
P100 ❌

B760M-E
   ↓
现代 LGA1700 / B760 UEFI
   ↓
CPU PCIe 4.0 x16
   ↓
P100 PCIe Gen3 x16
   ↓
P100 ✅
```

我会放心尝试用 **B760M-E** 搭配 **单块 P100**。([微星][1])

如果你告诉我 **你目前使用的 CPU 和内存**，我可以给出最省钱的精确 CPU + 主板 + 内存组合，避免购买不必要的部件。

参考资料：

* [MSI PRO B760M-E 规格参数](https://www.msi.com/Motherboard/PRO-B760M-E/Specification) ([微星][1])
* [微星：Tesla/GRID 与 Above 4G Decoding](https://ca.msi.com/faq/2736) ([微星加拿大][2])

[1]: https://www.msi.com/Motherboard/PRO-B760M-E/Specification?utm_source=chatgpt.com "PRO B760M-E"
[2]: https://ca.msi.com/faq/2736?utm_source=chatgpt.com "微星加拿大 | MSI Canada"
[3]: https://www.msi.com/Motherboard/PRO-B760M-E-DDR4/Specification?utm_source=chatgpt.com "PRO B760M-E DDR4"
