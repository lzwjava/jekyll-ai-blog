---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 串口访问已确认
translated: true
type: note
---

## ✅ 已确认 — 一切正常

| 检查项 | 结果 |
|-------|--------|
| 用户是否在 `dialout` 组中 | ✅ 是（通过 `sg dialout`） |
| `/dev/ttyUSB0` 设备 | ✅ 存在，CH340 已激活 |
| 端口权限 | ✅ `rw-rw----`，所有者 `root:dialout` (20) |
| 读写访问 | ✅ **成功** — 端口已通过 `O_RDWR` 打开 |

`usermod -aG dialout xiaoxin` 已正确生效。只是当前 shell 尚未加载新的组。通过 `sg dialout`（或 `newgrp dialout`）运行命令可立即激活。

### 两种方法使其在新终端中永久生效：

1. **注销并重新登录**（或重启）— 每个新终端将自动拥有 `dialout` 权限。
2. **或者在打开的任何新终端中运行一次以下命令：**
   ```bash
   exec su - $USER
   ```
   （将提示输入密码，然后启动一个新的登录 shell）

无论采用哪种方式，Arduino IDE 以及任何串口工具（`screen`、`minicom`、`arduino-cli`）现在都能正常连接到 `/dev/ttyUSB0`。