---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微星MAG B760M迫击炮PCIe 4.0
translated: true
type: note
---

问题：MSI MAG B760M Mortar 主板是否支持 PCIe 4.0？

回答：
是的，MSI MAG B760M Mortar 主板在多个插槽上完全支持 PCIe 4.0：

* **M.2 NVMe 存储：** 其板载的两个 M.2 插槽均支持 PCIe 4.0 x4 速度（最高 64 Gbps），适用于超高速固态硬盘。
* **PCIe 扩展插槽：** 虽然顶部主插槽（PCI_E1）已升级为用于显卡的超高速 **PCIe 5.0 x16**，但底部全长插槽（PCI_E3）以 **PCIe 4.0 x4** 运行。

由于 PCIe 技术具有向下兼容性，您可以安全地在顶部 PCIe 5.0 插槽中使用任何 PCIe 4.0 显卡或扩展卡，并且它将以最大 PCIe 4.0 速度完美运行。

参考资料：

* [MSI MAG B760M MORTAR WIFI 规格 | MSI 官网](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Specification)
* [MSI MAG B760M Mortar 评测 | Tom's Hardware](https://www.tomshardware.com/reviews/msi-mag-b760m-mortar-wifi-review)
