---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 技嘉X370 Gaming K3 PCIe插槽
translated: true
type: note
---

问题：技嘉 X370 Gaming K3 是否有两个适合安装两张卡的 PCIe 插槽？

答案：**有的。** **GA-AX370-Gaming K3** 具有：

* **1 × PCIe x16** — 电气规格 **x16**，PCIe 3.0
* **1 × PCIe x16 长度插槽** — 电气规格 **x4**，PCIe 2.0
* **3 × PCIe x1 插槽**（[技嘉][1]）

因此，如果你说的“两个 PCIe 插槽”是指**两个全长插槽，可用于 GPU / 加速卡**，那么是的：

```text
GPU / 卡 1 → PCIe x16（x16）
GPU / 卡 2 → PCIe x16（x4）
```

但**它不支持 x8/x8 模式**。第二个插槽仅为 **x4**，如果相关的 x1 插槽被占用，其带宽可能降至 **x2**。（[技嘉][1]）

如果你问这个是因为想安装**两张 GPU / AI 卡**，请告诉我这两张卡的具体型号，我可以检查这块主板是否适合该配置正常运行。我也可以核实卖家关于 BIOS 支持 Ryzen 1–5 代的说法。

[1]: https://www.gigabyte.com/Motherboard/GA-AX370-Gaming-K3-rev-10/sp?utm_source=chatgpt.com "GA-AX370-Gaming K3（Rev. 1.0）主板 - 技嘉全球"