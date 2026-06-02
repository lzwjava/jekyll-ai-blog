---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ollama启动代理禁用摘要
translated: true
type: note
---

以下是对已完成操作的回顾：

1. **识别服务** — `launchctl list | grep -i ollama` 发现注册了 `com.ollama.ollama` 作为启动代理。

2. **定位 plist 文件** — 搜索了标准位置 (`~/Library/LaunchAgents`、`/Library/LaunchAgents`、`/Library/LaunchDaemons`)。在应用内部找到位于 `/Applications/Ollama.app/Contents/Library/LaunchAgents/com.ollama.ollama.plist`。

3. **停用服务** — 执行两条命令：
   - `launchctl bootout` — 尝试停止正在运行的服务（因服务未主动运行而返回 I/O 错误，这并无影响）
   - `launchctl disable` — 防止其在未来登录时自动启动

4. **验证** — `launchctl print-disabled` 确认 `com.ollama.ollama => disabled`。

**注意一点：** 仍有一个标记为 `enabled` 的 `homebrew.mxcl.ollama` 条目。如果您也通过 Homebrew 安装了 Ollama，该条目也可能启动服务。如果您也需要停用此条目，请告知我。
