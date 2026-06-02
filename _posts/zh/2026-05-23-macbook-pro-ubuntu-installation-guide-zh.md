---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MacBook Pro Ubuntu 安装指南
translated: true
type: note
---

好问题。以下是实话实说：

**macOS Ventura 13.x 是 MacBookPro14,1 最后一个受支持的版本。** 此后再无安全更新。仅此一点就值得考虑换系统。

**该不该装 Ubuntu？**

**是，如果：**
- 它用作开发/服务器机器（终端、SSH、编码、Docker）
- 你希望感觉更流畅 —— Linux 在这款硬件上明显更轻快
- 你需要持续的安全更新（Ubuntu 24.04 LTS 支持至 2029 年）
- 你不需要 macOS 专属应用（Xcode、iMessage 等）

**否，如果：**
- 用户需要 macOS 应用或苹果生态
- 用户不擅长排查 Linux 驱动问题

**主要坑点：Broadcom WiFi。** MacBookPro14,1 使用 Broadcom BCM43602 WiFi 芯片。Ubuntu 不会自带驱动。你需要：

1. 通过以太网（USB-C 转接器）或手机 USB 共享网络完成安装
2. 然后运行：`sudo apt install bcmwl-kernel-source`

或者在首次安装时使用 USB WiFi 网卡。

**触控板** 能用，但不如 macOS 流畅。**音频、显示、键盘** 都正常工作。

**我的建议：** 如果这是一台备用/开发机器 —— 上 Ubuntu。双核 i5-7360U 配 16GB 内存，在 Ubuntu 上会比 Ventura 快得多。GNOME 甚至更轻量的桌面环境如 XFCE 都会很流畅。

需要我一步步讲解安装步骤，还是你只是在考虑这个想法？
