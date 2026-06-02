---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 精通macOS自动化缺口
translated: true
type: note
---

现在我已经清楚了。你已经有了 12 个 `ww macos` 命令，覆盖了相当扎实的领域。以下是我对你已有知识的分析，以及哪些开源项目能帮你进一步提升。

---

## 你的代码已经告诉我什么

你熟悉以下内容：
- **plistlib** — 读取二进制 plist（Dock）
- **networksetup** — 系统代理配置
- **pmset** — 电源/电池管理
- **diskutil** — 磁盘枚举
- **sysctl** — 内核参数（hw.memsize, hw.model 等）
- **vm_stat** — 虚拟内存页
- **PyObjC** — `UserNotifications`（toast.py），`CoreText`（list_fonts.py）
- **osascript** — AppleScript 桥接 System Events
- **stat -f** — BSD stat 获取文件时间戳
- **du** — 磁盘使用量

我看到的缺口——没有窗口管理，没有 Accessibility API 使用，没有 `screencapture`，没有 `shortcuts` CLI，没有 IOKit，没有深度使用 `launchctl`。而这些正是有趣的东西所在。

---

## 针对缺口推荐的项目

### 1. yabai — 窗口管理（填补你最大的缺口）

你的 `ww macos open-terminal` 只是打开 Ghostty 窗口。yabai 通过 CLI 和 IPC socket 让你以编程方式控制每个窗口的位置、大小、空间和堆叠。

```bash
# 安装
brew install koekeishiya/formulae/yabai
yabai -m signal --add event=dock_did_restart action="sleep 1; yabai -m config ..."

# 示例：将焦点窗口移到右半屏
yabai -m window --grid 1:2:1:0:1:1

# 示例：以 JSON 格式查询所有窗口
yabai -m query --windows

# 示例：按方向聚焦窗口
yabai -m window --focus east
```

你将学到：macOS Accessibility API、SIP（System Integrity Protection）——yabai 需要部分关闭 SIP 才能使用全部功能，这能让你精确了解 SIP 保护了什么以及如何工作。同时还能从 API 层面学习 macOS Spaces（虚拟桌面）。

https://github.com/koekeishiya/yabai

### 2. skhd — 全局热键守护程序（与 yabai 配合使用）

```bash
brew install koekeishiya/formulae/skhd

# ~/.config/skhd/skhd.conf
alt - h : yabai -m window --focus west
alt - j : yabai -m window --focus south
alt - k : yabai -m window --focus north
alt - l : yabai -m window --focus east
```

你将学到：macOS 如何在系统层面捕获键盘事件（CGEventTap、IOKit HID），以及输入监控权限的工作原理。

https://github.com/koekeishiya/skhd

### 3. screencapture + Shortcuts CLI — 完善你的截图流程

你已经在 `ww note screenshot-log` 中使用了截图 → LLM 视觉分析。但你还没有充分利用 macOS 原生工具的全部能力：

```bash
# screencapture 功能非常强大
screencapture -i ~/Desktop/capture.png          # 交互式选择区域
screencapture -R 0,0,1920,1080 ~/full.png       # 指定区域
screencapture -v ~/capture.mp4                   # 屏幕录制（macOS 15+）
screencapture -C                                 # 捕获光标

# Shortcuts CLI — Apple 的自动化框架
shortcuts list
shortcuts run "Get Text From Image" -i photo.png
shortcuts run "Remove Background" -i photo.png -o output.png

# 以编程方式创建快捷指令
shortcuts create "My Workflow" --workflow workflow.json
```

你将学到：macOS Shortcuts 框架、Quick Actions，以及如何桥接 CLI ↔ GUI 自动化。

### 4. 通过 PyObjC 使用 IOKit — 硬件级访问

你的 `get_system_info.py` 使用了 `sysctl` 和 `system_profiler`。IOKit 可以更深入：

```python
# IOKit 电池信息（原始数据，非 pmset）
import subprocess
import plistlib

# IORegistry — 内核的设备树
result = subprocess.run(
    ["ioreg", "-r", "-c", "AppleSmartBattery", "-a"],
    capture_output=True, text=True
)
# 解析 plist 输出获取：
# - CycleCount, DesignCapacity, MaxCapacity, Temperature
# - Serial, ManufactureDate, CellVoltage

# IOKit 显示器信息
result = subprocess.run(
    ["ioreg", "-r", "-c", "IODisplayConnect", "-a"],
    capture_output=True, text=True
)

# IOKit USB 设备
result = subprocess.run(
    ["ioreg", "-r", "-c", "IOUSBDevice", "-a"],
    capture_output=True, text=True
)
```

你将学到：IORegistry — 内核的设备树。这就是 `system_profiler` 获取数据的方式，但更原始。你可以添加一个比当前 `system-info` 更深入的 `ww macos hardware`。

### 5. launchctl — 进程管理（与你现有的 process_analyze.py 互补）

你的 `process_analyze.py` 使用了 `ps aux` + LLM。但 macOS 的进程管理核心在于 launchd：

```bash
# 列出所有服务（不仅仅是用户代理）
launchctl print system/
launchctl print gui/$(id -u)/

# 关于某个服务的详细信息
launchctl print gui/$(id -u)/com.apple.Spotlight

# 查看服务的 PID、退出状态、上次崩溃时间
launchctl list | grep -v com.apple

# 禁用某个服务（重启后持续生效）
launchctl disable gui/$(id -u)/com.some.background.agent

# 重新启用
launchctl enable gui/$(id -u)/com.some.background.agent

# Kickstart（重启）服务
launchctl kickstart -k gui/$(id -u)/com.apple.Finder
```

你将学到：完整的 macOS 服务生命周期——LaunchDaemons（系统级，root）、LaunchAgents（用户级，每个会话）、XPC 服务，以及 launchd 如何取代了 cron 和 inetd。

一个自然的 `ww macos services` 命令可以列出所有非 Apple 的代理及其状态、上次运行时间和退出码。

### 6. m-cli — 你应该研究的多功能瑞士军刀

不只是使用——要**阅读源码**。它是一个单一的 bash 脚本：

```bash
brew install m-cli
# 源码就在：
cat $(which m)
```

它封装了约 200 个 macOS 管理任务：Airport、蓝牙、DNS、防火墙、Time Machine、FileVault、家长控制、屏幕共享等等。每个命令都能教会你一个之前不知道的原生 macOS 工具。

https://github.com/rgcr/m-cli

### 7. osx-cpu-temp / iStats — 温度监控

```bash
brew install osx-cpu-temp
osx-cpu-temp  # 从 IOKit SMC（系统管理控制器）读取
```

你将学到：SMC（System Management Controller）——管理温度、风扇、电池充电的嵌入式芯片。IOKit SMC 访问让你能够在硬件层面读取 CPU 内部温度、风扇转速和电池健康度。

源码：https://github.com/lavoiesl/osx-cpu-temp

### 8. macos-defaults — 配置目录

```bash
# 每个 macOS `defaults write` 命令，都有文档
open https://github.com/yannbertrand/macos-defaults

# 可以加入 ww 的示例：
defaults read com.apple.dock tilesize              # Dock 图标大小
defaults read -g AppleFontSmoothing                # 字体渲染
defaults read com.apple.finder ShowPathbar         # Finder 路径栏
defaults read com.apple.Spotlight orderedItems     # Spotlight 配置
```

一个能读取/显示/搜索当前非默认设置的 `ww macos defaults` 命令会非常有用。

---

## 我接下来会在 ww 中构建什么

基于你的缺口，以下是最高价值的添加项：

| 命令 | 作用 | 你将学到什么 |
|---|---|---|
| `ww macos services` | 列出非 Apple 的 launchd 代理/守护进程 | launchctl, XPC |
| `ww macos hardware` | 深度的 IOKit 硬件信息（电池循环次数、温度、USB） | ioreg, IORegistry |
| `ww macos defaults` | 显示/搜索所有非默认系统偏好设置 | defaults CLI, plist 域 |
| `ww macos snapshot` | 带区域/录制功能的 screencapture | screencapture 标志 |
| `ww macos permissions` | 显示 TCC 数据库（哪些应用有相机/麦克风/文件访问权限） | TCC.db, sqlite3 |

其中 `permissions` 特别有趣——TCC（Transparency, Consent, and Control）是 macOS 的隐私框架。读取它有助于理解 Apple 如何对应用访问进行沙盒化：

```bash
# TCC 数据库位置（受 SIP 保护，需要复制）
cp ~/Library/Application\ Support/com.apple.TCC/TCC.db /tmp/
sqlite3 /tmp/TCC.db "SELECT client, service, auth_value FROM access;"

# 显示哪些应用有相机、麦克风、屏幕录制、文件访问等权限
```

---

## TL;DR 优先级

1. **yabai + skhd** — 今天安装，日常使用，最大的生产力提升
2. **阅读 m-cli 源码** — 30 分钟投入，让你的知识库增加 200 个新 macOS 命令
3. **构建 `ww macos services`** — launchctl 是最被低估的 macOS 工具
4. **构建 `ww macos hardware`** — ioreg 能提供 sysctl 无法获取的数据
