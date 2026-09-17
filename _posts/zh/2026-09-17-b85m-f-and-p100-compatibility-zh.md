---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B85M-F与P100兼容性
translated: true
type: note
---

问题：**华硕 B85M-F + i3-4170** 能否运行 NVIDIA Tesla P100 PCIe？

答案：**可以，可能性很大。** 实际上，这是一套性价比较高的 P100 测试平台。

* **CPU 插槽：** LGA1150；i3-4170 兼容。
* **GPU 插槽：** B85M-F 配备 **1 个 PCIe x16 插槽**，电气规格为 x16。华硕文档显示，根据平台/CPU 不同，该插槽为 PCIe 3.0/2.0 x16。（[华硕下载中心][1]）
* **P100 接口：** Tesla P100 PCIe 采用 **PCIe Gen3 x16**，因此接口匹配。（[NVIDIA][2]）
* **UEFI：** B85M-F 使用华硕 UEFI BIOS，而 P100 的 VBIOS 支持 UEFI。（[华硕下载中心][3]）
* **供电：** 这是关键部分。P100 PCIe 是一款 **250 W 被动散热显卡**，需要 **8-pin 辅助供电接口**。（[NVIDIA][2]）
* **散热：** P100 **采用被动散热**，因此不要在开放式测试平台上裸奔运行，须确保散热片上有强劲气流。NVIDIA 明确规定了散热所需的气流条件。（[NVIDIA 图片][4]）

### 与你之前的 ASUS A68HM-E 问题相比

对于你的 P100 测试，我更推荐这套 **B85M-F + i3-4170**，而不是 A68HM-E。

你之前遇到的 `PCI OUT OF RESOURCES CONDITION` 问题属于 BIOS/PCI 资源分配类问题，而一款采用现代 UEFI 实现的新款 Intel 平台更适合作为测试对象。

B85M-F 同样价格低廉：

> **主板 55 元 + CPU 12 元 = 67 元**

这是一套相当不错的 P100 测试平台。

### 一点注意事项

**P100 并非显示 GPU。** 如果将显示器连接到主板的 VGA/DVI 接口，系统会使用 i3-4170 的 Intel iGPU 负责显示，而 Linux/Windows 可将 P100 用作 CUDA 设备。

大致配置如下：

```text
B85M-F
├── i3-4170
├── 8–16 GB DDR3
├── Intel iGPU → 显示器
└── PCIe x16 → Tesla P100
                     └── 8-pin 供电
```

对于你的具体用途——**P100 CUDA/大语言模型实验及显卡维修/测试**——我认为 **67 元如果能在购买前测试，是值得入手的**。更大的风险不在于 PCIe 兼容性，而在于 **250 W 电源 + 8-pin 供电 + 气流散热**。

另外，如果卖家能帮忙更新 BIOS，建议将 B85M-F 升级到最新 BIOS（**2604**）；华硕将该主板的最终 BIOS 版本列为 2604。（[华硕全球官网][5]）

参考链接：

* [华硕 B85M-F 手册](https://dlcdnets.asus.com/pub/ASUS/mb/LGA1150/B85M-F/E9133_B85M-F.pdf?model=b85mf&utm_source=chatgpt.com)
* [NVIDIA Tesla P100 PCIe 规格](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com)
* [华硕 B85M-F BIOS 支持](https://www.asus.com/supportonly/b85m-f/helpdesk_bios/?utm_source=chatgpt.com)

[1]: https://dlcdnets.asus.com/pub/ASUS/mb/LGA1150/B85M-F/E9133_B85M-F.pdf?model=b85mf&utm_source=chatgpt.com "B85M-F 主板"
[2]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "规格"
[3]: https://dlcdnet.asus.com/pub/ASUS/mb/LGA1150/B85M-F/E9133_B85M-F.pdf?utm_source=chatgpt.com "B85M-F 规格摘要"
[4]: https://images.nvidia.com/content/grid/pdf/DA-09018-001_v10.pdf?utm_source=chatgpt.com "Tesla P100 显卡加速器"
[5]: https://www.asus.com/supportonly/b85m-f/helpdesk_bios/?utm_source=chatgpt.com "B85M-F - 支持"