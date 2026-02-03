---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ubuntu GNOME 设置终端命令
translated: true
type: note
---

在 **Ubuntu with GNOME**（自 Ubuntu 17.10+ 以来的默认桌面环境）中，可以通过终端使用以下命令启动图形化的 **Settings** 应用：

```bash
gnome-control-center
```

这将打开主 Settings 窗口（与点击齿轮图标或搜索 "Settings" 的效果相同）。

### 技巧与常用变体

- 直接打开**特定面板**（非常实用！）：

```bash
# Wi-Fi & network
gnome-control-center network

# Bluetooth
gnome-control-center bluetooth

# Sound / audio
gnome-control-center sound

# Displays / monitors
gnome-control-center display

# Power / battery
gnome-control-center power

# Privacy / screen lock
gnome-control-center privacy

# Users / accounts
gnome-control-center user-accounts

# Date & Time
gnome-control-center datetime

# Keyboard / shortcuts
gnome-control-center keyboard

# Mouse & Touchpad
gnome-control-center mouse

# Background / wallpaper
gnome-control-center background

# Notifications
gnome-control-center notifications

# Search for a panel by keyword
gnome-control-center search
```

- 查看**所有可用面板**（不同 Ubuntu 版本可能略有不同）：

```bash
gnome-control-center --list
```

（或者在输入 `gnome-control-center` 加空格后按下 **Tab** 键来自动补全面板名称）

### 如果命令未找到

在标准的 Ubuntu 桌面安装中非常罕见，但你可以（重新）安装它：

```bash
sudo apt update
sudo apt install --reinstall gnome-control-center
```

### 补充说明 (2025–2026 Ubuntu 版本)

- 在 Ubuntu 24.04 LTS、24.10、25.04、25.10 等版本中依然以相同方式工作。
- 如果你**没有**使用 GNOME（例如 KDE、XFCE、Cinnamon 等 Ubuntu 变体），命令会有所不同：
  - KDE Plasma → `systemsettings`
  - XFCE → `xfce4-settings-manager`
  - Cinnamon → `cinnamon-settings`

如果上述方法不起作用，或者你想打开某个非常具体的设置页面，请告知你的 Ubuntu 版本和桌面环境！