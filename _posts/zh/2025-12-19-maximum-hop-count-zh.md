---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: RIP 最大跳数解释
translated: true
type: note
---

问题：RIP 中的最大跳数是多少？

答案：

正确答案是 **A) 15**。

在路由信息协议 (RIP) 中，最大跳数是 15。这意味着任何距离超过 15 跳的目的地都被认为是不可达的，RIP 为此类路由分配度量值 16，将其标记为无限或无效。此限制旨在防止小型网络中的路由循环并保持协议的简单性，因为 RIP 是一种距离矢量路由协议。

- 选项 B) 16 是不正确的，因为 16 代表无限（不可达），而不是允许的最大跳数。
- 选项 C) 255 是内部网关路由协议 (IGRP) 中的最大跳数。
- 选项 D) 无限制适用于 OSPF 或 BGP 等协议，这些协议不强制规定严格的跳数限制。

此跳数限制是 RIP（RIPv1 和 RIPv2）的一个关键特征，并解释了为什么它主要适用于中小型网络。

参考文献：
- [Cisco RIP Documentation](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html)
- [RFC 1058 - Routing Information Protocol](https://tools.ietf.org/html/rfc1058)
- [RFC 2453 - RIP Version 2](https://tools.ietf.org/html/rfc2453)
