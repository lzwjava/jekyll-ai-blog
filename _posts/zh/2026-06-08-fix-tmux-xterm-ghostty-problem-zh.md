---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 tmux xterm-ghostty 问题
translated: true
type: note
---

**问题:** 为什么 tmux 抱怨 `xterm-ghostty` 是不合适的终端？

**回答:**

tmux 正在检查 `TERM` 环境变量（你的 shell 将其设置为 `xterm-ghostty`，因为你使用的是 Ghostty 终端）与其已知终端能力数据库的匹配情况。问题在于：tmux 在其 terminfo 数据库中不识别 `xterm-ghostty` —— 原因可能是：

1. **Ghostty 的 terminfo 未安装** —— Ghostty 较新，你的系统 terminfo 数据库中尚无对应条目
2. **TERM 不匹配** —— 你的 shell 导出了 `TERM=xterm-ghostty`，但 tmux 只知道标准终端如 `xterm-256color`、`screen` 等

**修复方法（按推荐顺序排列）：**

```bash
# 选项1：使用兼容的 TERM 值（最简单）
TERM=xterm-256color tmux

# 选项2：在 shell 配置文件中设置 TERM（~/.zshrc 或 ~/.bash_profile）
export TERM=xterm-256color

# 选项3：安装 Ghostty 的 terminfo（正确解决方案）
# 去 Ghostty 的仓库或查看其文档了解安装方法
# 通常类似：
tic -xe ghostty ~/.config/ghostty/terminfo  # 如果 Ghostty 提供了这个
```

**我的建议：** 使用 `TERM=xterm-256color` 作为快速修复。如果 Ghostty 是你的日常终端，在 shell 配置中添加 `export TERM=xterm-256color`。这是安全的——大多数现代终端（包括 Ghostty）都与 xterm-256color 的能力集兼容。

然后：

```bash
lzw@to:~/projects/private-projects/whisper-playground/yangyang2$ tmux
```

应该可以工作。如果你想要在 tmux 中长期获得原生 Ghostty 支持，查看 Ghostty 的文档了解 terminfo 安装——但说实话，xterm-256color 完全够用。
