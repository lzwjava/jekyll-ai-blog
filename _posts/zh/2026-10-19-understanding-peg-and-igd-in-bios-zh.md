---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解BIOS中的PEG与IGD
translated: true
type: note
---

在BIOS中，“Initiate Graphic Adapter”设置下的**PEG**和**IGD**是什么意思？

---

答案：

**“Initiate Graphic Adapter”**（也称*Primary Display*、*Init Display First*或*Initial Display Output*，因主板品牌而异）是一个BIOS/UEFI设置，用于控制**系统在启动时首先初始化哪个图形适配器**。

两个主要选项是：

| 选项 | 全称 | 含义 |
|------|------|------|
| **PEG** | PCI Express Graphics | 使用插入PCIe插槽的**独立（专用）GPU**（例如NVIDIA GeForce、AMD Radeon） |
| **IGD** | Integrated Graphics Device | 使用CPU或主板芯片组内置的**集成图形**（例如Intel UHD Graphics、AMD Radeon integrated） |

**何时选择哪个：**

- **PEG** — 当您安装了独立显卡并希望它从启动一开始就处理显示输出时选择此项。例如，在MSI固件上，此设置路径为：*Settings → Advanced → Integrated Graphics Configuration → Initiate Graphic Adapter → PEG*。

- **IGD** — 当您希望优先初始化集成显卡时选择此项。如果将优先级设置为PEG（Offboard），系统将跳过IGD初始化，这意味着集成GPU甚至可能不会出现在设备管理器中。

**实用提示：** 如果您将IGD设置为主适配器，但显示器连接到独立GPU，则在启动期间将无法显示——只有在操作系统加载后，独立显卡才会接管。请始终将显示器连接到设置为主适配器的图形适配器。

---

参考资料：

- [Initiate Graphic Adapter – PEG vs IGD (cloudspress.com)](https://www.cloudspress.com/?p=813460)
- [如何在BIOS中更改默认显示适配器 (freedom251.com)](https://www.freedom251.com/?p=456)
- [MSI BIOS – Initiate Graphic Adapter 设置 (yomotherboard.com)](https://www.yomotherboard.com/question/how-can-i-stop-my-bios-from-using-onboard-graphics/)
- [Supermicro FAQ – IGD 初始化优先级 (supermicro.com)](https://www.supermicro.com/zh_tw/support/faqs/faq.php?faq=16307)