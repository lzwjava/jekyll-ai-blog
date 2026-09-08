---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ASUS B150M-ET M2 GPU测试平台
translated: true
type: note
---

## 问题：ASUS B150M-ET M2——这是什么主板？

ASUS **B150M-ET M2** 是一款约 2016 年推出的低端 **micro-ATX LGA1151 主板**，基于 Intel B150 芯片组。对于 **GPU 测试平台**来说，它实际上是一个非常实用的廉价主板选择，尤其是考虑到你一直在搭建的东西。

![Image](https://images.openai.com/static-rsc-4/7L7FEzdi5OdwPRQXkpl00ho4QRmS0J_k63CnJrKswqRGo5D_o454baW3oj6nKBmElEW8CPeF6xeb8TJ2gusik9bjUh1BXbG_RDT_tPNgAZS1YjHwZU4QTgsd23H07upNetQ79tiuKhMMrmhyQzWAAa5aNG8efPxcq_iZ52b5vpnVJh6p5HWqhHcraLduoZz4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/UMGwfOeojvLhrTgaswYXks-TDYxCc6ghoqyZtTWOOBO83Y74dSEuhlMAJkX2vu1bQBta4piwawgWLS_QD70q_5Adr__fg2gtGAuLTQitorlbDDlC0XUrbAsgKl8e_XRc6U5PP4dMQ0Z38zPpdJL1gLqtExbqWcl6VOMkXfnQdQulAJ2RkrVhkJozECSGtUKH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/YzA0aeKbsaa3Bt-_5fT68yVxH37VliuRiAUePMpUs6fdXRD8pG7EyKw1r48j5s_7aGOTfmyO1YSfwmMq3SNqoCRnmxz1xJCsvPh8_ehqP7lsNukJE71si0BkJi2d1YLLEJ5DO1bl1eBphqNMiqSvjatT65hy64QqnCkTwT35O7i4NNJm00iRQ3VgOc94FnuJ?purpose=fullsize)

### 核心规格

| 项目             | B150M-ET M2                 |
| ---------------- | --------------------------- |
| 芯片组           | **Intel B150**              |
| CPU 插槽         | **LGA1151**                 |
| CPU 世代         | 官方支持第 6 代 Skylake     |
| 内存             | **2 × DDR4 DIMM**           |
| 最大内存         | **32 GB**                   |
| GPU 插槽         | **1 × PCIe x16**            |
| 其他 PCIe        | 2 × PCIe x1                 |
| M.2              | **1 × M.2**, 2242/2260/2280 |
| SATA             | **6 × SATA 6 Gb/s**         |
| 网卡             | Gigabit Ethernet            |
| 音频             | Realtek ALC887              |
| 板型             | ~22.6 × 18.5 cm micro-ATX   |

ASUS 的手册确认了 LGA1151 插槽、两个 DDR4 插槽、PCIe x16、两个 PCIe x1 插槽、六个 SATA 接口和 M.2 插槽。（[ASUS Downloads][1]）

### CPU 兼容性

这是重点。

官方支持以下 CPU：

* Core **i3/i5/i7 第 6 代**
* Pentium
* Celeron
* LGA1151 Skylake CPU

例如：

```text
i3-6100
i5-6400
i5-6500
i5-6600
i7-6700
Pentium G4400
Pentium G4500
Celeron G3900
```

官方文档明确列出了第 6 代 Core/Pentium/Celeron 处理器。（[ASUS Download Center][2]）

此外还有后来的 BIOS 更新记录：ASUS 于 2018 年发布了 BIOS 3606，以更新 CPU 微码并提升稳定性/安全性。（[ASUS Mall][3]）

**重要提示：** 不要因为所有第 7 代 Kaby Lake CPU 物理上都是 LGA1151 就认为它们都能用。购买前请查看准确的 CPU 支持列表/BIOS。

### 针对你的 GPU 测试用途

这块板实际上相当有吸引力。

拓扑结构基本上是这样的：

```text
CPU
 │
 └── PCIe x16
       │
       └── GPU
```

所以如果你的目标是：

```text
cheap CPU
+ cheap DDR4
+ B150 motherboard
+ PSU
+ GPU under test
```

你不需要昂贵的 X99/X299 平台。

而且由于它带有 **PCIe x16**，即使 CPU/平台较旧，你仍然可以测试现代 GPU。GPU 会根据平台/设备所支持的 PCIe 代数来运行。

对于 GPU 维修/测试，我其实更喜欢这种简单的 LGA1151 主板，而不是复杂的多 GPU 平台。

### 一个主要问题：没有 I/O 挡板

卖家说：

> **无挡板**

意思是 **后部 I/O 挡板缺失**。

这不是功能性问题。没有它，主板也能完全正常运行。

对于测试台/测试环境：

```text
              GPU
               │
        ┌──────┴──────┐
        │ B150M-ET M2 │
        └─────────────┘
             │
           PSU
```

对于 GPU 维修测试台，我其实**不太在意挡板缺失**。

### M.2 是一个不错的加分项

**M.2 插槽支持 2242 / 2260 / 2280** 规格的硬盘。（[ASUS Downloads][1]）

所以你可以放一块便宜的 NVMe SSD，得到这样的配置：

```text
B150M-ET M2
 ├── LGA1151 CPU
 ├── DDR4
 ├── M.2 SSD
 └── PCIe x16 → GPU under test
```

这是一个非常简洁的测试平台。

### 我的结论

针对你的用途：

**GPU 测试/维修平台：8/10**

**廉价通用 PC：7/10**

**现代游戏 PC：3/10**

**LLM 机器：1/10**

这个平台虽然老旧，但正因为如此它才有用：**便宜、简单、DDR4、LGA1151、PCIe x16、M.2，而且没有不必要的复杂性。**

购买前我最想确认的是**具体售价 + 卖家能否展示 POST/BIOS + CPU 插槽针脚是否干净**。既然商品描述里写着“功能都正常”，我还是想在付款前看到插槽照片和开机进入 BIOS 的画面。

如果你把**实际商品照片**发给我，我可以检查主板状态，并告诉你我会不会买来当 GPU 测试平台。

参考链接：

* [ASUS B150M-ET M2 官方支持](https://www.asus.com/us/supportonly/b150m-et%20m2/helpdesk_manual/?utm_source=chatgpt.com)
* [ASUS B150M-ET M2 用户手册](https://dlcdnet.asus.com/pub/ASUS/mb/LGA1151/B150M-ET_M2_Series/C11414_B150M-ET_M2_UM_6pages_0309.pdf?utm_source=chatgpt.com)
* [ASUS B150M-ET M2 BIOS 历史](https://www.asus.com.cn/supportonly/b150m-et%20m2%20series/helpdesk_bios/?utm_source=chatgpt.com)

我还可以将这块板直接与你的 **ASUS B85 GPU 测试平台**进行对比，告诉你哪个更值得买。

[1]: https://dlcdnets.asus.com.cn/pub/ASUS/mb/LGA1151/B150M-ET_M2_Series/C11415_B150M-ET_M2_V5_UM_6pages_0309.pdf?model=B150M-ET+M2%2FV5&utm_source=chatgpt.com "C11415 / 第一版 / 2016 年 2 月"
[2]: https://dlcdnet.asus.com/pub/ASUS/mb/LGA1151/B150M-ET_M2_Series/C11415_B150M-ET_M2_V5_UM_6pages_0309.pdf?utm_source=chatgpt.com "C11415 / 第一版 / 2016 年 2 月"
[3]: https://www.asus.com.cn/supportonly/b150m-et%20m2%20series/helpdesk_bios/?utm_source=chatgpt.com "B150M-ET M2 SERIES - 服务支持"
