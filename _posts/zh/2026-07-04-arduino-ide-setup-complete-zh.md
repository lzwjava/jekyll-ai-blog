---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Arduino IDE 设置完成
translated: true
type: note
---

已完成。Arduino IDE **2.3.10** 已安装并配置完成。以下是总结：

**已安装的内容：**

- `~/Apps/arduino-ide.AppImage` (193M) — 从GitHub Releases下载
- `~/.local/share/applications/arduino-ide.desktop` — 显示在应用菜单的"开发" / "电子"分类下
- `~/.local/share/icons/.../arduino-ide.png` — 应用图标

**已配置的内容：**

- **dialout 用户组** — 您已是该组成员（新登录后立即生效）
- **brltty 已移除** — 该盲文显示守护进程原本已安装，它会占用CH340克隆端口。现已移除。
- **libfuse2** 已安装，因此AppImage可以运行

**启动方式：**

- 从应用菜单：搜索"Arduino IDE"
- 从终端：`~/Apps/arduino-ide.AppImage &`

**插入Arduino Uno时：**

- 正版Uno → `/dev/ttyACM0`
- CH340克隆版 → `/dev/ttyUSB0`（驱动程序已内置于内核，无需安装）
- 使用 `ls /dev/tty{ACM,USB}*` 检查

**注意：** dialout 用户组的更改在下次登录时生效。如果您想在当前会话中立即使用而不注销，请在您启动IDE的终端中运行 `newgrp dialout`。
