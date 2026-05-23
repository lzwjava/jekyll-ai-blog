---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 程序坞固定和正在运行的应用概览
translated: true
type: note
---

已完成。以下是新增内容：

创建：/Users/lzwjava/projects/ww/ww/macos/dock.py  
修改：/Users/lzwjava/projects/ww/ww/main.py

`ww macos dock` 会读取 Dock 的 plist 文件（~/Library/Preferences/com.apple.dock.plist），并以以下格式显示所有固定的应用：

- Dock 中所有应用的编号列表
- 每个应用的 Bundle Identifier
- ● 标记当前正在运行的应用（通过 osascript System Events 检测）
- --json 标志提供结构化输出

你的 Dock 中有 9 个应用：Safari、Ghostty、Telegram、Zed、Microsoft To Do、GitHub Desktop、WeChat、Passwords、System Settings —— 其中 6 个正在运行。