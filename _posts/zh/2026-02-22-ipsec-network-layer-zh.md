---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络层的 IPsec
translated: true
type: note
---

问题：IPsec 安全通信机制在哪一层运行？

回答：

IPsec (Internet Protocol Security) 在 OSI 模型的 **Network Layer**（Layer 3）运行。

IPsec 在这一层的关键特性包括：
*   **Transparency:** 因为它在 network layer 工作，IPsec 对上层协议（如 TCP 和 UDP）和应用程序是透明的。应用程序无需修改即可使用 IPsec。
*   **Scope:** 它保护两个端点（主机或网关）之间传递的所有流量，而不管生成流量的特定应用程序。
*   **Functionality:** 它为 IP 数据包提供数据机密性（加密）、数据完整性、数据来源认证和防重放保护等服务。
*   **Modes:** 它以两种模式运行：
    *   **Transport Mode:** 只加密 IP 数据包的有效载荷（主要用于主机到主机的通信）。
    *   **Tunnel Mode:** 加密整个原始 IP 数据包，包括头部，并将其封装在新 IP 数据包中（主要用于网关到网关或站点到站点的 VPN）。

这将它与像 TLS/SSL 这样的安全协议区分开来，后者在 Transport Layer（Layer 4）或 Session/Presentation layers 运行，并且需要应用级集成或特定的代理配置。

参考文献：

- [RFC 4301: Security Architecture for the Internet Protocol](https://datatracker.ietf.org/doc/html/rfc4301)