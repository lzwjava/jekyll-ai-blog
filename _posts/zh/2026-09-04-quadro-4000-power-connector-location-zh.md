---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Quadro 4000 电源接口位置
translated: true
type: note
---

Question: Quadro 4000 的电源接口在哪里？

Answer: 在这款 **Quadro 4000** 上，外部电源接口位于 **卡尾部靠近顶端/边缘的位置**，与显示接口支架相对。它使用 **6-pin PCIe 电源接口**。

在照片中，请查看 **卡的左上区域**：PCB 边缘附近的小型凹槽接口是电源输入，而其他接口则用于 SLI 桥接。

因此，该显卡通过以下方式供电：

1. **PCIe x16 插槽** → 主板供电
2. **6-pin PCIe 电源线** → 电源辅助供电

如果你手边有实际的 Quadro 4000 显卡，**请将两侧/边缘的照片发给我**，我可以指出你具体板卡上的 6-pin 接口位置。