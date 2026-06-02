---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Ubuntu 22.04 上安装 Steam
translated: true
type: note
---

问题：如何在 Ubuntu 22.04上安装 Steam？

答案：

在 Ubuntu 22.04 LTS 上安装 Steam 有几种方法。最推荐的方法是使用 Valve 的官方 `.deb` 软件包（获取最新版本）或通过 Snap 软件包（简单且自包含）。来自 Ubuntu multiverse 仓库的 APT 方法可行，但可能会提供一个较旧的安装程序。

### 方法 1：官方 Debian 包（推荐用于最新版本）

这将直接从 Valve 安装完整的 Steam 客户端。

1. 打开终端。
2. 下载最新的 `.deb` 软件包：
   ```
   wget https://steamcdn-a.akamaihd.net/client/installer/steam.deb
   ```
3. 安装它：
   ```
   sudo dpkg -i steam.deb
   ```
4. 修复任何依赖问题（常见）：
   ```
   sudo apt update
   sudo apt install -f
   ```
5. 启动 Steam：
   ```
   steam
   ```
   或在应用程序菜单中搜索 "Steam"。

Steam 将在首次启动时自行更新。

### 方法 2：通过 Snap（最简单，Ubuntu 上预装）

Ubuntu 提倡使用 Snap 版本的游戏。

1. 打开终端。
2. 安装 Steam：
   ```
   sudo snap install steam
   ```
3. 启动它：
   ```
   steam
   ```

### 方法 3：通过 APT（来自 Ubuntu 仓库）

这将从 multiverse 仓库安装一个较旧的 Steam 启动器。

1. 启用 multiverse（如果尚未启用）：
   ```
   sudo add-apt-repository multiverse
   sudo apt update
   ```
2. 安装：
   ```
   sudo apt install steam
   ```
3. 启动：
   ```
   steam
   ```

**注意事项：**
- 为获得最佳性能，请确保您的显卡驱动程序是最新的（例如，如果适用，NVIDIA 专有驱动程序）。
- 首次运行时，Steam 会下载额外的运行时文件。
- 如果出现依赖问题，请运行 `sudo apt install -f`。

参考资料：

- [Steam 官方下载页面](https://store.steampowered.com/about/) (steam.deb 的来源)
- [Ubuntu Packages: steam](https://packages.ubuntu.com/jammy/steam)
- [Ubuntu Blog: Steam Snap](https://ubuntu.com/blog/level-up-linux-gaming-new-steam-snap)
- [LinuxConfig: Install Steam on Ubuntu 22.04](https://linuxconfig.org/how-to-install-steam-on-ubuntu-22-04-jammy-jellyfish-linux)
- [LinuxHint: Install Steam on Ubuntu 22.04](https://linuxhint.com/install-steam-on-ubuntu-22-04/)
