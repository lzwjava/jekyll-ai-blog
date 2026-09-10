---
audio: false
generated: true
image: false
lang: zh
layout: post
title: X99-A主板传统PCI检查
translated: true
type: note
---

**问题：** X99-A 主板有 PCI 插槽吗？

**回答：**通常 **没有传统 PCI 插槽**。

绝大多数华硕 X99-A 主板配备：

* **PCIe x16 插槽** — 用于显卡
* **PCIe x1 插槽** — 用于小型扩展卡
* **没有旧式 PCI（32位，33 MHz）插槽**

关键区别在于：

```text
Old PCI:
[ PCI ]       ← legacy parallel PCI

PCI Express:
[ PCIe x1 ]
[ PCIe x16 ]  ← GPU
```

因此，如果你问这个问题是因为想使用**旧式 PCI 诊断/测试卡**，X99-A 通常不是好选择。对于显卡维修/测试，**H81/B85/Z97 时代的主板**往往更实用，因为部分型号仍保留传统 PCI 插槽。

如果你指的是特定**华硕 X99-A 版本**，请发一张主板照片给我，我可以识别所有扩展插槽。