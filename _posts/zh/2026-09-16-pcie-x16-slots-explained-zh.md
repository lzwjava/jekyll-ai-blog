---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PCIe x16插槽详解
translated: true
type: note
---

问题：技嘉 **GA-AB350-Gaming 3** 是否有两个 PCIe x16 插槽？

答案：**有。** 它具备：

* **1× PCIe 3.0 x16** — 连接 CPU，完整 x16 带宽
* **1× 物理 PCIe x16，但实际运行在 x4** — 连接芯片组，PCIe 2.0
* **1× 物理 x16，但实际运行在 x1**
* **2× PCIe x1**

所以如果你指的是**两个全尺寸 x16 插槽用于显卡/扩展卡**，答案是：**两个**。但只有第一个在电气规格上真正是 x16；第二个是 **x4**。（[技嘉][1]）

一个重要细节：第二个 x4 插槽与两个 x1 插槽共享带宽。如果这些 x1 插槽被占用，x4 插槽会降级为 **x2**。（[技嘉][1]）

如果你正在考虑将此主板用于**双显卡 / 双 AI 加速卡**，我可以帮你确认 PCIe 通道布局是否实际适用于你的具体显卡。

[1]: https://www.gigabyte.com/us/Motherboard/GA-AB350-Gaming-3-rev-1x/sp?utm_source=chatgpt.com "GA-AB350-Gaming 3 (Rev. 1.x) 主板规格 — 技嘉美国官网"
