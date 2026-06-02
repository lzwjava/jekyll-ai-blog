---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 最大传输单元浅析
translated: true
type: note
---

### 网络中的MTU是什么？

**MTU** 全称为 **最大传输单元**。它指的是无需分片就能通过网络接口或协议传输的单个数据包的最大尺寸（以字节为单位）。

#### 关键细节：
- **典型值**：
  - 以太网通常使用1500字节的MTU（这是大多数基于IP网络的标准）。
  - 在支持的硬件上，巨型帧可达9000字节或更高。
  - IPv6的最小MTU为1280字节。
- **为何重要**：
  - **效率**：较大的MTU能减少开销（例如每个数据单元的头部信息更少），从而提升吞吐量。
  - **分片问题**：若数据包超过链路的MTU，可能会被分片或丢弃，导致延迟、重传或错误（如“数据包过大”的ICMP消息）。
  - **路径MTU发现**：设备通过此过程探测网络路径上的最小MTU，并相应调整数据包大小以避免分片。
- **常见问题**：设备间MTU不匹配（例如VPN隧道）可能导致连接问题。您可以使用 `ifconfig`（Linux/macOS）或 `netsh`（Windows）等工具检查或设置MTU。

简而言之，MTU定义了数据包的“最大载荷”限制，在网络设计中平衡了速度与兼容性。

深入阅读：[最大传输单元 - 维基百科](https://en.wikipedia.org/wiki/Maximum_transmission_unit)
