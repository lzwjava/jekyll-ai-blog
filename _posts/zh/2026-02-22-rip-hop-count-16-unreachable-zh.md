---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RIP 跳数 16 表示不可达
translated: true
type: note
---

问题：在 RIP 协议中，hop count 为 16 表示什么？

答案：

在 **Routing Information Protocol (RIP)** 中，hop count 为 **16** 表示目标网络 **不可达**。

### 解释

- RIP 是一种 **distance-vector routing protocol**，它使用 **hop count** 作为其 **metric** 来确定到目的地的最佳路径。
- RIP 中的最大有效 hop count 为 **15**。这意味着 15 个 hop 以内或更少的任何目的地都被认为是可达的。
- hop count 为 **16** 在 RIP 术语中被定义为 **infinity**。当路由器接收或计算出一个 metric 为 16 的路由时，它会将该路由视为无效或不可达。
- 此机制有助于防止 **routing loops** 并限制 RIP 支持的网络大小（不支持超过 15 hop 的直径）。

因此，当 RIP 路由器通告一个 metric 为 16 的路由时，它实际上是在说：“我没有到此网络的有效路径。”

参考资料：

- [RFC 1058 - Routing Information Protocol](https://datatracker.ietf.org/doc/html/rfc1058)
- [Cisco Documentation on RIP Metrics](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13730-3.html)
