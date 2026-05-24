---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 终端优先的macOS精通必备工具
translated: true
type: note
---

好问题。根据你的个人画像——终端优先、构建CLI工具、想要深入理解操作系统——以下是我按影响优先级排名的实际推荐：

---

## 第一层：每日使用，潜移默化学习

### Homebrew
你已经在用了，但研究它的配方（Formula）系统能让你了解macOS的打包、代码签名、沙箱机制以及苹果依赖生态的运作方式。

```
# 查看某个配方的内部结构
brew cat fd
brew info --json=v2 jq
```

源码：https://github.com/Homebrew/brew

### iTerm2
如果你还在用 Terminal.app，建议切换过来。iTerm2 配置性更强且开源，支持触发器、配置方案、脚本 API 和 tmux 集成。

https://github.com/gnachman/iTerm2

### skhd / yabai
**skhd** = 热键守护进程，**yabai** = 平铺窗口管理器。两者结合能让你像使用 i3 一样通过键盘完全控制 macOS 窗口。研究 yabai 的源码可以了解 macOS 的 WindowServer、无障碍 API 和 SIP 的工作原理。

```bash
brew install koekeishiya/formulae/skhd
brew install koekeishiya/formulae/yabai
```

https://github.com/koekeishiya/skhd
https://github.com/koekeishiya/yabai

对于你这种工作流而言，这是 macOS 上最大的效率提升工具。

---

## 第二层：深入理解操作系统

### XNU 内核源码
你提到过——实际阅读和想象中完全不同。建议从以下开始：

```bash
# 查看你的内核版本
uname -a
# 对应到 https://github.com/apple-oss-distributions/xnu/tags
```

按顺序阅读以下文件：
1. `osfmk/kern/startup.c` — 启动流程
2. `bsd/kern/kern_proc.c` — 进程运行机制
3. `osfmk/ipc/` — Mach IPC（macOS 进程间通信的实际实现）

### launchd
理解 launchd 就是理解 macOS 的进程管理、调度和守护进程生命周期。建议阅读源码后熟练使用 `launchctl`：

```bash
# 列出所有用户代理
launchctl list | grep -v apple

# 检查某个具体服务
launchctl print gui/$(id -u)/com.apple.Finder
```

https://github.com/apple-oss-distributions/launchd

### libdispatch (GCD)
GCD 在 macOS 中无处不在。阅读其源码可以学习并发原语、线程池以及苹果对并行处理的思考方式。

https://github.com/apple/swift-corelibs-libdispatch

---

## 第三层：教你 macOS 能力的工具

### m-cli
macOS 管理任务的瑞士军刀。研究它可以了解 `defaults`、`profiles`、`diskutil`、`scutil`、`networksetup` 等数十种原生命令的用法：

```bash
brew install m-cli
m --help
```

https://github.com/rgcr/m-cli

### macos-defaults
`defaults write` 命令的全面目录。每个选项都有功能说明，你会发现自己从未了解过的系统特性。

https://github.com/yannbertrand/macos-defaults

```bash
# 示例：禁用“是否确定要打开此文件”对话框
defaults write com.apple.LaunchServices LSQuarantine -bool false
```

### osx-serial-number / powermetrics / fs_usage
不是项目，而是原生工具，但大多数人从未碰过：

```bash
# 实时显示电源/CPU/GPU指标（需要 sudo）
sudo powermetrics --samplers cpu_power,gpu_power -i 1000

# 实时监控所有文件系统系统调用
sudo fs_usage -w -f filesys

# 实时监控所有网络连接
sudo nettop -m tcp

# DTrace（SIP 允许部分功能，你也可以使用 Instruments）
sudo dtrace -n 'syscall::open*:entry { printf("%s", copyinstr(arg0)); }'
```

---

## 第四层：安全与内部机制研究

### The Objective-See Foundation
Patrick Wardle 的工具——免费、开源的 macOS 安全工具。研究它们可以了解 macOS 恶意软件的工作原理、TCC 数据库是什么、权限机制的运作方式以及如何审计自己的系统。

- **KnockKnock** — 检测 Mac 上的持久化项
- **BlockBlock** — 监控持久化位置
- **RansomWhere?** — 勒索软件检测
- **OverSight** — 麦克风/摄像头访问监控

https://objective-see.org/products.html

### macOS Security（GitHub 项目）
社区维护的 macOS 安全机制文档，涵盖 SIP、TCC、权限、AMFI、Gatekeeper、XProtect、MRT 等。

https://github.com/drduh/macOS-Security-and-Privacy-Guide

---

## 第五层：动手构建项目

以你的技能水平，深入学习 macOS 最快的方式是构建一个小工具。推荐思路：

1. **用 `libproc` + IOKit 做一个类似 `top` 的 macOS 工具**——学习进程内部机制
2. **做一个剪贴板管理器**（你的 `ww` 已有剪贴板处理功能）
3. **一个窗口自动化 CLI**，通过 PyObjC 封装 macOS 无障碍 API

```bash
# PyObjC 让你从 Python 访问几乎所有 macOS 框架
pip install pyobjc-framework-Cocoa pyobjc-framework-Quartz

# 示例：列出所有窗口
python3 -c "
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly
for w in CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, 0):
    print(w.get('kCGWindowOwnerName', '?'), '-', w.get('kCGWindowName', ''))
"
```

---

## 针对你的具体建议

从 **yabai + skhd**（第一层）开始——立刻提升效率，在配置过程中就能学到 macOS 窗口管理的内部机制。然后阅读 **XNU 的进程管理代码**（第二层），理解 `ps`、`top` 和“活动监视器”到底在查询什么。

将日常使用 yabai 与阅读 XNU 源码相结合，比起其他任何方法，都能让你更快地同时获得实用技能和深度理解。