---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Chrome调试端口轮询修复
translated: true
type: note
---

已修复并推送（`d601f9f`）。

问题：`launch_chrome()` 使用了固定的 `time.sleep(3)` —— 当 Playwright 尝试连接端口 9222 时，Chrome 尚未完成其调试服务器的启动，因此导致 `ECONNREFUSED` 错误。

现在改为每 0.5 秒轮询端口 9222（最长 15 秒），直到端口实际可接受连接后才返回。请再次尝试 `ww x unfollow`。

需要注意：你需要先关闭所有其他 Chrome 窗口，否则 Chrome 可能会附加到现有进程，完全跳过 `--remote-debugging-port` 标志。