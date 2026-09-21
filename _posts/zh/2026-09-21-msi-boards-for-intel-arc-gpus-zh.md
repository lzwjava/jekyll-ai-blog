---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI Intel Arc 显卡主板
translated: true
type: note
---

**问题：** ReBarUEFI 工作主板列表中，哪些 MSI 主板已知可与 Intel Arc 显卡配合使用？

**回答：** 可以。从您列出的 MSI 主板中，以下为相关型号：

| MSI 主板               | Intel Arc / ReBarUEFI 相关性             |
| --------------------- | ------------------------------------------- |
| **Z170-A PRO**        | ✅ 已确认在 ReBarUEFI 工作主板列表中 |
| **Z170A Gaming M5**   | ✅ 已确认                                 |
| **Z270-A PRO**        | ✅ 已确认                                 |
| **Z270 GAMING M5**    | ✅ 已确认                                 |
| **Z97 Gaming 3**      | ✅ 已确认                                 |
| **Z97 Gaming 5**      | ✅ 已确认                                 |
| **B150M Bazooka**     | ✅ 已确认                                 |
| **B150M Plus**        | ✅ 已确认                                 |
| **H110M Gaming**      | ✅ 已确认                                 |
| **C236M WORKSTATION** | ✅ 已确认                                 |
| **H97M-G43**          | ✅ 已确认                                 |

需要区分的重要概念是：**ReBarUEFI 可正常工作 ≠ MSI 官方支持 Intel Arc**。ReBarUEFI 专门用于启用 PCIe Resizable BAR 功能，而 Arc 显卡对该功能有很高的依赖度。

对于 Intel Arc 显卡，我会特别关注 **Z170/Z270 系列 MSI 主板**：

* **Z170-A PRO**
* **Z170A Gaming M5**
* **Z270-A PRO**
* **Z270 GAMING M5**

这些主板比 Z97/H97 型号更新，采用 Intel 100/200 系列平台，因此通常更适合作为 Arc + ReBarUEFI 实验的起点。

有一点需要注意：**Arc 本身的平台要求不仅限于 ReBAR**。Intel 现代 Arc 显卡要求 **UEFI 启动 + Above 4G Decoding + ReBAR**，而较旧的平台还可能遇到 PCIe/固件/CSM 相关的兼容性问题。因此具体的 CPU + Arc 显卡型号组合也会影响兼容性。

如果您正在为 **Arc A770/A750/B580** 等显卡专门挑选主板，我可以将 ReBarUEFI 报告与 Intel Arc 的规格要求进行交叉比对，找出最实用的 MSI 主板，而不仅仅是出现在工作列表中的型号。