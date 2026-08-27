---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA Quadro 410 端口概述
translated: true
type: note
---

**问题：** NVIDIA Quadro 410 显卡上有哪些端口，特别是靠近 RoHS 合规标签的位置？

**答案：**

NVIDIA Quadro 410 在其挡板上有 **两个显示输出端口**：

1. **1× Dual-Link DVI-I** — 支持最高 2560×1600 @ 60 Hz 分辨率
2. **1× DisplayPort 1.2** — 支持最高 3840×2160 @ 60 Hz 分辨率

根据官方 PNY 数据表，显示接口为：**Dual Link DVI-I（×1）** 和 **DisplayPort 1.2（×1）**。

该显卡还通过 **PCI Express 2.0 ×16** 插槽连接到主板，并且 **无需额外电源连接器** — 因此显卡本身没有 PCIe 电源插头。

**RoHS 标签** 通常印在 PCB 背面或挡板贴纸上。端口（DVI-I 和 DisplayPort）位于 I/O 挡板上，附近即可找到 RoHS/合规标记。

---

**参考文献：**
- [NVIDIA Quadro 410 Official Datasheet (PDF)](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/quadro-product-literature/nv-quadro-410-lr.pdf)
- [PNY Quadro 410 Datasheet (PDF)](https://www.azken.com/download/Nvidia_Quadro_410.pdf)
- [Amazon PNY VCQ410-PB Product Page](https://www.amazon.com/PNY-NVIDIA-VCQ410-PB-Quadro-Profile/dp/B008PK7J8I)