---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU维修中的PEX：PCIe电源轨
translated: true
type: note
---

问题：在此上下文中，PEX 是什么意思？

回答：
在显卡（GPU）维修和硬件工程中，**PEX** 代表 **PCI Express（PCIe）**，特指 **PCIe 主电源域/供电轨**（在 NVIDIA 原理图上常标为 `NVVDD_PEX`、`PEX_VDD` 或 `1.8V PEX`）。

在视频画面中，技术人员正在使用万用表/探针测量技嘉 RTX 3070 板上的元件。在板卡维修术语中，“PEX”通常指以下之一：

* **PEX 供电轨（`PEX_VDD` / `1.8V_PEX`）：** GPU 核心的 PCIe 接口逻辑与主板通信所需的专用供电电压。技术人员在诊断显卡无法被识别或无法启动时，常检查该供电轨是否存在短路、对地阻值是否正确或输出电压是否正常。
* **PCI Express 接口（PCIe）：** NVIDIA 常在板卡丝印标注、原理图和信号名称（例如 PEX_RESET、PEX_CLK）中使用缩写“PEX”来表示与 PCIe 相关的电路。
