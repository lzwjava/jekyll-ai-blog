---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WebSocket 集成与故障排除指南
translated: true
type: note
---

这些是独立的问题：

**为什么使用 WebSocket？**

OpenClaw 使用 WebSocket 作为浏览器 Control UI 和 gateway 进程之间的核心实时传输。gateway 以持久化后台服务运行，管理 AI agents、message routing 和 channel connections。WebSocket 提供：
- 双向、低延迟流式传输（AI responses 以 token-by-token 方式流式传输到 UI）
- 持久连接，因此 gateway 可以推送事件（新消息、agent status）到浏览器，而无需 polling
- 一个连接可以复用多个并发 sessions/agents

URL `ws://192.168.1.36:18789` 只是 gateway 的 WebSocket endpoint 的 plain-HTTP 等价物 — 与 HTTP server 相同的 host/port，但升级到 WebSocket protocol。

**复制按钮问题**

很可能相关，是的。Control UI 中的复制按钮几乎肯定使用 WebSocket 连接向 gateway 发送命令（例如，通过 gateway host 上的 native clipboard 复制消息内容）。如果 WS 连接未完全建立或被断开，则任何触发 WS 消息的按钮都会静默失败或报错。

首先修复 WS 连接（origin allowlist + `dangerouslyDisableDeviceAuth`），然后重新测试复制按钮。