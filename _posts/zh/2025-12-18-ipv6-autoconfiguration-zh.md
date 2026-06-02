---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: IPv6 无状态地址自动配置协议
translated: true
type: note
---

问题：IPv6 中用于无状态地址自动配置的协议是哪个？
A) DHCPv6
B) SLAAC
C) NAT66
D) OSPFv3

答案：

正确答案是 **B) SLAAC**。

**解释**：
无状态地址自动配置 (SLAAC) 是 IPv6 中定义的一种机制，允许主机自动配置其 IPv6 地址，而无需有状态服务器。它使用路由器发出的路由器通告 (RA) 消息，其中包含网络前缀信息，使主机能够生成其接口标识符（通常通过 EUI-64 或隐私扩展从 MAC 地址生成）并形成完整的地址。SLAAC 在 RFC 4862 中有描述。

- **A) DHCPv6**：不正确。DHCPv6 是一种有状态协议，它从服务器提供地址和其他配置（类似于 IPv4 中的 DHCP），但它不是无状态的。
- **C) NAT66**：不正确。NAT66 是 IPv6 的网络地址转换的一种形式，由于 IPv6 拥有巨大的地址空间，因此很少使用。
- **D) OSPFv3**：不正确。OSPFv3 是一种用于 IPv6 的路由协议，与地址配置无关。

SLAAC 提供了一种简单、无服务器的方式让设备获取地址，使其成为 IPv6 中无状态自动配置的标准。

参考文献：
- [RFC 4862: IPv6 Stateless Address Autoconfiguration](https://tools.ietf.org/html/rfc4862)
- [RFC 8415: DHCPv6](https://tools.ietf.org/html/rfc8415)（与有状态配置对比）
