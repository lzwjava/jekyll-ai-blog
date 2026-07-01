---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ICMP与IGMP：主要区别
translated: true
type: note
---

**问题：** ICMP 和 IGMP 有什么区别？

**回答：**

两者听起来相似，但解决的是完全不同的问题。它们都直接位于 IP 之上（没有 TCP/UDP），但相似之处仅此而已。

**ICMP（协议号 1）**——IP 本身的错误报告和诊断。当数据包投递出现问题时（TTL 过期、主机不可达、需要分片），路由器/主机会向源端发送 ICMP 消息。它是 IP 缺乏的反馈通道，因为 IP 是“发后即忘”的。

关键消息类型：

- 类型 8/0 —— 回显请求/应答（`ping`）
- 类型 11 —— 超时（`traceroute` 利用这一点：发送 TTL=1,2,3... 的数据包，并从每一跳收集类型 11 消息）
- 类型 3 —— 目的不可达（代码 4，“需要分片但设置了 DF”，驱动路径 MTU 发现）
- 类型 5 —— 重定向

**IGMP（协议号 2）**——多播组成员管理，仅用于本地子网上主机与其第一跳路由器之间。主机通过 IGMP 成员关系报告说“我想接收发往 239.1.1.1 的流量”；路由器定期发送查询以了解哪些组仍有监听者，从而决定是否将多播流量转发到该网段。如果没有 IGMP，路由器将不得不向所有地方泛滥所有多播流量。

版本：IGMPv2（加入/离开），IGMPv3（源特定多播——“我想要组 G，但只来自源 S”，SSM 需要）。IPv6 完全弃用了 IGMP；等效协议是 MLD，它*作为 ICMPv6 消息*实现——这说明这两个协议是“兄弟”，而非同一事物。

快速对比：

| | ICMP | IGMP |
| --- | --- | --- |
| IP 协议号 | 1 | 2 |
| 目的 | 错误报告、诊断 | 多播组成员管理 |
| 范围 | 端到端（任何跳均可生成） | 仅链路本地（TTL=1） |
| 使用者 | ping、traceroute、PMTUD | IPTV、与 mDNS 相关的协议栈、使用多播的路由协议（OSPF 的 224.0.0.5） |
| IPv6 等效 | ICMPv6 | MLD（并入 ICMPv6） |

用 scapy 动手实践使之具体化：

```python
from scapy.all import *

# ICMP 回显请求（ping）
ans = sr1(IP(dst="1.1.1.1")/ICMP(type=8), timeout=2)
ans.show()  # type=0 echo-reply

# 构造 IGMPv2 成员关系报告（加入 239.1.1.1）
load_contrib("igmp")
pkt = IP(dst="239.1.1.1", ttl=1)/IGMP(type=0x16, gaddr="239.1.1.1")
send(pkt)

# 在局域网中观察真实的 IGMP（路由器每约 125 秒发送一次查询）
# sniff(filter="igmp", prn=lambda p: p.summary())
```

当你通过套接字 API 加入一个多播组时，内核会自动为你处理 IGMP：

```python
import socket, struct
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
             struct.pack("4s4s", socket.inet_aton("239.1.1.1"),
                                 socket.inet_aton("0.0.0.0")))
# ^ 这一行 setsockopt 会触发内核发送一个 IGMP 成员关系报告
```

在执行以上代码时运行 `tcpdump -i en0 igmp`，你会看到报告发出——花 5 分钟做个实验，效果不错。

思维模型：**ICMP 是 IP 的错误/控制平面；IGMP 是多播的信令平面。**一个报告故障，另一个声明兴趣。
