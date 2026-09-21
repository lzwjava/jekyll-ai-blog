---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 原生ReBAR在微星B450M迫击炮Max上
translated: true
type: note
---

问题：**如果我想要原生 ReBAR 且不想用 ReBarUEFI，MSI B450M MORTAR MAX 是否是一个好选择？**

答案：**是的，这是一块值得购买的主板，但在付款前请确认 BIOS 版本。**

**MSI B450M MORTAR MAX** 是一款 AM4/B450 主板，MSI 的 BIOS 体系在这一代上支持 Re-Size BAR。MSI 将 Re-Size BAR 列为与 Above 4G Decoding 并列的标准 BIOS 功能。（[MSI][1]）

关键区别在于：

```text
B450M MORTAR MAX
        │
        ├── Above 4G Decoding       ← BIOS 设置
        ├── Re-Size BAR Support     ← BIOS 设置
        │
        └── ReBarUEFI               ← 不需要
```

### 购买二手板前我会检查的事项

请卖家提供以下页面的照片：

```text
BIOS → Advanced → PCIe Sub-system Settings
```

你需要看到：

```text
Above 4G Decoding        [Enabled/Disabled]
Re-Size BAR Support      [Enabled/Disabled/Auto]
```

MSI 当前的 BIOS 文档显示了这一确切的 Re-Size BAR 配置路径。（[MSI][1]）

同时询问 **当前 BIOS 版本**。这很重要，因为 MORTAR MAX 是一款较老的 B450 主板，BIOS 版本决定了 CPU/ReBAR 兼容性。

该主板本身带有一条连接 CPU 的 **PCIe 3.0 x16** 插槽，因此搭配 Ryzen 3000/5000 系列处理器和 RX 6000/RTX 30 系列显卡时，硬件拓扑对于 ReBAR 来说非常合理。（[MSI][2]）

### 对我之前回答的一个修正

我不会再将这款主板仅仅描述为“ReBarUEFI 社区变通方案”板。

更准确的理解是：

> **B450M MORTAR MAX + 合适的原厂 MSI BIOS = 原生 BIOS ReBAR，无需 ReBarUEFI。**

ReBarUEFI 项目中可能仍然包含这款主板的报告，因为该项目追踪了大量历史配置，但这并不意味着在正确更新的原厂 BIOS 上你需要 ReBarUEFI。

### 针对这个特定的二手商品

我会给卖家发消息：

> “请拍一下 BIOS 里 `Above 4G Decoding` 和 `Re-Size BAR Support` 的设置页面，再拍一下 BIOS 版本号。”

如果他们展示了这两个选项，**我认为这块主板符合你的需求。**

有一点需要注意：卖家的描述中完全没有提到 BIOS 版本，所以**不要仅凭这个商品描述就下单**。主板本身没问题，但缺少的是确认 BIOS。

[MSI B450M MORTAR MAX 官方规格](https://www.msi.com/Motherboard/B450M-MORTAR-MAX/Specification?utm_source=chatgpt.com)

[MSI Re-Size BAR BIOS 文档](https://us.msi.com/Landing/msi-click-bios-intel-amd-motherboard?utm_source=chatgpt.com)

[1]: https://us.msi.com/Landing/msi-click-bios-intel-amd-motherboard?utm_source=chatgpt.com "MSI Click BIOS - 为英特尔/AMD 主板提供一键优化，轻松高效"
[2]: https://www.msi.com/Motherboard/B450M-MORTAR-MAX/Specification?utm_source=chatgpt.com "B450 MORTAR MAX | 主板 | MSI 全球"
