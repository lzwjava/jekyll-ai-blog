---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: MAC 地址数量限制端口
translated: true
type: note
---

问题：哪个端口安全功能限制了端口上的 MAC 地址数量？

答案：

正确答案是 **C) 最大 MAC 地址数 (Maximum MAC addresses)**。

在 Cisco 交换机端口安全中，直接限制端口上允许的 MAC 地址数量的功能是通过 `switchport port-security maximum <number>` 命令配置的。这会设置端口可以容纳的安全 MAC 地址（无论是动态学习还是静态配置）的最大数量。

- **A) 粘滞 MAC 地址 (Sticky MAC)**：这指的是 `switchport port-security mac-address sticky` 功能，它动态学习 MAC 地址并将其转换为运行配置中的粘滞（持久）条目。它不限制地址的数量。
- **B) 违规限制 (Violation Restrict)**：这是一种违规模式（`switchport port-security violation restrict`），当超出最大数量时，它会增加违规计数器并丢弃来自未经授权 MAC 地址的流量，但它本身不是设置限制的功能。
- **D) Portfast**：这是一种生成树协议 (STP) 功能，它绕过接入端口上的监听和学习状态，从而实现立即转发。它与 MAC 地址限制无关。

“最大 MAC 地址数”设置是限制安全端口上允许的源 MAC 地址数量的核心机制。
