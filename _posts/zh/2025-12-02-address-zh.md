---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 网络中的地址解析协议
translated: true
type: note
---

问题：网络中的 ARP 是什么？

答案：ARP (Address Resolution Protocol) 是 TCP/IP 网络中的一个基本协议，它将 IP 地址（第 3 层）转换为 MAC 地址（第 2 层），从而允许同一局域网 (LAN) 上的设备在数据链路层进行通信。

### ARP 的工作原理

1. 设备（例如，计算机 A）想要向同一局域网上的另一台设备（计算机 B）发送数据，并且知道计算机 B 的 IP 地址但不知道其 MAC 地址。
2. 计算机 A 向整个本地网络广播一个 ARP Request 数据包：
   “谁有 IP 地址 192.168.1.10？告诉 192.168.1.5”（包括它自己的 MAC 和 IP）。
3. 局域网上的所有设备都收到广播，但只有具有匹配 IP 的设备（计算机 B）回复 ARP Reply（单播）：
   “IP 192.168.1.10 在 MAC 00:1A:2B:3C:4D:5E”。
4. 计算机 A 收到回复，更新其本地 ARP 缓存（一个临时的 IP 到 MAC 映射表），现在可以直接向计算机 B 的 MAC 地址发送以太网帧。

### 关键点

- 在 OSI 模型的第 2 层（数据链路层）运行，但对于局域网上的第 3 层（IP）通信是必需的。
- 仅在同一广播域（同一子网/局域网）内使用。路由器不转发 ARP 广播。
- ARP 是无状态和无连接的。
- ARP 缓存中的条目通常会在几分钟后过期（例如，根据操作系统的不同，2-10 分钟）以处理硬件变化。

### ARP 数据包结构（简化）

| 字段                | 目的                                    |
|---------------------|-----------------------------------------|
| Hardware Type       | 通常为 1 (Ethernet)                     |
| Protocol Type       | 通常为 0x0800 (IPv4)                    |
| Hardware Address Length | MAC 地址为 6 字节                     |
| Protocol Address Length | IPv4 地址为 4 字节                    |
| Operation           | 1 = Request, 2 = Reply                  |
| Sender MAC & IP     | 源设备信息                              |
| Target MAC & IP     | 目标信息（请求中目标 MAC 为 00:00:00:00:00:00） |

### 变体和相关协议

- Gratuitous ARP：设备宣布自己的 IP 到 MAC 映射（在 IP 更改或检测重复时使用）。
- Proxy ARP：路由器代表其他子网中的设备响应 ARP 请求。
- ARP Spoofing/Poisoning：一种常见的攻击，恶意设备发送伪造的 ARP 回复，将其 MAC 与其他人的 IP 关联起来（中间人攻击的基础）。

### 示例（Linux/Windows 命令）

```bash
# 查看 ARP 表
arp -a          # Windows
ip neigh show   # Linux
```

简而言之：没有 ARP，局域网上的设备将不知道哪个物理 (MAC) 地址属于给定的 IP 地址，并且以太网通信将失败。
