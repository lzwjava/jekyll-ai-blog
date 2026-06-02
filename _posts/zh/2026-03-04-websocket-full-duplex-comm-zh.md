---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WebSocket 全双工通信详解
translated: true
type: note
---

**问题：WebSocket 如何工作？**

**答案：**

WebSocket 是一种通信协议，它在单个长期存在的 TCP 连接上，为客户端（通常是浏览器）和服务器之间提供 **full-duplex**（双向）、持久连接。

以下是 WebSocket 的实际工作原理，按步骤说明：

### 1. WebSocket 握手 (HTTP → WebSocket 升级)

一切从一个 **普通的 HTTP 请求** 开始——这是浏览器允许我们切换到 WebSocket 的唯一方式。

```
Client → Server

GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
Origin: https://client.example.com
```

重要头部：
- `Upgrade: websocket` — 我想要切换到 WebSocket
- `Connection: Upgrade` — 请不要将其视为普通的 HTTP
- `Sec-WebSocket-Key` — 随机 base64 值（浏览器生成）
- `Sec-WebSocket-Version: 13` — 当前标准版本

服务器必须回复：

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

- `101 Switching Protocols` = “好的，现在切换”
- `Sec-WebSocket-Accept` = 特殊哈希：
  `base64( SHA-1( client-key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11" ) )`

收到此响应后——**连接不再是 HTTP**。它现在是同一 TCP socket 上的 **WebSocket 连接**。

### 2. WebSocket 帧格式（握手后）

升级后，双方可以随时发送 **frames**。

最常见的帧类型：

| Opcode | 含义                      | 典型用途                        |
|--------|---------------------------|---------------------------------|
| 0x1    | Text frame                | JSON、聊天消息                  |
| 0x2    | Binary frame              | images、audio、protobuf 等      |
| 0x8    | Connection close          | 礼貌告别                        |
| 0x9    | Ping                      | 保活检查                        |
| 0xA    | Pong                      | Ping 回复                       |

小型真实世界帧示例（文本消息 "Hello"）：

```
FIN=1, Opcode=0x1 (text)
Mask=1 (client → server messages are always masked)
Payload length = 5
Masking-key: 4 random bytes
Payload: "Hello" XORed with the 4-byte mask (repeated)
```

→ 服务器使用相同密钥对其进行解掩码 → 得到 "Hello"

### 3. WebSocket 的关键特性

| 属性                   | WebSocket                        | HTTP polling / long-polling     |
|------------------------|----------------------------------|----------------------------------|
| 连接                   | 持久，单个 TCP                   | 每次新连接                       |
| 方向                   | full-duplex（双方随时）          | 通常客户端 → 服务器请求         |
| 每消息开销             | ~2–14 bytes                      | 200–800+ bytes (HTTP headers)    |
| 延迟                   | 非常低                           | 高（新 TCP + HTTP 开销）         |
| 浏览器支持             | 优秀（所有现代浏览器）           | 到处可用                         |

### 4. JavaScript 中的典型生命周期

```javascript
// Client side
const ws = new WebSocket("wss://server.example.com/chat");

ws.onopen = () => {
  console.log("Connected!");
  ws.send(JSON.stringify({ type: "join", user: "alice" }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Received:", data);
};

ws.onclose = () => console.log("Disconnected");
ws.onerror = (err) => console.error("Error", err);

// Later
ws.send("Hello everyone!");
ws.close(1000, "User left");
```

### 5. 最常见的服务器实现（2025）

- Node.js → `ws`、`uWebSockets.js`（非常快）、Socket.IO（添加回退 + 功能）
- Python → `websockets`、`FastAPI + WebSockets`、`Django Channels`
- Go → `gorilla/websocket`，自 Go 1.22 以来的原生支持非常好
- Java → Spring WebSocket、Jakarta WebSocket
- Rust → `tokio-tungstenite`、`warp`、`axum`

### 快速总结——一句话描述 WebSocket

WebSocket 使用一个普通的 HTTP 请求，将其升级为一个长期存在的双向二进制安全通道，添加非常少的帧开销，然后允许客户端和服务器随时发送消息，而无需再次请求许可。

**参考资料：**

- [WebSocket protocol RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [WebSocket framing explained (excellent visualization)](https://tools.ietf.org/html/rfc6455#section-5.2)
