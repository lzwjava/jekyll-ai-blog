---
audio: false
generated: true
image: false
lang: en
layout: post
title: WebSocket Runs Over TCP
translated: false
type: note
---

**Question:** Is WebSocket built on UDP?

**Answer:**

No, **WebSocket is not built on UDP**.

WebSocket is built on top of **TCP**, just like HTTP.

Here is the actual protocol stack:

```
Application → WebSocket (ws:// or wss://)
              ↓
Transport     → TCP
              ↓
Internet      → IP
```

Typical full stack comparison:

| Protocol       | Transport layer | Reliable? | Ordered? | Common use cases                  |
|----------------|------------------|-----------|----------|------------------------------------|
| WebSocket      | TCP              | Yes       | Yes      | Real-time apps, chat, games, trading |
| HTTP/1.1       | TCP              | Yes       | Yes      | Web pages, APIs                    |
| HTTP/2, HTTP/3 | TCP (h2) / UDP (h3) | Yes    | Yes      | Faster web, multiplexing           |
| WebRTC data    | UDP (SCTP over DTLS over UDP) | No* | No*   | Video calls, file transfer in browsers |
| Raw UDP        | UDP              | No        | No       | DNS, gaming, VoIP, streaming       |

*WebRTC data channel provides optional reliability & ordering via SCTP, but it still runs over UDP.

### Quick summary – why WebSocket uses TCP (not UDP)

- Needs **reliable, ordered** delivery (no lost or duplicated messages)
- Works through almost all NATs and firewalls (because it starts as HTTP)
- Browser security model strongly prefers TCP-based connections
- Most real-time applications that need guaranteed message delivery (chat, collaborative editing, trading terminals, notifications) want TCP semantics

UDP-based alternatives (used when you explicitly want lower latency and can tolerate loss):

- WebRTC data channels
- Raw WebTransport over HTTP/3 (QUIC → UDP)
- Custom UDP protocols (very rare in browsers)

**Bottom line (2026):**

WebSocket = **TCP**  
WebSocket ≠ UDP

References:

- [https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [https://datatracker.ietf.org/doc/html/rfc6455](https://datatracker.ietf.org/doc/html/rfc6455) (WebSocket protocol specification)