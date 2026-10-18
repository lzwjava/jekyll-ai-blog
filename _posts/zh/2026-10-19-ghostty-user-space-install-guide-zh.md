---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ghostty 用户空间安装指南
translated: true
type: note
---

Ghostty 已安装并正常运行。由于 `sudo` 需要 TTY（我无法获取），我使用了 **user-space install** 方式——无需 root 权限。

## 安装内容

- **Ghostty 1.3.0**：来自 Ubuntu 26.04 的 universe 仓库（deb 包）
- 内容被提取至 `~/.local` 而非 `/usr`，并包含一个缺失的依赖 `libgtk4-layer-shell0`

## 布局

| Path | 用途 |
| ------ | --------- |
| `~/.local/bin/ghostty` | 启动器包装脚本（设置环境变量，并已加入你的 `PATH`） |
| `~/.local/opt/ghostty/` | Ghostty 二进制文件及资源（主题、Shell 集成、文档） |
| `~/.local/lib/ghostty-deps/` | 捆绑的 `libgtk4-layer-shell.so.0` |
| `~/.local/share/terminfo/x/xterm-ghostty` | Terminfo 条目 |
| `~/.local/share/icons/hicolor/...` | 应用图标 |
| `~/.local/share/applications/com.mitchellh.ghostty.desktop` | Desktop entry（已修改以使用包装脚本） |

该包装脚本负责处理系统安装通常会做的两件事：

```bash
export GHOSTTY_RESOURCES_DIR="$HOME/.local/opt/ghostty/usr/share/ghostty"
export LD_LIBRARY_PATH="$HOME/.local/lib/ghostty-deps/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
```

## 验证

- `ghostty --version` → `Ghostty 1.3.0-dev+0000000`
- 所有共享库均已解析（`ldd` 检查干净）
- `xterm-ghostty` terminfo 成功加载
- **Live GUI 冒烟测试**：成功打开了一个 Wayland 窗口并运行了一条命令
- 已出现在你的应用启动器中

## 备注

- 配置文件位于 `~/.config/ghostty/config`。
- `ghostty` 的启动方式与其他终端类似（例如，从启动器启动，或在 shell 中运行 `ghostty`）。
- `ww/ghostty/` 模块（`ww ghostty list` 等命令）**仅限 macOS**——它使用 Swift/Cocoa `CGWindowList`/`AXUIElement`，因此在此 Linux 机器上无法运行，无论本安装情况如何。
- 如果你更倾向于干净的、系统范围的安装（安装到 `/usr`，并带有正常的 apt 跟踪），请运行：

  ```bash
  sudo apt install ghostty
  ```

  然后移除用户空间副本：`rm -rf ~/.local/opt/ghostty ~/.local/lib/ghostty-deps ~/.local/bin/ghostty`。
