---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 测试用i5-6500集成GPU
translated: true
type: note
---

**问题：英特尔酷睿 i5-6500 是否集成 GPU？**

**答案：是的。** i5-6500（第六代 Skylake）内置集成显卡：

* **集成显卡：** 英特尔高清显卡 530
* **执行单元：** 24 个执行单元
* **基础频率：** 约 350 MHz
* **最大动态频率：** 约 1.05 GHz
* **视频输出：** 取决于主板（HDMI/DVI/DP/VGA）
* **显存：** 动态占用系统内存；无独立显存。

因此，若使用 i5-6500 主板作为 **GPU 维修/测试平台**，您可以拔掉独立显卡，直接通过主板的视频输出启动系统，并单独测试 PCIe 显卡。

例如：

```text
i5-6500
   │
   └── HD Graphics 530
           │
           └── 主板 HDMI/DP/DVI/VGA
```

一个关键细节：**主板必须配备视频输出接口**。CPU 虽集成 GPU，但若无显示接口，则无法直接使用。

您也可以参考一套 **i5-6500 + 廉价 H110/B150 主板** 的 GPU 维修测试配置方案。
