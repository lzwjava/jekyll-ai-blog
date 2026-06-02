---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-sonnet-4
title: xdotool命令行自动化指南
translated: true
type: note
---

## 什么是 xdotool？

xdotool 是一个用于 X11（Linux 桌面环境）的命令行自动化工具，它允许您：
- 控制鼠标移动和点击
- 向应用程序发送击键
- 操作窗口（移动、调整大小、聚焦）
- 通过各种条件搜索窗口
- 以编程方式自动化桌面交互

## 安装

```bash
# Ubuntu/Debian
sudo apt install xdotool

# Fedora/RHEL/CentOS
sudo dnf install xdotool

# Arch Linux
sudo pacman -S xdotool

# 从源码安装
git clone https://github.com/jordansissel/xdotool
cd xdotool
make
sudo make install
```

## 核心命令

### 窗口信息命令

#### `getactivewindow`
获取当前活动/聚焦窗口的窗口 ID。
```bash
xdotool getactivewindow
# 输出：52428807（窗口 ID）

# 获取活动窗口的窗口标题
xdotool getactivewindow getwindowname
```

#### `getwindowfocus`
类似于 getactivewindow，但在某些窗口管理器中行为可能不同。
```bash
xdotool getwindowfocus
```

#### `getwindowname`
获取窗口的标题/名称。
```bash
# 获取活动窗口的名称
xdotool getactivewindow getwindowname

# 获取特定窗口 ID 的名称
xdotool getwindowname 52428807
```

#### `getwindowpid`
获取与窗口关联的进程 ID（PID）。
```bash
xdotool getactivewindow getwindowpid
```

#### `getwindowgeometry`
获取窗口的位置和大小信息。
```bash
xdotool getactivewindow getwindowgeometry
# 输出：Window 52428807
#   Position: 100,50 (screen: 0)
#   Geometry: 800x600
```

#### `getdisplaygeometry`
获取屏幕/显示器的尺寸。
```bash
xdotool getdisplaygeometry
# 输出：1920x1080
```

### 窗口搜索与选择

#### `search`
通过各种条件搜索窗口。
```bash
# 按窗口名称/标题搜索
xdotool search --name "Firefox"
xdotool search --name "Terminal"

# 按类名搜索
xdotool search --class "firefox"

# 不区分大小写搜索
xdotool search --name --onlyvisible --maxdepth 1 "terminal"

# 常用搜索选项：
# --name: 搜索窗口标题
# --class: 搜索窗口类名
# --classname: 搜索窗口类实例名
# --onlyvisible: 仅可见窗口
# --maxdepth N: 限制搜索深度
# --limit N: 限制结果数量
# --desktop N: 搜索特定桌面/工作区
```

#### `selectwindow`
交互式窗口选择（点击选择）。
```bash
xdotool selectwindow
# 点击任意窗口获取其 ID
```

### 鼠标控制

#### `click`
模拟鼠标点击。
```bash
# 在当前位置左键点击
xdotool click 1

# 右键点击
xdotool click 3

# 中键点击
xdotool click 2

# 双击
xdotool click --repeat 2 1

# 在特定坐标点击
xdotool mousemove 500 300 click 1

# 带延迟点击
xdotool click --delay 500 1
```

#### `getmouselocation`
获取当前鼠标光标位置。
```bash
xdotool getmouselocation
# 输出：x:500 y:300 screen:0 window:52428807

# 仅获取坐标
xdotool getmouselocation --shell
# 输出：X=500 Y=300 SCREEN=0 WINDOW=52428807
```

#### 鼠标移动
```bash
# 将鼠标移动到绝对位置
xdotool mousemove 500 300

# 相对于当前位置移动鼠标
xdotool mousemove_relative 10 -20

# 在一个命令中移动并点击
xdotool mousemove 500 300 click 1
```

### 键盘输入

#### `key`
向活动窗口发送击键。
```bash
# 发送单个键
xdotool key Return
xdotool key Escape
xdotool key Tab

# 发送组合键
xdotool key ctrl+c
xdotool key ctrl+alt+t
xdotool key shift+F10

# 按顺序发送多个键
xdotool key ctrl+l type "https://google.com" key Return

# 常用键名：
# - 字母：a, b, c, ...（小写）
# - 数字：1, 2, 3, ...
# - 特殊键：Return, Escape, Tab, space, BackSpace, Delete
# - 功能键：F1, F2, ... F12
# - 修饰键：ctrl, alt, shift, super（Windows 键）
# - 方向键：Up, Down, Left, Right
```

#### 文本输入
```bash
# 输入文本（模拟逐个字符输入）
xdotool type "Hello World"

# 在字符间带延迟输入
xdotool type --delay 100 "Slow typing"

# 清除延迟以实现快速输入
xdotool type --clearmodifiers --delay 0 "Fast text"
```

### 窗口操作

```bash
# 聚焦/激活窗口
xdotool windowactivate WINDOW_ID

# 最小化窗口
xdotool windowminimize WINDOW_ID

# 最大化窗口
xdotool windowmaximize WINDOW_ID

# 关闭窗口
xdotool windowclose WINDOW_ID

# 将窗口移动到指定位置
xdotool windowmove WINDOW_ID 100 50

# 调整窗口大小
xdotool windowsize WINDOW_ID 800 600

# 将窗口移动到特定桌面
xdotool set_desktop_for_window WINDOW_ID 2

# 将窗口提升到顶部
xdotool windowraise WINDOW_ID

# 映射（显示）窗口
xdotool windowmap WINDOW_ID

# 取消映射（隐藏）窗口
xdotool windowunmap WINDOW_ID
```

### 高级功能

#### `behave`
设置窗口事件行为（触发器）。
```bash
# 当窗口获得焦点时执行命令
xdotool behave WINDOW_ID focus exec echo "Window focused"

# 当窗口创建时执行
xdotool behave WINDOW_ID create exec "notify-send 'New window'"

# 可用事件：focus, unfocus, mouse-enter, mouse-leave, create, destroy
```

#### `behave_screen_edge`
当鼠标到达屏幕边缘时触发操作。
```bash
# 当鼠标碰到左边缘时执行命令
xdotool behave_screen_edge left exec "echo 'Left edge hit'"

# 可用边缘：left, right, top, bottom
```

## 实用示例

### 基础自动化脚本

#### 打开终端并运行命令
```bash
#!/bin/bash
# 打开终端并运行 ls 命令
xdotool key ctrl+alt+t
sleep 1
xdotool type "ls -la"
xdotool key Return
```

#### 截取活动窗口截图
```bash
#!/bin/bash
WINDOW=$(xdotool getactivewindow)
NAME=$(xdotool getwindowname $WINDOW | sed 's/[^a-zA-Z0-9]/_/g')
import -window $WINDOW "screenshot_${NAME}.png"
```

#### 聚焦特定应用程序
```bash
#!/bin/bash
# 聚焦 Firefox，如果未运行则打开
WINDOW=$(xdotool search --onlyvisible --class "firefox" | head -1)
if [ -n "$WINDOW" ]; then
    xdotool windowactivate $WINDOW
else
    firefox &
fi
```

### 窗口管理脚本

#### 并排平铺窗口
```bash
#!/bin/bash
# 获取屏幕几何信息
eval $(xdotool getdisplaygeometry --shell)
HALF_WIDTH=$((WIDTH / 2))

# 获取两个最近的窗口
WINDOWS=($(xdotool search --onlyvisible --maxdepth 1 "" | tail -2))

# 将第一个窗口定位在左侧
xdotool windowsize ${WINDOWS[0]} $HALF_WIDTH $HEIGHT
xdotool windowmove ${WINDOWS[0]} 0 0

# 将第二个窗口定位在右侧
xdotool windowsize ${WINDOWS[1]} $HALF_WIDTH $HEIGHT
xdotool windowmove ${WINDOWS[1]} $HALF_WIDTH 0
```

#### 居中活动窗口
```bash
#!/bin/bash
WINDOW=$(xdotool getactivewindow)
eval $(xdotool getdisplaygeometry --shell)
eval $(xdotool getwindowgeometry --shell $WINDOW)

NEW_X=$(((WIDTH - WINDOW_WIDTH) / 2))
NEW_Y=$(((HEIGHT - WINDOW_HEIGHT) / 2))

xdotool windowmove $WINDOW $NEW_X $NEW_Y
```

### 应用程序特定自动化

#### 浏览器自动化
```bash
#!/bin/bash
# 打开新标签页并导航
xdotool key ctrl+t
sleep 0.5
xdotool type "github.com"
xdotool key Return
```

#### 文本编辑器自动化
```bash
#!/bin/bash
# 全选并复制到剪贴板
xdotool key ctrl+a
sleep 0.1
xdotool key ctrl+c
```

## 技巧与最佳实践

### 定时与延迟
```bash
# 为慢速应用程序添加延迟
xdotool key ctrl+alt+t
sleep 2  # 等待终端打开
xdotool type "echo hello"

# 使用 xdotool 的内置延迟
xdotool key --delay 100 ctrl+alt+t
```

### 错误处理
```bash
#!/bin/bash
# 在对窗口操作前检查其是否存在
WINDOW=$(xdotool search --name "MyApp" 2>/dev/null)
if [ -n "$WINDOW" ]; then
    xdotool windowactivate $WINDOW
else
    echo "Window not found"
    exit 1
fi
```

### 处理多个窗口
```bash
#!/bin/bash
# 对特定应用程序的所有窗口执行操作
xdotool search --name "Firefox" | while read WINDOW; do
    xdotool windowactivate $WINDOW
    xdotool key F5  # 刷新
    sleep 0.5
done
```

### 调试
```bash
# 启用详细输出
xdotool --verbose key Return

# 获取详细的窗口信息
xdotool search --name "Terminal" getwindowgeometry getwindowname getwindowpid
```

## 常见用例

1. **窗口管理**：以编程方式聚焦、移动、调整窗口大小
2. **应用程序测试**：自动化 GUI 测试场景
3. **演示工具**：自动化幻灯片导航和窗口切换
4. **游戏宏**：自动化重复性游戏任务
5. **无障碍功能**：为残障用户创建自定义输入方法
6. **系统管理**：自动化基于 GUI 的管理任务
7. **开发工具**：与 IDE 和开发工作流集成

## 故障排除

### 常见问题

- **命令不工作**：确保 X11 正在运行（不是 Wayland）
- **权限问题**：某些操作可能需要适当的用户权限
- **窗口未找到**：使用 `xdotool search` 验证窗口是否存在且可见
- **定时问题**：在命令之间添加适当的延迟
- **特殊字符**：对文本输入中的特殊字符使用适当的转义

### 安全考虑

- xdotool 可以控制任何应用程序，请谨慎使用
- 避免运行不受信任的 xdotool 脚本
- 在处理敏感数据的自动化操作中要小心
- 考虑仅在受控环境中使用 `xdotool`

本指南涵盖了 xdotool 的基本和高级功能。尝试这些命令，创建适合您特定需求的强大桌面自动化脚本。
