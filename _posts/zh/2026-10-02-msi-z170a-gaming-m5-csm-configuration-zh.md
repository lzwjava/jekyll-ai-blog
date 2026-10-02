---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI Z170A Gaming M5 CSM配置
translated: true
type: note
---

问题：如何在 **MSI Z170A Gaming M5** 上配置 CSM？

回答：在这块主板上，MSI 通过 **Windows OS Configuration** 暴露 CSM，而不是直接显示一个名为“CSM”的菜单。

### 启用 CSM

按 `Delete` 键进入 BIOS：

```text
Settings
  → Advanced
    → Windows OS Configuration
      → Windows 10 WHQL Support
```

设置：

```text
Windows 10 WHQL Support = Disabled
```

MSI 专门针对 **Z170A Gaming M5** 记录了此路径。禁用 WHQL 支持后，即可使用传统/CSM 配置。（[MSI 美国][1]）

然后检查：

```text
Settings
  → Boot
    → Boot Mode Select
```

你应该可以选择传统/UEFI 兼容模式，而不是被锁定为 UEFI。（[MSI 美国][2]）

### 针对你的 M40 实验

我实际上会测试**两种模式**，因为 M40 是较老的 GPU：

**测试 A — 启用 CSM**

```text
Windows 10 WHQL Support = Disabled
Boot Mode               = Legacy + UEFI / CSM
Above 4G Decoding       = Enabled   ← if available
PCI_E1                  = M40
PCIe speed              = Gen2
```

然后测试：

**测试 B — 纯 UEFI**

```text
Windows 10 WHQL Support = Enabled / UEFI
CSM                     = Disabled
Above 4G Decoding       = Enabled
PCI_E1                  = M40
PCIe speed              = Gen2
```

对我之前回答的一个重要更正：**在这一代 MSI BIOS 上，不要先寻找独立的“CSM Support”开关。** 相关控制项是 **Windows 10 WHQL Support / CSM-UEFI mode**。MSI 自己的文档将其描述为 CSM/UEFI 设置。（[MSI 美国][3]）

你的 **Z170A Gaming M5 BIOS 版本也很重要**。MSI 当前的支持页面列出了该主板的 BIOS **7977v1I**。（[au.msi.com][4]）

[1]: https://us.msi.com/faq/2622?utm_source=chatgpt.com "MSI USA | MSI USA"
[2]: https://us.msi.com/faq/2803?utm_source=chatgpt.com "MSI USA | MSI USA"
[3]: https://us.msi.com/support/technical_details/DT_BIOS_Manual?utm_source=chatgpt.com "BIOS Manual"
[4]: https://au.msi.com/Motherboard/Z170A-GAMING-M5/support?utm_source=chatgpt.com "MSI Australia | MSI Australia"
