---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 从MacBook远程桌面到Ubuntu
translated: true
type: note
---

问题：我如何在躺在床上时，不使用 SSH，将我的 MacBook Air M2 仅用作屏幕/显示器，远程访问和控制运行 Ubuntu 的强大台式电脑？

答案：

要实现这一目标——将您的 **MacBook Air M2** 作为显示器和输入设备，通过本地网络（Wi-Fi 或以太网）连接您的 **Ubuntu 台式电脑**——您需要一个**远程桌面解决方案**。这将把 Ubuntu 桌面流式传输到您的 MacBook，并支持鼠标、键盘和触控板控制，将其传递给 PC。感觉会非常接近将 MacBook 直接用作显示器，尽管会存在一些网络延迟（在良好的家庭 Wi-Fi 环境下，尤其是在 5GHz 或有线连接下，延迟会很小）。

MacBook（包括 M2 Air）不支持通过电缆作为物理外部显示器（没有目标显示模式）。所有解决方案都是基于软件的远程访问。

以下是从 macOS 客户端到 Ubuntu 主机实现低延迟图形远程桌面的最佳选择：

### 推荐：Sunshine + Moonlight (性能最佳)
这种组合专为低延迟流媒体设计（最初用于游戏，但非常适合桌面使用）。它利用您的 RTX 4070 GPU 进行硬件编码，提供最流畅的体验。

- **在 Ubuntu PC (主机) 上**：
  - 安装 **Sunshine** (开源服务器)。
  - 遵循官方指南：从 https://github.com/LizardByte/Sunshine 下载 Debian 包或使用 AppImage/Flatpak。
  - Sunshine 包含一个内置的“Desktop”应用程序，用于流式传输整个 Ubuntu 桌面（无需启动游戏）。
  - 将其作为服务运行，用于自动启动。

- **在 MacBook Air M2 (客户端) 上**：
  - 从 https://moonlight-stream.org 或 Mac App Store (Moonlight 应用程序) 安装 **Moonlight** (开源客户端)。
  - 在本地网络上与您的 PC 配对。
  - 选择“Desktop”条目并以全屏模式进行流式传输。

- **优点**：
  - 极低延迟。
  - 出色的视频质量。
  - 通过 NVIDIA GPU 进行硬件加速。
  - 全面支持音频。
  - 免费且开源。

这非常适合您的*高端 PC* 和*卧室使用*。

### 简单替代方案：内置 Ubuntu 远程桌面 (RDP 协议)
Ubuntu 22.04+ 内置的 RDP 支持非常出色（优于 VNC）。

- **在 Ubuntu PC 上**：
  - 进入“设置”>“共享”>“启用共享”。
  - 启用“远程桌面”（使用 RDP）。
  - 设置用户名/密码，如果安全，则启用自动登录。
  - 记下 PC 的 IP 地址（通过终端中的 `ip addr show` 命令）。

- **在 MacBook Air 上**：
  - 从 Mac App Store 下载免费的 **Microsoft Remote Desktop** 应用程序。
  - 添加新连接，输入您的 Ubuntu PC 的 IP 和凭据。
  - 连接并切换到全屏。

- **优点**：
  - Ubuntu 上无需额外安装软件。
  - 良好的性能。
  - 剪贴板/音频共享。
  - macOS 上的原生体验。

### 其他选项
- **NoMachine**：非常快速和可靠。在 Ubuntu 上安装服务器，在 Mac 上安装客户端（个人使用免费）。从 https://www.nomachine.com 下载。
- **RustDesk**：TeamViewer 的开源替代品，低延迟，设置简单。跨平台工作良好。

避免使用经典的 VNC（例如 Ubuntu 较旧的屏幕共享）——它的延迟高于上述方法。

### 获得最佳体验的技巧
- 将两台设备连接到同一个快速 Wi-Fi (5GHz) 或使用以太网适配器以获得更低的延迟。
- 在客户端上，启用全屏模式和高比特率/质量设置。
- 确保您的 Ubuntu PC 已登录（或设置自动登录）以实现无缝访问。
- 为了床上舒适度：将 MacBook 支在枕头/支架上，使用全屏模式，并调整亮度。

Sunshine + Moonlight 将为您提供最接近“仅仅是一个显示器”的感觉，因为它具有游戏级别的低延迟。

参考资料：

- https://github.com/LizardByte/Sunshine
- https://moonlight-stream.org
- https://www.nomachine.com
- https://ubuntu.com/tutorials/access-remote-desktop