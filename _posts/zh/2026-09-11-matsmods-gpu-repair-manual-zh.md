---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MATS/MODS GPU维修手册
translated: true
type: note
---

问题：上传的**显卡测试命令手册**对GPU维修，特别是**MATS/MODS**有多大用处？

答案：**对您的GPU维修设置非常有用。** 它本质上是一本实用的MATS/MODS/Tserver现场手册，而不仅仅是通用的GPU基准测试指南。

对您来说最有价值的部分包括：

* **NVIDIA MATS** — 内存测试。手册展示了诸如`./mats -e 10`和`./mats -n 1 -e 5`等命令，并解释了`report.txt`如何标识内存错误。
* **MODS** — 在MATS之前初始化/测试GPU环境。手册明确指出，如果环境无法达到PASS，则可能存在电源/核心/硬件问题，无法正常进入MATS流程。
* **故障VRAM定位** — 它将MATS结果（如`A0`）映射到板上的物理VRAM组织结构。这正是判断需要检查/更换哪个内存芯片时所需的信息。
* **核心与VRAM区分** — 它还记录了一项额外的MODS测试（`gputest.js ... -matsinfo`），帮助区分GPU核心问题与内存问题。
* **AMD支持** — 涵盖了RX 400/500、Vega、RX 5000/6000及Radeon VII，并介绍了AMD的`tserver`/`memfa`工作流程。

### 这改变了我对那台¥208 B75机器的看法

手册本身推荐一个相对简单的Intel平台，**8 GB以上内存**，并且重要的是需要一块支持**多GPU**的主板，这样板载iGPU可以在测试故障独立GPU时提供显示输出。

因此，您提出的设置：

```text
B75
E3-1260L
8 GB DDR3
160 GB SSD
        │
        ├── 主板视频输出 → 显示器
        │
        └── PCIe x16 → 待修GPU
                         │
                    MATS / MODS
```

在概念上**正是该手册所描述的设置类型**。

一个重要限制：手册中记录的NVIDIA支持**最高到RTX 3090**，其指令基于一组特定的较旧MODS/MATS版本。因此，不要假定它能自动处理所有更新的GPU。

对于您的维修学习路径，我对工具的排序如下：

**万用表 → 电源/测试平台 → 示波器 → MATS/MODS → 显微镜/BGA设备**

MATS/MODS特别有价值，因为它让您从**"这个GPU不工作"**转变为更可操作的**"内存测试报告A0错误 → 定位对应的VRAM芯片 → 检查电源/数据线路 → 更换/重新植球 → 重新测试"**。

这是向实际板级GPU维修迈出的一大步，而不仅仅是简单地替换部件。
