---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ASM1083 PCIe转PCI桥
translated: true
type: note
---

**问题：** MSI B85M-E45主板上的ASMedia ASM1083芯片是什么？

**回答：**

MSI B85M-E45主板上的ASMedia ASM1083是一款**PCIe转PCI桥接控制器**——本质上是一颗兼容性芯片，让现代主板能够继续提供传统的PCI插槽。

以下是它的功能及存在原因：

**在MSI B85M-E45上的作用**

Intel B85芯片组是一个原生支持PCIe（PCI Express）的现代平台，但不再内置对传统PCI插槽的支持。微星通过添加ASM1083芯片来弥补这一缺口，使主板在原生PCIe插槽之外，还能包含一个或多个传统的PCI扩展插槽。

**工作原理**

ASM1083是一款x1 PCI Express转32位PCI桥接芯片，使用户能够将传统的并行总线设备连接到先进的串行PCI Express接口。换言之，它将芯片组的一条PCIe通道转换为一个PCI总线，供老式扩展卡使用。

ASM1083是一款符合PCI-SIG PCI Express转PCI桥接规范1.0的PCI Express转PCI正向桥接器。

**主要规格**

- 桥接：x1 PCIe → 32位PCI总线
- 单颗桥接芯片最多支持3个PCI插槽
- 功能包括：支持I²C串行EEPROM、全面的PME（电源管理事件）支持、3.3V/1.2V供电以及传统模式支持

**需要安装驱动吗？**

该芯片无需额外安装驱动即可工作——但通过该芯片桥接的设备（即插在PCI插槽上的板卡）需要安装它们自己的驱动。

**通俗地说：** ASM1083让您B85M-E45主板上的老式PCI插槽能在现代主板上正常工作。如果没有它，主板将只有PCIe插槽。

---

**参考来源：**
- [ASM1083产品页面 – ASMedia Technology](https://www.asmedia.com.tw/product/E8AyQ44sX3zPbruF/2f2yq89xz7URBZqD.html)
- [ASM1083数据手册摘要 – Datasheetcafe](https://www.datasheetcafe.com/asm1083-datasheet-controller/)
- [ASM1083芯片信息 – TheRetroWeb](https://theretroweb.com/chips/5897)
- [ASM1083驱动信息 – OEMDrivers](https://oemdrivers.com/pcie-asmedia-asm1083-pcie-to-pci-bridge)