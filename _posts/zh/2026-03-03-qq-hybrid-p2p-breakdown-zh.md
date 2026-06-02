---
audio: false
generated: true
image: false
lang: zh
layout: post
title: QQ 混合 P2P 通信拆解
translated: true
type: note
---

问题：QQ 如何使用 P2P 技术进行通信？

答案：

QQ（腾讯的即时通讯应用）采用了一种 **hybrid architecture**，它结合了集中式服务器与 **P2P (peer-to-peer)** 连接。它并不对所有通信使用纯 P2P，而是选择性地应用 P2P 来减少服务器负载、降低延迟并节省带宽，特别是针对媒体密集型功能。

### QQ 使用 P2P 的主要场景

- **视频通话和音频通话**
  QQ 采用经典的 VoIP 风格设计：
  - 通话建立和信令（邀请、参数协商、会话建立）始终通过腾讯的服务器。
  - 一旦会话建立并达成 codec/参数协议，实际的 **audio/video media stream** 就会尽可能使用 P2P 在两个客户端之间直接传输。
  这显著减少了服务器在实时媒体方面的带宽消耗。

- **文件传输（特别是在线好友之间）**
  当双方用户均在线时，QQ 会尝试建立直接 P2P 连接进行文件传输。
  - 成功 → 数据直接在两个客户端之间流动（更快且节省服务器流量）。
  - 失败（严格 NAT/防火墙、不兼容网络环境）→ 回退到通过腾讯服务器中继。

- **文本消息**
  文本消息通常通过腾讯服务器传输，而不是纯 P2P，特别是：
  - 接收方离线时（消息存储在服务器上）。
  - 许多日常场景（QQ 客户端的历史行为）。
  不过，当双方在线且网络条件有利时，一些实现可能通过 P2P 直接发送小消息。

### QQ 如何实现 P2P 连接（NAT 穿越）

大多数用户位于 NAT 路由器后面，因此 QQ 必须解决 NAT 穿越问题以实现直接连接。它使用与 Skype、WebRTC 等非常相似的技术：

1. **两个客户端定期维护与 QQ 登录服务器的 UDP 连接**（通常在端口 8000/8001 上）。这会创建 NAT 映射。
2. **发现阶段**
   - 每个客户端通过 QQ 服务器（类似于 STUN 服务器）获知自己的公网 IP:port。
   - 当用户 A 想要呼叫用户 B 或发送大文件时，A 会向服务器请求 B 的公网 IP:port 映射。
3. **打洞（Hole punching (P2P打洞)）**
   - 两个客户端同时向对方的预期的公网 IP:port 发送 UDP 数据包。
   - 这会在各自的 NAT 设备上“打洞”。
   - 短时间后，NAT 映射允许来自对端的传入数据包，建立直接 UDP 通道。
4. **回退中继**
   如果打洞失败（例如一方或双方为对称 NAT），则媒体/数据通过腾讯的高带宽服务器中继。

QQ 主要使用 **UDP** 进行媒体 P2P 通道（更适合实时性和打洞），但在网络环境困难时可回退到 **TCP**。

### QQ 的 P2P 策略总结



| 功能                  | 信令 / 控制 | 媒体 / 数据传输             | 主要方法                |
|-----------------------|-------------|-----------------------------|-------------------------|
| 文本聊天              | Server     | 通常服务器，有时 P2P        | Server → hybrid        |
| 语音/视频通话         | Server     | 尽可能 P2P                  | Hybrid (P2P preferred) |
| 文件传输（在线）      | Server     | 尽可能 P2P                  | Hybrid (P2P preferred) |
| NAT 穿越              | —          | UDP 打洞 + 中继              | STUN-like + relay      |

简而言之，QQ 主要针对**高带宽实时媒体**（视频/语音）和**在线用户之间的大文件传输**使用 P2P，同时依赖服务器进行信令、离线消息以及直接 P2P 无法建立时的回退。

参考文献：

- [The Mechanism of Tencent QQ Video Communication](https://www.researchgate.net/publication/266643063_The_Mechanism_of_Tencent_QQ_Video_Communication)
- [Forensic Analysis of Popular Chinese Internet Applications](https://opendl.ifip-tc6.org/db/conf/ifip11-9/df2010/YangCHWCCC10.pdf)
- [QQ通信原理及QQ是怎么穿透内网进行通信的？](https://blog.csdn.net/tanqiuwei/article/details/27198983)
- [P2P通信原理与实现 - 腾讯云开发者社区](https://cloud.tencent.com/developer/article/2215777)
