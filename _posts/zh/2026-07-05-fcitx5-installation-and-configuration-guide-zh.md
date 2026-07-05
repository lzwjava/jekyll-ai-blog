---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fcitx5安装与配置指南
translated: true
type: note
---

已完成。Fcitx5 已在此机器上安装并运行。

## 概要

**已安装的软件包**：fcitx5、fcitx5-chinese-addons（包含拼音引擎 + cloudpinyin + pinyinhelper）、fcitx5-config-qt（GUI 配置工具）、所有前端（GTK3/4、Qt5/6）。

**配置**：
- im-config 设置为 fcitx5
- `~/.config/fcitx5/profile` 配置了 `keyboard-us` + `pinyin`
- IBus 守护进程已终止（两者冲突——不要同时运行）
- Fcitx5 守护进程在 X11 上运行

**使用方法**：
- `Ctrl+Space` 在英文（keyboard-us）和中文拼音之间切换
- 或运行 `fcitx5-config-qt` 打开 GUI 设置
- 或通过命令切换：`fcitx5-remote -s pinyin` / `fcitx5-remote -s keyboard-us`

**注意**：当前通过 SSH 运行在服务器（192.168.1.36 工作站）上。Fcitx5 需要一个正在运行的 X11 会话——如果你通过 X 转发进行 SSH 连接，或者直接在工作站的显示器上使用，它就能正常工作。如果你的 MacBook Air 也需要使用，可以通过 `brew install fcitx5` 安装。