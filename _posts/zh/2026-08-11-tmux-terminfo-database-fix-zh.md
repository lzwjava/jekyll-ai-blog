---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tmux terminfo 数据库修复
translated: true
type: note
---

已修复。以下是问题原因及处理方法：

## 根本原因
你 `~/bin` 中的 `tmux` 是一个自定义构建版本，链接到绑定的 ncurses 库：
```
libncurses.so.6 => /home/lzw/bin/libs/libncurses.so.6
```
该库是在 **AppImage 构建环境** 内编译的，因此其中硬编码了 terminfo 路径：
```
/opt/build/AppDir/usr/share/terminfo   ← 你的机器上不存在
```
tmux 在此路径查找终端定义，找不到，于是报错 "can't find terminfo database"。

系统 terminfo 数据库是正常的，位于 `/usr/share/terminfo`（由 `ncurses-term` 包提供）。

## 修复方法
设置 `TERMINFO=/usr/share/terminfo`，让 tmux 使用系统数据库而非失效的 AppImage 路径。已验证可以工作：

```bash
TERMINFO=/usr/share/terminfo tmux
```

并使其永久生效，已追加到你的两个 shell 配置文件中：

```bash
# ~/.bashrc (第124行) 和 ~/.zshrc (第5行)
export TERMINFO=/usr/share/terminfo
```

打开新终端（或运行 `source ~/.bashrc`），`tmux` 即可正常工作。

## 可选（更干净的替代方案）
如果你不想保留环境变量，也可以通过符号链接将失效路径指向真实路径来修复库本身——但这需要 root 权限（因为涉及 `/opt`）。使用环境变量更简单且完全足够。如果你将来重新编译/更新该 tmux 构建版本，请针对系统 ncurses 进行编译（`apt install libncurses-dev`），以免再次遇到此问题。