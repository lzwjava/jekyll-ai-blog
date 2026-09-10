---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ICMP源抑制：传统减速信号
translated: true
type: note
---

**问题:** 什么是“源点抑制报文”（Source Quench Message）？

**回答:**

**源点抑制报文**（ICMP Type 4）是ICMP协议中一种传统的拥塞控制机制。其工作原理如下：

**用途：** 它是一种发送给源主机的请求，要求其降低向某个目的地发送流量的速率。该报文由网关（路由器）或目标主机生成，用于告知发送方因为无法跟上接收数据的速度而需要减速。

**触发条件：**
- 当网关没有足够的缓冲空间来排队数据报以便输出到下一个网络时，它可能会丢弃IP数据报。如果网关丢弃了数据报，它可能会向源主机发送源点抑制报文。
- 如果数据报到达过快导致无法处理，目标主机也可能发送源点抑制报文。

**发送方的反应：** 收到源点抑制报文后，源主机应降低向指定目的地的流量发送速率，直到不再收到源点抑制报文。然后源主机可以逐渐提高速率，直到再次收到源点抑制报文。

**典型使用场景：** 源点抑制通常用于路由器连接高带宽网络（如局域网）与低带宽网络或设备（如拨号服务器）时，此时发送方很容易传输超出低速端处理能力的数据。

**当前状态——已弃用：** RFC 6633正式弃用了ICMP源点抑制报文。与现代化的TCP拥塞控制和ECN（显式拥塞通知）相比，源点抑制效率低下且存在安全问题，因此已被停止使用。

简而言之：源点抑制报文 = **ICMP Source Quench** —— 一种现已废弃的、由拥塞的路由器或主机向发送方发出的“减速！”信号。

---

**参考文献：**
- [RFC 6633 – 弃用ICMP源点抑制报文](https://tex2e.github.io/rfc-translater/html/rfc6633.html)
- [ICMP源点抑制报文分析 – firewall.cx](https://www.firewall.cx/networking/network-protocols/icmp-protocol/icmp-source-quench.html)
- [ICMP类型4源点抑制 – networksorcery.com](http://www.networksorcery.com/enp/protocol/icmp/msg4.htm)