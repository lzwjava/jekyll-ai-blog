---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PCIe插槽区别：x16与x1
translated: true
type: note
---

问：PCIEX_1 和 PCIEX16 有什么区别？

答：

这些标签出现在主板上，指的是 PCIe（PCI Express）插槽，但它们在**通道数量**和**预期用途**上有所不同：

| 特性 | PCIEX16 | PCIEX1 |
|---|---|---|
| 通道数量 | 16 条通道 | 1 条通道 |
| 带宽（PCIe 4.0） | 约 32 GB/s | 约 2 GB/s |
| 物理插槽尺寸 | 长 | 短 |
| 主要用途 | 独立显卡 | 声卡、Wi-Fi 卡、采集卡等 |
| 向后兼容 | 是（可插入 x1 卡） | 是（但仅提供 x1 吞吐量） |

**关键点：**

- **PCIEX16** 是为显卡设计的全带宽插槽，拥有 16 条数据通道以实现最大吞吐量。
- **PCIEX1**（有时标记为 PCIEX_1）仅有 1 条数据通道，带宽低得多。它用于不需要高速的扩展卡，例如网络适配器、USB 扩展卡或音频卡。
- 只要插槽长度足够，任何卡都能物理插入，但仅会以插槽实际通道数的速度运行。
- 在许多主板上，第二个"x16 物理"插槽实际电气连接可能只有 x4 或 x1——务必查阅主板手册确认实际布线通道。

参考文献：
- [PCIe Lanes Explained – What Are They and How Many Do You Need?](https://www.cgdirector.com/pcie-lanes-explained/)
- [PCI Express – Wikipedia](https://en.wikipedia.org/wiki/PCI_Express)