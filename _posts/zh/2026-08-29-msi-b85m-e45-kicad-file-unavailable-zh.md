---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI B85M-E45 KiCad文件不可用
translated: true
type: note
---

**问题：** 哪里可以找到 MSI B85M-E45 主板的 KiCad PCB 文件？

**回答：**

很遗憾，**这个文件不存在，也不可能公开存在**——原因如下：

---

**为什么没有这款主板的 KiCad（或任何开源 PCB）文件：**

MSI 是一家商业公司。B85M-E45 的 PCB 设计文件（原理图、布局、Gerber 文件）属于**专有、闭源且受商业机密保护**。MSI 从未发布过这些文件，也永远不会为这类商业产品发布。这款主板不存在任何公开的 KiCad 文件、Altium 文件或 Eagle 文件。

公开存在的内容包括：

- **用户手册**（连接器引脚定义图、基本布局概览）
- 一些用户在 Badcaps.net 等维修论坛上请求过**板视图**（`.BRD` 文件，用于维修追踪）和**原理图**，但即使在这些论坛上也很难找到，且仅在维修社区内非正式分享

---

**您实际可能寻找的内容及获取途径：**

| 目标 | 寻找内容 | 来源 |
| --- | --- | --- |
| 维修/追踪电源轨 | 板视图（`.BRD`）文件 | Badcaps.net、eevblog 论坛 |
| 了解电路设计 | 原理图 PDF | Badcaps.net 原理图请求帖 |
| 元件位置 | 带连接器布局的用户手册 | ManualsLib、MSI 支持页面 |
| 参考 Intel B85 平台设计 | Intel B85 PCH 参考原理图 | Intel ARK / 开发者资源 |

---

**您能获得的最接近的内容：**

Badcaps.net 社区有专门请求 MSI B85M-E45 原理图和板视图（用于维修目的）的帖子。实际上，这是唯一可能偶尔出现非官方副本的地方。**总而言之：** MSI B85M-E45 的 KiCad PCB 文件根本不存在于公共领域。商业主板设计永远不会开源。对于维修/追踪工作，最佳选择是 Badcaps.net 社区获取板视图文件，或官方手册获取连接器布局参考。
