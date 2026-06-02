---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-sonnet-4
title: Linux版Firefox窗口检测工具
translated: true
type: note
---

除了 `xdotool`，在 Linux 上还有多种替代工具和方法可用于获取活动 Firefox 窗口信息：

## 替代工具

### 1. **wmctrl**
比 xdotool 更健壮的替代方案：
```bash
# 获取活动窗口
wmctrl -a

# 列出所有窗口详情
wmctrl -l -x

# 专门获取 Firefox 窗口
wmctrl -l | grep -i firefox
```

### 2. **qdbus**（适用于 KDE/Qt 应用程序）
```bash
# 获取活动窗口信息
qdbus org.kde.KWin /KWin activeWindow

# 获取窗口列表
qdbus org.kde.KWin /KWin windows
```

### 3. **xwininfo**
内置的 X11 工具：
```bash
# 交互式窗口选择
xwininfo

# 获取根窗口信息
xwininfo -root -tree | grep -i firefox

# 获取活动窗口（需要知道窗口 ID）
xwininfo -id $(xprop -root _NET_ACTIVE_WINDOW | cut -d' ' -f5)
```

### 4. **xprop**
另一个 X11 工具：
```bash
# 获取活动窗口属性
xprop -root _NET_ACTIVE_WINDOW

# 获取窗口类和标题
xprop -root | grep "_NET_ACTIVE_WINDOW(WINDOW)"
```

## 适用于 Wayland 系统

如果运行的是 Wayland，X11 工具将无法工作。请尝试以下替代方案：

### 5. **swaymsg**（适用于 Sway）
```bash
swaymsg -t get_tree | jq -r '.. | select(.focused? == true)'
```

### 6. **hyprctl**（适用于 Hyprland）
```bash
hyprctl activewindow
```

### 7. **gdbus**（GNOME/GTK）
```bash
gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell --method org.gnome.Shell.Eval "global.get_window_actors()"
```

## Python 解决方案

### 8. **使用 Xlib 的 Python**
```python
from Xlib import X, display
from Xlib.error import XError

def get_active_window():
    try:
        d = display.Display()
        root = d.screen().root

        # 获取活动窗口
        active_window = root.get_full_property(
            d.intern_atom('_NET_ACTIVE_WINDOW'), X.AnyPropertyType
        )

        if active_window:
            window_id = active_window.value[0]
            window = d.create_resource_object('window', window_id)
            window_name = window.get_wm_name()
            return window_name
    except XError:
        return None

print(get_active_window())
```

### 9. **使用 subprocess 的 Python**
```python
import subprocess

def get_firefox_windows():
    try:
        # 使用 wmctrl
        result = subprocess.run(['wmctrl', '-l'],
                              capture_output=True, text=True)
        firefox_windows = [line for line in result.stdout.split('\n')
                          if 'firefox' in line.lower()]
        return firefox_windows
    except FileNotFoundError:
        return "wmctrl not installed"

print(get_firefox_windows())
```

## xdotool 问题排查

"BadWindow" 错误通常意味着：

1. **权限问题**：尝试使用不同权限运行
2. **显示问题**：检查 `$DISPLAY` 是否正确设置
3. **Wayland 冲突**：可能运行的是 Wayland 而不是 X11

检查显示服务器：
```bash
echo $XDG_SESSION_TYPE
loginctl show-session $(loginctl | grep $(whoami) | awk '{print $1}') -p Type
```

## 推荐方法

为了最大兼容性，我推荐按以下顺序尝试：

1. **wmctrl** - 在不同窗口管理器中最可靠
2. **xwininfo + xprop** 组合 - 内置在大多数 X11 安装中
3. **Python 解决方案** - 最灵活且可编程
4. **桌面环境特定工具**（swaymsg、hyprctl 等）

首先尝试 `wmctrl -l | grep -i firefox` - 这通常是替代 xdotool 窗口检测功能最直接的方法。
