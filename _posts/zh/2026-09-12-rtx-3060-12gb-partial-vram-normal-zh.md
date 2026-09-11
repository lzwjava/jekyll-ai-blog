---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 3060 12GB 部分显存正常
translated: true
type: note
---

问题：**RTX 3060 12GB 只焊了6颗显存芯片，M2和M5位置空焊——这正常吗？**

回答：**是的，很可能正常。** 这实际上是许多 RTX 3060 12GB 显卡的标准设计。

RTX 3060 12GB 采用：

* **6 × 2GB GDDR6 显存颗粒 = 12GB**
* **192-bit 显存位宽**
* 每颗芯片对应一个 **32-bit 显存通道**
* 因此：`6 × 32-bit = 192-bit`

例如，EVGA RTX 3060 XC 的拆解显示，PCB 上只有 **六颗三星 GDDR6 显存芯片**，另外两个显存位置是空焊的。（[Tom's Hardware][1]）

微星 RTX 3060 12GB 官方也明确标注 **12GB / 192-bit**，PCB 照片同样显示有空焊的显存位置。（[Notebookcheck][2]）

因此，如果你的显卡板子看起来像这样：

```text
M1  [VRAM]
M2  [EMPTY]   ← 正常
M3  [VRAM]
M4  [VRAM]
M5  [EMPTY]   ← 正常
M6  [VRAM]
M7  [VRAM]
M8  [VRAM]
```

并且 GPU-Z 报告：

```text
Memory Size: 12288 MB
Memory Bus Width: 192 bit
```

那么 **很可能没有缺失或损坏。**

实际上，这对显卡维修很有用：**不要自动将空焊的显存焊盘视为缺少组件。** 厂商经常在不同产品/配置中重复使用 PCB。RTX 3060 PCB 系列可能会留出额外的空焊显存位置。（[Tom's Hardware][1]）

如果你能提供一张 **RTX 3060 PCB 上 M1–M8 位置清晰的照片**，我可以判断 **M2/M5 是故意空焊，还是像是被物理移除的芯片**。

参考文献：

* [Nvidia GeForce RTX 3060 评测 / PCB 拆解 — Tom's Hardware](https://www.tomshardware.com/reviews/nvidia-geforce-rtx-3060-review/2?utm_source=chatgpt.com)
* [MSI RTX 3060 GAMING 12G 规格](https://www.msi.com/Graphics-Card/GeForce-RTX-3060-GAMING-12G/Specification?utm_source=chatgpt.com)
* [MSI RTX 3060 PCB 分析 — Notebookcheck](https://www.notebookcheck.net/First-look-at-MSI-s-custom-RTX-3060-PCB-design-for-the-Gaming-X-series.523982.0.html?utm_source=chatgpt.com)

[1]: https://www.tomshardware.com/reviews/nvidia-geforce-rtx-3060-review/2?utm_source=chatgpt.com "EVGA GeForce RTX 3060 XC Teardown - Nvidia GeForce RTX 3060 12GB Review: Hope Springs Eternal - Page 2 | Tom's Hardware"
[2]: https://www.notebookcheck.net/First-look-at-MSI-s-custom-RTX-3060-PCB-design-for-the-Gaming-X-series.523982.0.html?utm_source=chatgpt.com "First look at MSI's custom RTX 3060 PCB design for the Gaming X series - Notebookcheck News"