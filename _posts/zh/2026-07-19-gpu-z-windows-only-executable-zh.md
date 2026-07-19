---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU-Z Windows专用可执行文件
translated: true
type: note
---

问题：TechPowerUp GPU-Z，所以只有Windows可执行文件？

答案：是的，官方**TechPowerUp GPU-Z**严格来说是一款**仅限Windows的可执行文件（`.exe`）**。开发者并未提供Linux或macOS的原生版本。

如果你使用的是其他操作系统，虽然无法运行GPU-Z的特定渲染测试，但可以使用以下原生替代工具来获取类似的硬件数据：

* **Linux：**
* **GPU-T：** 一款全新的开源诊断工具，专门设计为Linux下的GPU-Z替代品。它提供详细的规格、传感器以及Resizable BAR检测功能。
* **NVTOP：** 一款命令行工具，可作为GPU的专用任务管理器（支持NVIDIA、AMD和Intel）。

* **macOS：**
* **系统报告：** 点击 **Apple菜单 > 关于本机 > 系统报告 > 图形卡/显示器** 即可查看准确的GPU规格、通道带宽和显存信息。

（注：虽然理论上可以通过WINE等兼容层在Linux上强行打开GPU-Z，但它通常无法与底层硬件组件正确通信，导致数据不准确。）

参考文献：

* [TechPowerUp GPU-Z 官方页面](https://www.techpowerup.com/gpuz/)
* [GitHub上的Linux版GPU-T](https://github.com/lseurttyuu/GPU-T)
