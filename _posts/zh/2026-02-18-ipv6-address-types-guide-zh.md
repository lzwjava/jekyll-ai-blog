---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IPv6 地址类型简明解析
translated: true
type: note
---

问题：IPv6 地址的三种类型包括哪些？请列出单播、多播和任播地址。

答案：

IPv6 地址主要分为三种类型：

1. **单播地址（Unicast addresses）** - 标识单个网络接口。发送到单播地址的数据包将被传递到与该地址关联的特定接口。

2. **多播地址（Multicast addresses）** - 标识一组接口。发送到多播地址的数据包将被传递到该组内的所有接口（一对多通信）。

3. **任播地址（Anycast addresses）** - 标识一组接口中的最近接口。发送到任播地址的数据包将被传递到路由度量上最近的接口，从而实现高效的服务发现和负载分发。

问题中的空白处应填写 **unicast address**（单播地址）。

注意：与 IPv4 不同，IPv6 不使用广播地址，而是通过多播地址实现相关功能。

参考资料：

- [IPv6 地址架构 - RFC 4291](https://datatracker.ietf.org/doc/html/rfc4291)
- [Cisco - IPv6 地址类型](https://www.cisco.com/c/en/us/support/docs/ip/ipv6/29199-ipv6-faq-29199.html)