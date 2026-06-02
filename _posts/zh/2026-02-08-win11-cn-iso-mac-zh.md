---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Mac 上下载 Windows 11 中国版 ISO 镜像
translated: true
type: note
---

Question: 如果我只有 Mac，该如何下载 Windows 11 家庭版（仅限中国）的 ISO 镜像？

Answer:

你可以直接在 Mac 的浏览器上从 Microsoft 官方网站下载官方的 Windows 11 **家庭版（仅限中国）** ISO。以下是详细步骤：

1. 在 Mac 上打开 Safari（或任何浏览器）并访问：
   https://www.microsoft.com/zh-cn/software-download/windows11

2. 向下滚动到 **“下载适用于 x64 设备的 Windows 11 磁盘映像 (ISO)”** 部分。

3. 在版本选择下拉菜单中，选择：
   **Windows 11 家庭版（仅限中国）**
   （这是中国特有的家庭版，与多版本混合的 ISO 是区分开的。）

4. 点击 **“确认”**，然后选择语言：
   通常该版本会预选或默认设为 **中文(简体)**。

5. 选择架构：**64-bit** (x64)。

6. 点击 **“下载”**。ISO 文件（约 5-7 GB）将开始直接下载到你的 Mac。

**重要提示：**

- 此 ISO 专门用于中国家庭版（预配置了中文语言、地区设置以及一些针对中国的功能/应用）。
- 下载时不需要产品密钥，但安装后需要有效的 Windows 11 Home 产品密钥（中国区）进行激活。
- 如果你想在实体 PC 上安装，可以使用 Mac 上的工具如 **balenaEtcher**、**Rufus**（通过 Parallels/VM）或 Terminal 命令 (dd) 将 ISO 制作成可启动的 USB 闪存盘。
- 对于 Mac 上的虚拟机（例如 Parallels、UTM、VMware Fusion），可以直接使用下载好的 ISO。
- Media Creation Tool 仅限 Windows，无法在 macOS 上原生运行，因此直接下载 ISO 是在 Mac 上的最佳官方方法。
- 此方法适用于最新版本（例如截至 2026 年的 25H2）。

如果页面表现不同（例如地区识别问题），请尝试清除浏览器缓存/cookies。中国版会明确列在 zh-cn 页面上。

References:

- [https://www.microsoft.com/zh-cn/software-download/windows11](https://www.microsoft.com/zh-cn/software-download/windows11)
- [https://www.microsoft.com/zh-cn/software-download/windows11arm64](https://www.microsoft.com/zh-cn/software-download/windows11arm64) (如果需要 ARM 版本)
