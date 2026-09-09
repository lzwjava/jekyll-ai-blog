---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么IP是无连接的
translated: true
type: note
---

问题：为什么 IP protocol 是 connectionless 的？

答案：

IP (Internet Protocol) 在设计上是 connectionless 的，这意味着它在发送数据前不会建立专用的 communication channel。原因如下：

**1. 每个 packet 都是独立的**
每个 IP packet 都包含它所需的全部 routing information（source IP、destination IP、TTL 等），并独立地在 network 中传输。来自同一 transmission 的 packet 可能走不同的 route，并且到达时可能乱序。

**2. 简单性与 Scalability**
通过不维护 connection state，router 只需要根据 destination address 转发 packet。这使得 protocol 轻量级，并允许 internet 扩展到数十亿台设备，而无需 router 跟踪每一个正在进行的“conversation”。

**3. Fault Tolerance**
由于没有固定的 path，如果某个 router 失败，packet 可以动态地被 reroute。一个 connection-oriented protocol 需要从头重新建立整个 connection。

**4. “Dumb Network, Smart Endpoints” Philosophy**
IP 的设计目标是让 network 本身保持简单（只负责 forward packet），而 reliability 和 ordering 由 higher layers 处理——具体来说就是 transport layer 的 TCP。这就是 **end-to-end principle**。

**5. 效率**
在 data 流动之前，不需要任何 handshaking overhead。这使得 IP 在那些 low latency 比 guaranteed delivery 更重要的任务中更快（例如 DNS lookups、通过 UDP 的 video streaming）。

简而言之：IP 用 reliability guarantees 换取了速度、简单性和 resilience。如果你需要在 IP 之上获得 connection-oriented 行为，你可以使用 **TCP**，它增加了 handshaking、ordering 和 retransmission——但 IP 本身仍然是“fire and forget”。

References:
- [RFC 791 – Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)
- [End-to-end principle – Wikipedia](https://en.wikipedia.org/wiki/End-to-end_principle)
- [Connectionless communication – Wikipedia](https://en.wikipedia.org/wiki/Connectionless_communication)