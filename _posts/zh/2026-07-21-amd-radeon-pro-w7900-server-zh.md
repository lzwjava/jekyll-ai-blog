---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD Radeon PRO W7900 服务器
translated: true
type: note
---

以下是完整的服务器规格：

**服务器：u-9758-811746f0（AMD Radeon 云）**

| 组件 | 规格 |
| ----------- | ------ |
| **操作系统** | Ubuntu 24.04.4 LTS |
| **CPU** | 2× AMD EPYC 9334（各 32 核）— **128 线程** |
| **内存** | **503 GiB** |
| **磁盘** | 3.5 TB 叠加存储 + 98 GB /workspace |
| **ROCm** | 驱动 6.16.13 |

**GPU：**

- **架构：** `gfx1100` — **AMD RDNA 3**（Navi 31）
- **计算单元：** 96
- **着色引擎：** 6
- **最大频率：** 1760 MHz
- **显存：** **约 48 GB**（池 1：50,315,264 KB）
- **缓存：** L1=32KB，L2=6MB，L3=96MB
- **温度：** 24°C（空闲）

具备 96 个计算单元和 48 GB 显存，基于 gfx1100，这几乎可以肯定是 **Radeon PRO W7900**（48 GB GDDR6）—— RX 7900 XTX 级别 Navi 31 芯片的工作站变体。非常适合使用 ROCm 进行 LLM 推理/训练。
