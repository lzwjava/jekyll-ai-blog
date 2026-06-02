---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 以太网数据帧类型解析
translated: true
type: note
---

问题：什么是单播帧？其他类型的帧有哪些？

回答：

在计算机网络中，特别是在以太网的数据链路层（第2层），帧根据其目标MAC地址进行分类。此分类决定了交换机和其他设备如何处理和转发它们。

### 单播帧

- **单播帧**是以太网帧，从一个发送方发送到一个单一的特定接收方。
- 目标MAC地址是分配给单个网络接口的唯一单播地址（例如，十六进制的第一个八位字节以偶数开头，其中第一个八位字节的最低有效位为0）。
- 交换机仅将单播帧转发到与目标MAC地址关联的特定端口（通过MAC地址表学习）。如果目标未知，则帧会被泛洪（在学习之前被视为广播）。
- 这是最常见的流量类型，用于日常通信，如Web浏览或两个设备之间的文件传输。

### 其他类型的帧

在第2层，主要还有两种其他类型：

#### 广播帧

- **广播帧**是从一个发送方发送到本地网络段（广播域）中的**所有设备**。
- 目标MAC地址是`FF:FF:FF:FF:FF:FF`（所有二进制1）。
- 交换机将广播帧泛洪到同一VLAN中的所有端口（除了入站端口）。
- 常见用途：ARP请求、DHCP发现。
- 广播不会跨越路由器（局限于本地第2层域）。

#### 组播帧

- **组播帧**是从一个发送方发送到**特定组**的感兴趣接收方（而不是所有设备）。
- 目标MAC地址的第一个八位字节的最低有效位设置为1（例如，IPv4组播地址以01:00:5E开头）。
- 如果没有优化（如IGMP Snooping），交换机将像广播一样泛洪组播帧。通过优化，它们只发送到有感兴趣设备的端口。
- 常见用途：视频流、路由协议更新（例如OSPF）、发现协议（例如CDP）。

注意：以太网帧级别没有“任播”，因为任播是第3层（IP）概念，其中流量被路由到组中最近的设备。

这些分类有助于高效管理网络流量：单播用于直接通信，组播用于组效率，广播用于本地到达所有人。

参考资料：

- [Unicast, Multicast, and Broadcast Addresses - Study CCNA](https://study-ccna.com/unicast-multicast-and-broadcast-addresses/)
- [Unicast, Multicast, and Broadcast Explained](https://www.computernetworkingnotes.com/ccna-study-guide/unicast-multicast-and-broadcast-explained.html)
- [Identifying Ethernet Multicast - Brad Hedlund](https://bradhedlund.com/2007/11/21/identifying-ethernet-multicast/)
- [Unicast, multicast, broadcast addresses | CCNA](https://geek-university.com/unicast-multicast-broadcast-addresses/)
