---
audio: false
generated: true
image: false
lang: en
layout: post
title: WebSocket Full Duplex Communication Explained
translated: false
type: note
---

**Question: How does WebSocket work?**

**Answer:**

WebSocket is a communication protocol that provides **full-duplex** (two-way), persistent connection between a client (usually browser) and a server over a single, long-lived TCP connection.

Here’s how WebSocket actually works, step by step:

### 1. The WebSocket Handshake (HTTP → WebSocket upgrade)

Everything starts with a **normal HTTP request** — this is the only way browsers allow us to switch to WebSocket.

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

Important headers:

- `Upgrade: websocket` — I want to switch to WebSocket
- `Connection: Upgrade` — please don't treat this as normal HTTP
- `Sec-WebSocket-Key` — random base64 value (browser generates it)
- `Sec-WebSocket-Version: 13` — current standard version

Server must reply with:

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

- `101 Switching Protocols` = "okay, switching now"
- `Sec-WebSocket-Accept` = special hash:
  `base64( SHA-1( client-key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11" ) )`

After this response — **the connection is no longer HTTP**. It is now a **WebSocket connection** on the same TCP socket.

### 2. WebSocket framing (after handshake)

Once upgraded, both sides can send **frames** at any time.

Most common frame types:

| Opcode | Meaning                  | Typical use                     |
|--------|--------------------------|---------------------------------|
| 0x1    | Text frame               | JSON, chat messages             |
| 0x2    | Binary frame             | images, audio, protobuf, etc.   |
| 0x8    | Connection close         | polite goodbye                  |
| 0x9    | Ping                     | keep-alive check                |
| 0xA    | Pong                     | reply to ping                   |

Small real-world frame example (text message "Hello"):

```
FIN=1, Opcode=0x1 (text)
Mask=1 (client → server messages are always masked)
Payload length = 5
Masking-key: 4 random bytes
Payload: "Hello" XORed with the 4-byte mask (repeated)
```

→ Server unmasks it using the same key → gets "Hello"

### 3. Key properties of WebSocket

| Property               | WebSocket                        | HTTP polling / long-polling     |
|------------------------|----------------------------------|----------------------------------|
| Connection             | persistent, single TCP           | new connection each time         |
| Direction              | full-duplex (both ways anytime)  | usually client → server request  |
| Overhead per message   | ~2–14 bytes                      | 200–800+ bytes (HTTP headers)    |
| Latency                | very low                         | high (new TCP + HTTP overhead)   |
| Browser support        | excellent (all modern browsers)  | works everywhere                 |

### 4. Typical lifecycle in JavaScript

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

### 5. Most common server implementations (2025)

- Node.js → `ws`, `uWebSockets.js` (very fast), Socket.IO (adds fallback + features)
- Python → `websockets`, `FastAPI + WebSockets`, `Django Channels`
- Go → `gorilla/websocket`, native since Go 1.22 is very good
- Java → Spring WebSocket, Jakarta WebSocket
- Rust → `tokio-tungstenite`, `warp`, `axum`

### Quick summary — WebSocket in one sentence

WebSocket takes one normal HTTP request, upgrades it to a long-lived bidirectional binary-safe channel, adds very little framing overhead, and then lets both client and server send messages at any time without asking permission again.

**References:**

- [WebSocket protocol RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [WebSocket framing explained (excellent visualization)](https://tools.ietf.org/html/rfc6455#section-5.2)
