---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nvidia GPU维修工具包指南
translated: true
type: note
---

问题：**介绍这个页面：Levirepair的“Nvidia MATS & MODS U盘（含NVMT）”帖子。**

回答：

这本质上是Levirepair论坛上一个**社区维护的NVIDIA显卡GPU维修/VRAM诊断工具包**。

![Image](https://images.openai.com/static-rsc-4/0a9txzFEdY5EeOfS3rDyd3lkUCYUr98hgMBGUDdkL1AaXa3Dmsnuzda_WGAD4uo2pDFJtz2r5XREK3nYbU4En2ZC2mAI7rDHdm59tSwmUtapKUaRX52vwwbFqW0kwp-DI2NhdCyS5uIUBcFa2J9AZBOwf2BNpw7ThVHUaefJUWc-kpVKKdNczTRZvISjRZc2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/g_Iw6v4d9XzTa5U3YF1ZnJTIV2kLaN3iw1UPaTK-IMVk8KkBaka_lGehwepPEAYs7epfxGXH42PP8qZQY_hS-SmYr1f4nj9t18BZVsmAP4obXMLZEsrRdLgwDtoX3bEqgR14ccQGSz5XBB-x4zoPp5OSKeESgLNpcAG-JMhoMUN6iLJuQ0veSlZct60RvnrF?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pDIgSFXpZk4j2xMVLQJmnNJ5ttkqU5OiLA_Ce56mnx1KSNEibBaelV-MxCyl02y4e1hZmXrFv0TtuqLwJd0Cf0KtbkndP3ekYRfdmlvgMUb1sU74cWM_iKKI0S0v4ej8sBGgYZUDNnHsZe-NxGYPP30a4X8e8n1NGhWIqWqTGpzZJlkzNiqcm6BWafmhkQw3?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dS0rPB1ZVoGVMP4_6jbYNkp7GPOG-FzjmZa_1mV14T17pIJ9oFnS9j3LUMYYiOaxIkZwN7BfUWojvLKS89bjVvlFMRVqfkd_mtmANL58tjSYZ2Dr0AnAcQdZ_FFuRQ6gBvpv1Ym9a1yw_SYC0w9MFVP-D0dAZ7L8yO9zWdoOkyVKc7s7pYzQaGiwMqBUKVcu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3gLxDoAXamQ-uJBYwuo0uPdlF1XnbbeRnVAzJ-o6a9Zdr-3Gxn1Hg5kH9nY_XzFST-4wq6QzyTItzjPO1qPf55qroy7N_hwgrKRxwIddzmq1cEhMB5eDbN7Nw0xubSFFpCP49gFFhmeXFg505IP3AfybBe6Jlrgegk6Iv_H31b0ZwxJUUBPoX6x2-965GBo_?purpose=fullsize)

### 包含内容

* **MATS** — NVIDIA GPU内存诊断/测试。帖子描述其仅测试GPU内存。([Levirepair][1])
* **MODS** — 更广泛的GPU测试，包含GPU+内存。([Levirepair][1])
* **NVMT** — NVIDIA相关的底层工具，包含VBIOS/设备信息及分析命令。([Levirepair][1])
* 一个**可启动的Linux USB环境**，包含从老式GT系列到RTX 40系列的多版本MATS/MODS，并附带RTX 50系列相关说明。([Levirepair][1])
* 实用的**VRAM维修笔记**，包括GDDR6/GDDR6X内存布局、Micron零件兼容性、通道映射以及基于温度的测试方法。([Levirepair][1])
* 示例诊断命令，例如：

  ```bash
  mods
  mats
  mats -n 1
  nvmt ts > log.txt
  ```

  帖子还记录了`modsinit`命令，用于在GPU无法输出显示时作为副适配器进行测试。([Levirepair][1])

### 为何值得关注

其价值不在于USB镜像本身，而在于**定位不良VRAM的工作流程**。

例如，帖子描述了使用`-floorsweep`禁用单个内存通道，再逐步组合通道以定位故障区域的方法。其中还包含了GDDR6X映射参考，以及一个用于关联VRAM温度行为与故障的MODS脚本。([Levirepair][1])

因此，我将它归类为：

> **NVIDIA板级GPU诊断（特别是VRAM故障分析与维修）的实战手册+可启动工具包。**

如果你从事**GPU板卡维修、GDDR6/GDDR6X替换、NVIDIA内存通道诊断或GPU测试行为逆向工程**，这份资料尤为相关。

该帖子持续维护中：页面显示更新至**2026年1月**，早期帖子随后于2026年进行了编辑。([Levirepair][1])

[打开原始Levirepair帖子](https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3&utm_source=chatgpt.com)

参考资料：

* [Levirepair — Nvidia MATS & MODS U盘（含NVMT）](https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3&utm_source=chatgpt.com) 
* [Levirepair GPU维修论坛](https://levirepair.eu/infusions/forum/index.php?forum_id=3&viewforum=&utm_source=chatgpt.com) 

[1]: https://levirepair.eu/infusions/forum/viewthread.php?thread_id=3 "Nvidia MATS & MODS USB stick (with NVMT): Forum - Levirepair"