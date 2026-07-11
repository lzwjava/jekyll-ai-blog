---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI Mortar 前置USB-C接口
translated: true
type: note
---

**问题：** 在这些微星 Mortar / Mortar II 主板照片的右上角、SATA 接口附近可见的黑色方块组件是什么？

**回答：**

那是**前置面板 USB Type-C 内部接头**（微星在 Mortar 系列主板上将其标注为 `JUSBC1`）。

关键识别点：

- **外形** — 与 USB 2.0（`JUSB1/2`）或 USB 3.2 Gen1 Type-A（2×10 针脚、可见排针的接头）的排针接头不同，USB-C 内部接头是一个**单个成型的塑料块**，内部带有键控槽。你看到的正是这个——一个实心黑色方块，而不是一排排针脚。
- **位置** — 在 Mortar / Mortar II 主板上，该接头紧邻 SATA 接口，靠近 `JTPM1` 和 `JFP1`，这与你的两张截图都吻合（在图 1 中，你可以看到 `JTPM1` 和 `JFP1` 标签就在其正下方）。
- **功能** — 它允许你从此接头连接一根线缆到**机箱前面板上的 USB-C 端口**，从而在大多数 B650/B850 Mortar 主板上提供 10Gbps（USB 3.2 Gen 2）的前置 USB-C 连接，或在较旧的 B450/B550 Mortar 主板上提供 5Gbps（Gen1）。

要确认你具体主板版本，请查阅对应 Mortar 芯片组的微星手册——MAG B850M Mortar WIFI 用户指南在其接口表中明确列出了“JUSBC1: USB 10Gbps Type-C® 前置面板连接器”，且与 SATA 和 TPM 接头并列，与你照片中的布局一致。

如果你的机箱有前置面板 USB-C 端口且带有匹配的键控线缆，那么这个接头就是用来插线的。如果你没有 USB-C 前置端口，这个接头就闲置不用——它是可选的，并非主板启动所必需。

参考：

- [MAG B850M MORTAR WIFI 用户指南（PDF）](https://download-2.msi.com/archive/mnu_exe/mb/MAGB850MMORTARWIFI_English.pdf)
- [MAG B550M MORTAR 规格](https://www.msi.com/Motherboard/MAG-B550M-MORTAR/Specification)
