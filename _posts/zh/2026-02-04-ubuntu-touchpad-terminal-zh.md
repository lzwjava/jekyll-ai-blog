---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 通过终端启用 Ubuntu 触摸板
translated: true
type: note
---

以下是截至 2025–2026 年在 Ubuntu 中通过 Terminal **启用** touchpad 最常用且最新的方法。具体方法取决于你使用的是 **Wayland**（自 Ubuntu 21.10/22.04 起的默认设置）还是 **X11**，以及你的 GNOME 版本。

### Method 1: 通过 Terminal 修改 GNOME settings（推荐 – 同时适用于 Wayland 和 X11）

这是适用于使用 GNOME 的现代 Ubuntu 版本（22.04, 24.04, 24.10, 25.04 等）最干净的方法。

```bash
# 启用 touchpad (正常模式)
gsettings set org.gnome.desktop.peripherals.touchpad send-events enabled
```

其他有用的变体：

```bash
# 禁用 touchpad
gsettings set org.gnome.desktop.peripherals.touchpad send-events disabled

# 智能模式：连接外部鼠标时禁用
gsettings set org.gnome.desktop.peripherals.touchpad send-events disabled-on-external-mouse

# 查看当前设置
gsettings get org.gnome.desktop.peripherals.touchpad send-events
```

此更改会**立即生效**并能在重启后保留。

### Method 2: 使用 `xinput`（仅适用于 X11 会话 – 在旧指南中非常常见）

1. 列出所有输入设备：

```bash
xinput list
```

寻找类似以下的内容：

- SynPS/2 Synaptics TouchPad
- ETPS/2 Elantech Touchpad
- DLL07E4:01 06CB:7E92 Touchpad
- 等等

示例输出片段：

```
⎜   ↳ DLL07E4:01 06CB:7E92 Touchpad          id=12   [slave  pointer  (2)]
```

2. 启用它（将 `12` 替换为你的真实 ID）：

```bash
xinput enable 12
```

或者（更显式的方式）：

```bash
xinput set-prop 12 "Device Enabled" 1
```

如需再次禁用：`xinput disable 12` 或 `... "Device Enabled" 0`

**注意**：这仅在 **X11** 会话中有效。如果你使用的是 Wayland（默认），`xinput` 将无法正确识别或控制 touchpad。

### 快速检查你处于 Wayland 还是 X11 的方法

```bash
echo $XDG_SESSION_TYPE
```

- `wayland` → 使用 Method 1 (`gsettings`)
- `x11`     → 两种方法均可使用

### 如果以上方法都不起作用

极少数情况（driver bug、kernel 问题等）：

```bash
# 重新加载 touchpad kernel module (最常见的)
sudo modprobe -r psmouse
sudo modprobe psmouse proto=imps   # 或 auto, synaptics 等
```

但请先尝试前两种方法 —— 它们能解决 95% 以上的问题。

如果仍然无效，请告知你使用的 Ubuntu 版本以及你处于 Wayland 还是 X11 环境！
