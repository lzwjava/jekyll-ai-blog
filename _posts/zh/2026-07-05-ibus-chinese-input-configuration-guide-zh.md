---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IBus中文输入法配置指南
translated: true
type: note
---

以下是摘要：

**IBus + libpinyin** 现已安装并配置完成。

**已设置的内容：**
- 已安装 `ibus-libpinyin`（拼音输入引擎）
- 引擎设置为 `libpinyin` — 按 **Ctrl+Space** 可在英文和中文之间切换
- IBus 守护进程已重启
- 环境变量已添加到 `~/.bashrc`：
  - `GTK_IM_MODULE=ibus`
  - `QT_IM_MODULE=ibus`
  - `XMODIFIERS=@im=ibus`
- 保存的默认预载引擎：`[libpinyin, xkb:us::eng]`

**⚠️ 注意事项（纯终端会话）：**

该系统在此会话中没有运行桌面环境 — 这是一个 CLI/SSH 会话。输入法环境变量仅对此 shell 中启动的 **GUI 应用程序** 生效（如 `gedit`、`libreoffice`、`vscode`），但**不适用于此终端本身**。要在终端中支持中文输入，需满足以下条件之一：
1. **支持输入法的终端应用程序**（如 GNOME Terminal、Konsole、kitty — 不支持不带 X 的纯 TTY 或 tmux）
2. 或者使用 `fbterm` + `ibus` 实现 TTY 层级输入

如果使用 **TTY**（Ctrl+Alt+F1–F6，无 X 服务器），未安装 `fbterm` + `ibus-fbterm` 则中文输入无法工作。如果通过 **SSH** 从 Mac（使用 Terminal.app 或 iTerm2）登录，输入处理由**客户端**负责 — 在 Mac 端设置好中文输入法，即可在任何远程 shell 中正常使用。