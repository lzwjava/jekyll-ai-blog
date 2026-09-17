---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 适用于Tesla P100的X570主板
translated: true
type: note
---

问题：**我应该为 Tesla P100 PCIe 购买哪款主板？**

答案：**我建议放弃 A68HM-E，购买一款 X570 主板。** 重要的不是 PCIe Gen4 本身，而是**正确的 64 位 PCI 资源分配 / Above 4G Decoding**。NVIDIA 将 P100 PCIe 列为 Gen3 x16、250W 的显卡，其计算模式的 BAR1 为 **16 GB**，这解释了旧主板上资源耗尽的原因。([NVIDIA][1])

### 我的推荐：ASUS TUF Gaming X570-PLUS

### [ASUS TUF GAMING X570-Plus](https://www.newegg.com/asus-tuf-gaming-x570-plus-atx-amd-motherboard-amd-x570-am4/p/N82E16813119198?item=9SIC70UKZU0650&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$197.38*

如果你愿意升级到 **AM4**，我会选择这款。

原因：

* X570 + 现代 AM4 固件
* 为 P100 提供全长 PCIe x16 插槽
* 比 A68 平台更新得多的 PCIe 资源分配
* ASUS 仍在为此主板提供 BIOS 更新；支持页面目前列出了 2026 年 2 月的 BIOS 5044。([ASUS Global][2])
* ASUS 提供了 X570 BIOS 手册/支持文档。([ASUS Global][3])
* 二手市场供应良好

对于 P100，我会这样配置：

```text
BIOS
├── Above 4G Decoding = Enabled
├── CSM                = Disabled
├── Re-Size BAR        = 初始禁用
└── PCIe x16           = Auto / Gen3
```

**初始不要启用 Re-Size BAR。** 先让 P100 仅通过 Above 4G 解码正常运作。

NVIDIA 本身也建议对需要大 PCIe 资源的设备/功能启用 Above 4G Decoding。([NVIDIA Networking][4])

### 更便宜的选择

### [ASRock X570 PRO4](https://www.newegg.com/asrock-x570-pro4-atx-amd-motherboard-amd-x570-am4/p/N82E16813157886?item=9SIC6E1M4H8976&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$147.14*

如果二手价格明显更低，**ASRock X570 Pro4** 是另一个合理的选择。

ASRock 自己的 BIOS 文档明确显示：

```text
BIOS
  → Advanced
    → Chipset Configuration
      → Above 4G Decoding = Enabled
```

这正是我们所需的固件功能。([ASRock][5])

### 我不会再购买旧的 A68/FM2+ 主板

你当前的拓扑结构基本上是：

```text
A68HM-E
   │
   └── 旧 AMD 平台
          │
          └── PCIe
                │
                └── P100
                     └── BAR1 = 16 GB
```

P100 正在向固件请求一个巨大的 MMIO 地址空间：

```text
BAR0    16 MB
BAR1    16 GB    ← 主要部分
BAR3    32 MB
```

在计算模式下。([NVIDIA][1])

这就是为什么我建议把钱花在主板上，而不是试图绕过 A68 BIOS 进行破解。

### 另一个重要点

P100 是 **250W 且被动散热** 的。桌面主板可以电气上运行它，但你的机箱需要强劲的气流直接通过 P100 散热片。NVIDIA 将 PCIe P100 描述为被动散热、全高/双槽卡，需要系统气流。([NVIDIA][6])

所以我的目标构建是：

```text
ASUS TUF X570-PLUS
        │
        ├── Ryzen 5 3600 / 5600
        ├── 32–64 GB DDR4
        ├── Tesla P100 12/16 GB
        ├── NVMe
        └── 650–750 W PSU
```

**如果你告诉我你的预算（$50 / $100 / $150 / $200）以及是否想保留当前的 AMD CPU/内存，我可以缩小到特定的主板 + CPU 组合。**

参考链接：

* [NVIDIA Tesla P100 PCIe specifications](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com)
* [ASUS TUF Gaming X570-PLUS support/BIOS](https://www.asus.com/us/supportonly/tuf%20gaming%20x570-plus/helpdesk_bios/?utm_source=chatgpt.com)
* [ASRock Above 4G Decoding documentation](https://www.asrock.com/support/faq.asp?k=bios&utm_source=chatgpt.com)

[1]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "规格"
[2]: https://www.asus.com/us/supportonly/tuf%20gaming%20x570-plus/helpdesk_bios/?utm_source=chatgpt.com "TUF GAMING X570-PLUS - 支持"
[3]: https://www.asus.com/us/supportonly/tuf%20gaming%20x570-plus/helpdesk_manual/?utm_source=chatgpt.com "TUF GAMING X570-PLUS - 支持"
[4]: https://networking-docs.nvidia.com/doca/archive/2-5-5/features-overview-and-configuration?utm_source=chatgpt.com "功能概述与配置 | DOCA"
[5]: https://www.asrock.com/support/faq.asp?k=bios&utm_source=chatgpt.com "ASRock > 常见问题"
[6]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-p100/pdf/nvidia-tesla-p100-PCIe-datasheet.pdf?utm_source=chatgpt.com "数据表: Tesla P100"
