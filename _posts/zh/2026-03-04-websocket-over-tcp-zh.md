---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WebSocket 运行在 TCP 之上
translated: true
type: note
---

**问题：** WebSocket 是基于 UDP 的吗？

**答案：**

不是，**WebSocket 并非基于 UDP**。

WebSocket 是基于 **TCP** 的，就像 HTTP 一样。

以下是实际的协议栈：

```
Application → WebSocket (ws:// or wss://)
              ↓
Transport     → TCP
              ↓
Internet      → IP
```

典型的完整协议栈比较：

| Protocol       | Transport layer | Reliable? | Ordered? | Common use cases                  |
|----------------|------------------|-----------|----------|------------------------------------|
| WebSocket      | TCP              | Yes       | Yes      | Real-time apps, chat, games, trading |
| HTTP/1.1       | TCP              | Yes       | Yes      | Web pages, APIs                    |
| HTTP/2, HTTP/3 | TCP (h2) / UDP (h3) | Yes    | Yes      | Faster web, multiplexing           |
| WebRTC data    | UDP (SCTP over DTLS over UDP) | No* | No*   | Video calls, file transfer in browsers |
| Raw UDP        | UDP              | No        | No       | DNS, gaming, VoIP, streaming       |

*WebRTC data channel 通过 SCTP 提供可选的可靠性和有序性，但它仍然运行在 UDP 之上。

### 快速总结 – 为什么 WebSocket 使用 TCP（而非 UDP）

- 需要**可靠、有序**的交付（无丢失或重复消息）
- 能够穿越几乎所有 NAT 和防火墙（因为它以 HTTP 开始）
- 浏览器安全模型强烈偏好基于 TCP 的连接
- 大多数需要保证消息交付的实时应用（聊天、协作编辑、交易终端、通知）都希望使用 TCP 语义

基于 UDP 的替代方案（当您明确希望更低延迟并能容忍丢失时使用）：

- WebRTC data channels
- Raw WebTransport over HTTP/3 (QUIC → UDP)
- Custom UDP protocols (very rare in browsers)

**底线（2026）：**

WebSocket = **TCP**
WebSocket ≠ UDP

参考资料：

- [https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [https://datatracker.ietf.org/doc/html/rfc6455](https://datatracker.ietf.org/doc/html/rfc6455) (WebSocket protocol specification)
