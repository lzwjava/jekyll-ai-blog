---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 检测到独立 NVIDIA GPU
translated: true
type: note
---

您的系统配备了一块**独立 NVIDIA GPU**：

| 属性 | 值 |
|---|---|
| **GPU** | NVIDIA GeForce GT 730 (GK208B) |
| **厂商** | ASUS (`1043:84f7`) |
| **PCI 地址** | `01:00.0` |
| **驱动** | `nouveau`（开源） |

它**并非集成显卡**——它位于独立的 PCIe 插槽上，拥有专用的内存区域（128MB + 32MB 可预取，16MB 不可预取），并且系统将显示中断路由至该设备。

如果您希望切换到专有 NVIDIA 驱动，请安装 `nvidia-driver-XXX`（其中 `XXX` 与您的发行版软件包匹配）并重启。加载专有驱动后，`nvidia-smi` 将正常运行。