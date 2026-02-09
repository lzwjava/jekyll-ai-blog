---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 快速修复 Ghostty 终端错误
translated: true
type: note
---

Question: 为什么我在运行 htop 时出现 "Error opening terminal: xterm-ghostty"，而在运行 top 时出现 "'xterm-ghostty': unknown terminal type"？

Answer: 

你正在使用 **Ghostty** 作为你的 terminal emulator（可能是在 macOS 或 Linux 上），它将 `TERM` 环境变量设置为 `xterm-ghostty`。这是有意为之的 —— Ghostty 附带了自己的 terminfo 条目以支持其高级功能。

然而，当你通过 SSH 进入远程服务器（或者在某些 terminfo 数据库受限的本地环境中）时，远程系统在其 terminfo 数据库中没有 `xterm-ghostty` 的定义。像 `htop`、`top`、`nano`、`vim`、`multitail` 等使用 **ncurses** 的程序依赖 terminfo 来了解如何绘制 UI、处理按键、颜色等。如果没有它，它们会失败并报错，例如：

- `Error opening terminal: xterm-ghostty`
- `'xterm-ghostty': unknown terminal type`

这是较新的 terminal emulator 非常常见的问题（类似的问题也发生在 kitty → `xterm-kitty`，以及某些情况下的 Alacritty、WezTerm 等）。

### 快速修复（任选其一）

1. **最佳快速修复 —— 让 Ghostty 使用广泛支持的 TERM 值**  
   在你的 Ghostty 配置文件中添加这一行：

   ```
   term = xterm-256color
   ```

   - macOS 路径：`~/Library/Application Support/com.mitchellh.ghostty/config`
   - Linux 路径：`~/.config/ghostty/config`

   保存文件，**完全退出 Ghostty**（不仅是关闭窗口 —— 退出应用程序），然后重新启动它并开启一个新的 SSH 会话。  
   这能保持良好的颜色支持，且几乎在所有服务器上都能工作，无需进行任何远程更改。

2. **仅在使用 Ghostty 时覆盖 TERM（基于 shell 的临时方案）**  
   在**本地**机器的 shell 配置（例如 `~/.zshrc` 或 `~/.bashrc`）中添加以下内容：

   ```bash
   if [[ "$TERM_PROGRAM" == "ghostty" ]]; then
       export TERM=xterm-256color
   fi
   ```

   然后 source 配置文件（`source ~/.zshrc`）或打开一个新的终端标签页。这可以避免修改 Ghostty 的全局配置，仅影响 Ghostty 会话。

3. **SSH 特定修复（如果你仅在 SSH 时遇到问题，推荐此项）**  
   在本地的 `~/.ssh/config` 中添加：

   ```
   Host *
       SetEnv TERM=xterm-256color
   ```

   （需要 OpenSSH ≥ 8.7；现在已经非常普遍。）  
   这会为所有 SSH 连接强制使用 `xterm-256color`，而不影响本地终端的使用。

4. **更规范但也更麻烦 —— 在远程服务器上安装 Ghostty 的 terminfo**  
   从你的本地机器（已安装 Ghostty）执行：

   ```bash
   ssh user@remote-server mkdir -p ~/.terminfo/x
   scp /path/to/ghostty/terminfo/x/xterm-ghostty user@remote-server:~/.terminfo/x/
   ```

   或者遵循 Ghostty 官方的 terminfo 指南：将编译好的 terminfo 条目复制到远程机器。到 2026 年，一些较新的发行版可能会在 `ncurses-term` 或类似软件包中包含 `xterm-ghostty`。

### 建议
使用选项 1（在 Ghostty 配置中设置 `term = xterm-256color`）—— 对大多数人来说这是最简单且最可靠的。你只是在 SSH 时失去了 Ghostty 特有的高级功能（而这些功能对于 `htop`/`top` 来说通常并不需要）。

应用修复后，`htop` 和 `top` 应该都能正常启动。

References:  

- [https://ghostty.org/docs/help/terminfo](https://ghostty.org/docs/help/terminfo)
- [https://travis.media/blog/ghostty-ssh-unknown-terminal-error](https://travis.media/blog/ghostty-ssh-unknown-terminal-error)
- [https://github.com/ghostty-org/ghostty/discussions/3161](https://github.com/ghostty-org/ghostty/discussions/3161)
- [https://vninja.net/2024/12/28/ghostty-workaround-for-missing-or-unsuitable-terminal-xterm-ghostty](https://vninja.net/2024/12/28/ghostty-workaround-for-missing-or-unsuitable-terminal-xterm-ghostty)