---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TCP/IP模型层次结构
translated: true
type: note
---

问题：TCP/IP 模型的四层是什么？

答案：

TCP/IP 模型分为四层，每一层负责网络通信中一个不同的部分：

**1. Network Access Layer (Link Layer)**
负责同一网络内设备之间的数据物理传输。它处理硬件寻址（MAC 地址）、网络驱动程序和物理介质（Ethernet、Wi-Fi 等）。

**2. Internet Layer**
负责逻辑寻址和跨不同网络路由数据包。此处的关键协议是 **IP (Internet Protocol)**，以及 ICMP 和 ARP。它决定数据从源到目的地的最佳路径。

**3. Transport Layer**
管理主机之间的端到端通信。两个主要协议是：

- **TCP** (Transmission Control Protocol) — 可靠、面向连接
- **UDP** (User Datagram Protocol) — 快速、无连接

**4. Application Layer**
最顶层，面向用户的协议在此运行。它包含 **HTTP、FTP、DNS、SMTP、SSH** 等。应用程序直接与此层交互以发送和接收数据。

以下是一个简明的图示总结：

| 层 | 名称 | 主要协议 |
| ------- | ------ | --------------- |
| 4 | Application | HTTP, DNS, FTP, SMTP |
| 3 | Transport | TCP, UDP |
| 2 | Internet | IP, ICMP, ARP |
| 1 | Network Access | Ethernet, Wi-Fi, MAC |

参考：

- [TCP/IP Model – GeeksforGeeks](https://www.geeksforgeeks.org/tcp-ip-model/)
- [RFC 1122 – Requirements for Internet Hosts](https://datatracker.ietf.org/doc/html/rfc1122)
- [TCP/IP Guide – No Starch Press](http://www.tcpipguide.com/free/t_TCPIPArchitectureandtheTCPIPModel.htm)
