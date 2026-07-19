---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU-Z 渲染测试详解
translated: true
type: note
---

问题：什么是 GPU-Z 测试？

回答："GPU-Z 测试"通常指 **PCI-Express 渲染测试**，这是免费图形工具 **TechPowerUp GPU-Z** 的内置功能。

现代显卡在桌面闲置时会自动启用省电功能，降低连接速度和 PCIe 通道数（例如从 PCIe x16 4.0 降级到 PCIe x4 1.1）。因此，在无操作状态下查看 GPU-Z 可能会显示不准确的规格参数。

GPU-Z 渲染测试通过强制运行一个小型轻量 3D 窗口来解决此问题。这会给显卡施加轻微负载，使其立即提升至最高性能状态，从而验证显卡是否运行在正确的完整总线宽度和速度上。

### 使用方法

1. 打开 **GPU-Z**。
2. 在主"显卡"选项卡中查看**总线接口**栏。
3. 点击总线接口栏右侧的小**问号 (?)** 图标。
4. 点击**开始渲染测试**。此时会出现一个带动态画面的窗口，同时总线接口数值会更新为实际最高速度。

*注意：GPU-Z 渲染测试仅用于唤醒显卡以检查带宽和基本通道路由，并非高强度压力测试或稳定性基准测试。真正的散热、硬件稳定性或性能压力测试应使用 FurMark 或 3DMark 等工具。*

参考资料：

* [TechPowerUp GPU-Z 主页](https://www.techpowerup.com/gpuz/)