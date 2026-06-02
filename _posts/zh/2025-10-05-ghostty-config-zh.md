---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Ghostty Shell 配置指南
translated: true
type: note
---

### Ghostty 与 Ubuntu 系统中的 .bashrc

在加载 `.bashrc` 文件时，Ghostty 的行为与 Ubuntu（及其他 Linux 发行版）默认的 GNOME 终端保持一致。Ghostty 默认会为 bash 启动**非登录交互式 shell**，这意味着它会直接加载 `~/.bashrc`——正如 GNOME 终端那样。这是大多数 Linux 终端的标准行为，其中 `.bashrc` 用于处理交互式 shell 的配置（例如别名、提示符、非登录会话的环境变量）。

#### 加载 .bashrc 的机制
- 当您打开新的 Ghostty 窗口或标签页时，它会以非登录 shell 形式执行 `bash`（或您的默认 shell）。
- 如果 shell 处于交互模式（默认即是），Bash 会检查并加载 `~/.bashrc`。
- 如果您设置了 `~/.bash_profile`（通常用于登录 shell），除非您显式配置 Ghostty 启动登录 shell（例如在 `~/.config/ghostty/config` 中添加 `initial-command = bash --login`），否则该文件不会被加载。
- 潜在问题：部分用户反馈在新用户首次启动或特定设置（如 Ubuntu 远程 SSH 会话）时 `.bashrc` 未加载。这通常可通过确保不存在冲突的 `~/.bash_profile`，或在配置中手动加载该文件来解决。在 `.bashrc` 中添加保护语句如 `[[ $- != *i* ]] && return` 可避免在非交互场景中出现问题。

简而言之，在 Ubuntu 系统使用 `.bashrc` 时，Ghostty 与默认终端的行为完全一致，均采用非登录模式作为默认设置。

### macOS 系统中的 Ghostty：使用 .zprofile 还是 .bash_profile？

在 macOS 系统中，Ghostty 遵循平台传统（与 Terminal.app 类似），默认启动**登录 shell**，这与使用的 shell 类型无关。这将影响配置文件的加载：

- **若使用 zsh（macOS Catalina 及之后版本的默认 shell）**：每次新开终端时会同时加载 `~/.zprofile`（用于登录设置）*和* `~/.zshrc`（用于交互设置）。
- **若使用 bash**：系统会加载 `~/.bash_profile`（登录 shell）。此时 Bash 不会直接加载 `~/.bashrc`——因为 `~/.bashrc` 仅适用于非登录交互式 shell。如需引入 `.bashrc` 中的配置，请在 `~/.bash_profile` 中添加：
  ```
  if [ -f ~/.bashrc ]; then . ~/.bashrc; fi
  ```

因此，对于默认的 zsh 设置会加载 `~/.zprofile`，若使用 bash 则会加载 `~/.bash_profile`。您可以根据需要通过 Ghostty 的配置切换 shell 或调整设置。

[Shell 集成 - Ghostty](https://ghostty.org/docs/features/shell-integration)
[macOS 登录 Shell - Ghostty](https://ghostty.org/docs/help/macos-login-shells)
[潜在缺陷：启动时未读取 .bashrc - GitHub 讨论区](https://github.com/ghostty-org/ghostty/discussions/3437)
[Bash 启动文件 - GNU 手册](https://www.gnu.org/software/bash/manual/bash.html#Bash-Startup-Files)
