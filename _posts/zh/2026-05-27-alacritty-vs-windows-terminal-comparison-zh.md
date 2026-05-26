---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Alacritty 与 Windows Terminal 对比
translated: true
type: note
---

**问题：** 在 Windows 上，Alacritty 是否比 Windows Terminal（使用 Git Bash 配置文件）更好？

**答案：**

简而言之：**Alacritty 在原始性能和配置即代码方面胜出；Windows Terminal 在集成和日常使用便利性方面胜出。** 对于你以终端为先、氛围编码的工作流程，以下是详细对比：

---

## 性能

| | Alacritty | Windows Terminal |
|---|---|---|
| 渲染器 | GPU 加速（OpenGL/Vulkan） | GPU 加速（DirectX） |
| 延迟 | 业界最佳（约 1ms 输入延迟） | 良好，但不及前者激进 |
| 回滚 | 可配置，快速 | 大缓冲区时较慢 |
| 启动速度 | 近乎瞬时 | 约 300–500ms |

Alacritty 的*设计初衷*就是成为最快的终端模拟器。它在基准测试中胜出。在实际使用中，现代硬件上两者都足够快，你在进行 Python 脚本编写或 SSH 会话时不会感到差异。

---

## 配置

**Alacritty：** TOML 文件（`~/.config/alacritty/alacritty.toml`）——可版本控制、可脚本化，通过 dotfiles 跨机器同步。

```toml
[shell]
program = "C:\\Program Files\\Git\\bin\\bash.exe"
args = ["--login", "-i"]

[font]
size = 13.0

[font.normal]
family = "JetBrainsMono Nerd Font"

[window]
opacity = 0.95
padding = { x = 8, y = 8 }
```

**Windows Terminal：** JSON 配置，但以 GUI 驱动。跨机器干净同步较为困难。

---

## Git Bash 集成

两者都能很好地配合 Git Bash。Windows Terminal 的 Git Bash 配置文件设置起来略微容易（下拉菜单自动检测）。Alacritty 需要你手动指定 shell（如上所示）。

对于 WSL2 工作流，Windows Terminal 略有优势——与 WSL 发行版的原生集成更为流畅。

---

## Alacritty 缺少的功能

- **无标签页**（设计如此——改用 tmux，你很可能已经在用）
- **无原生分屏**（同样，使用 tmux）
- **无下拉/quake 模式**（需第三方封装）
- Sixel/图像渲染：与 Mac 上的 iTerm2 相比受限

---

## 针对你的配置的结论

考虑到你的个人情况——以终端为先、Python/bash、SSH 连接 GPU 机器、配置即代码思维——**Alacritty + tmux** 是更好的组合，*前提*你愿意花 30 分钟进行设置。它与你目前在 macOS 上的设置相似（很可能使用 iTerm2 或类似快速终端 + tmux）。

**选择 Alacritty 如果：**
- 你想将终端配置放在 dotfiles 仓库中
- 你已经在使用 tmux 管理面板/标签页
- 你关心快速打字 / vim 的输入延迟

**留在 Windows Terminal 如果：**
- 你频繁在 WSL2、PowerShell 和 Git Bash 之间切换
- 你想要零配置的即插即用替代方案
- 你不想在 Windows 上管理 tmux

对于跨机器一致性（MacBook + Ubuntu 工作站 + Windows），Alacritty 的 TOML 配置可以在三者间干净同步——在你这个特定案例中，这可能是最有力的选择理由。