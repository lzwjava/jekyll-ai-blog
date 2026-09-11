---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华硕A68HM-E显卡维修测试台
translated: true
type: note
---

**ASUS A68HM-E** 是一款小巧的入门级 **AMD FM2+ micro-ATX 主板**，大约于 2014 年发布。它实际上对于搭建廉价的 **GPU 维修/测试平台** 来说相当有趣，因为它同时拥有 **PCIe x16 和传统 PCI** 插槽。（[ASUS 下载中心][1]）

![Image](https://images.openai.com/static-rsc-4/QeccZqDp66-qdtPkXwMOn-5mygyneJcRrpo7PsKEn9L0-oYhQ4OP2bFQfpDs1VsUw3qAa8Ze34qaXGUbux77mp5Cw3lnGV6HRPARUw0rB7sZ2hA3Ti6tfpc4YKeEK8XPHqPu-22Pe0gQ8xydjcrhgoWCb9Uf87sT5uixN4HXl1NLsxfF9tcXEGAMYhQ7A0nu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/33vo-oCvZKv7iXp4Z9EocpGGHVo5ZAvC60pdqG2hEaRWvgJwp01vcPyRI9xsZEqN2SWVb4pUgxgy723U8Qw39UGpg6nz2qvHdNZlKskFk8U5AoUjot5STWl4T-FIUdIO-c9ld7N5sDPFZqGPn9am_xZPNUWn9807yy3js3mhyiYwyQrXkydm-A1nwISuMNAH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/R-q-C6RqQcDjNAwIvtk4Py-qzZ_lGz23UNIGPjAtazBNgzV_a_vyhbA8IPClBdw0bfICOLU9btQ2Uq6xhatMer1g0VlDYK9Ig03Qq7ir5Y9UxTRFtrcURj3Qu_oDzxqs1o8wpJtia1lBEzT6_WmfazX9IFoh4PEUfI5mYKaMm36-4gjfdt01p5cijmyn1geE?purpose=fullsize)

### 核心规格

| Component        | A68HM-E                |
| ---------------- | ---------------------- |
| CPU socket       | **AMD FM2+**           |
| Chipset          | **AMD A68H FCH**       |
| CPU family       | AMD A-series / Athlon  |
| RAM              | **2 × DDR3 DIMM**      |
| Max RAM          | **32 GB**              |
| RAM architecture | Dual-channel           |
| PCIe GPU slot    | **1 × PCIe x16**       |
| PCIe x1          | **1 × PCIe x1**        |
| Legacy PCI       | **1 × PCI**            |
| SATA             | **4 × SATA 6 Gb/s**    |
| LAN              | Realtek 8111GR Gigabit |
| Audio            | Realtek ALC887         |
| Form factor      | Micro-ATX              |

ASUS 官方列出支持 DDR3-1333/1600/1866/2133 以及通过超频可达 DDR3-2400，最大 32 GB。（[ASUS 下载中心][2]）

### CPU 选择

这是 FM2+ 的有趣之处。

它可以运行以下 CPU/APU：

* **A10-7890K**
* **A10-7850K**
* **A10-6800K**
* **A8-8800**
* **A8-8600**
* **Athlon X4 860K**
* **Athlon X4 880K**
* 各种 A4/A6/A8/A10 芯片

ASUS 官方 CPU 兼容性列表包括直至 **A10-7890K / Athlon X4 880K** 代的处理器。（[ASUS Global][3]）

对于廉价的测试机器，我特别推荐寻找 **Athlon X4 860K/880K** 或 A8/A10 APU。

### 为什么它对您的 GPU 维修工作台很有趣

这块主板具有：

```text
CPU/APU
   │
   ├── DDR3 × 2
   │
   └── PCIe x16 ─────── GPU
        │
        └── PCIe x1

PCI ─────────────── legacy PCI diagnostic cards
```

**PCIe x16 插槽在搭配 FM2+ CPU 时支持 PCIe 3.0**。使用较旧的 FM2 处理器时则会相应受限。（[ASUS 下载中心][1]）

重要的是：

**它仍然有一个物理 PCI 插槽。**

这对于旧诊断硬件、POST 卡、旧网卡等可能很有用。

### 电源接口

主板上重要的电源接口为：

```text
24-pin ATX
   +
4-pin ATX12V CPU
```

手册中的主板布局还提供了：

* CPU_FAN
* CHA_FAN
* SATA6G_1 ~ SATA6G_4
* F_PANEL
* USB 2.0 headers
* front-panel audio
* COM header
* TPM
* CLR_CMOS

手册特别指出了 A68HM-E 布局上的 `F_PANEL`、SATA 和其他接口。（[ManualsLib][4]）

### 一个非常有用的特性

与许多较新的廉价主板不同，这款主板具有：

**PCI + PCIe x1 + PCIe x16。**

因此，对于电子/GPU 维修实验，我认为它是一款 **相当不错的廉价测试主板**，尽管技术上已经过时。

它**不是**一台好的现代计算设备——FM2+ 平台大约是 2014 年的平台——但对于：

```text
GPU power-on testing
PCIe GPU detection
old GPU testing
POST/diagnostic cards
Linux experiments
BIOS experiments
cheap repair bench
```

它完全合理。

ASUS 仍然提供官方的 **A68HM-E 手册和 CPU 支持列表**。（[ASUS Global][5]）

**参考来源：**

* [ASUS A68HM-E Support](https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com)
* [ASUS A68HM Series User Manual](https://dlcdnet.asus.com/pub/ASUS/mb/SocketFM2/A68HM-E/E9808_A68HM_Series_Manual_Print_vendor_only.pdf?utm_source=chatgpt.com)

[1]: https://dlcdnet.asus.com/pub/ASUS/mb/SocketFM2/A68HM-E/E9808_A68HM_Series_Manual_Print_vendor_only.pdf?utm_source=chatgpt.com "A68HM Series specifications summary"
[2]: https://dlcdnets.asus.com/pub/ASUS/mb/SocketFM2/A68HM-E/E9808_A68HM_Series_Manual_Print_vendor_only.pdf?utm_source=chatgpt.com "A68HM Series"
[3]: https://www.asus.com/supportonly/a68hm-e/helpdesk_cpu/?utm_source=chatgpt.com "A68HM-E - Support"
[4]: https://www.manualslib.com/manual/868554/Asus-A68hm-Series.html?utm_source=chatgpt.com "ASUS A68HM SERIES USER MANUAL Pdf Download | ManualsLib"
[5]: https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com "A68HM-E - Support"