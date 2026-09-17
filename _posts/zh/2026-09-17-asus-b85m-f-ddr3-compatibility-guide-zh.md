---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复特斯拉P100 PCI错误
translated: true
type: note
---

问题：华硕 B85M-F 是否使用 DDR3？

答案：**是的。** 华硕 B85M-F 使用 **DDR3 台式机内存**。

* **内存：** 2 × DIMM，DDR3
* **支持频率：** DDR3-1600 / 1333 MHz
* **最大容量：** 16 GB（2 × 8 GB）
* **CPU：** i3-4170，LGA1150
* **GPU：** PCIe x16 → Tesla P100

因此，一根便宜的 **8 GB DDR3 1600 MHz** 内存条就足以开始测试 P100。

我还可以将这款 B85M-F 与你正在专门为 P100 兼容性考虑的 **B85M-VDH、B150M 和 X99 主板**进行对比。