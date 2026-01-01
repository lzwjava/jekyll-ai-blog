---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: PPP 身份验证与封装概述
translated: true
type: note
---

Question: 哪种 WAN protocol 常用于 serial links 上的 authentication 和 encapsulation？

Answer: 

正确答案是 **C) PPP**。

**Explanation**:  
PPP (Point-to-Point Protocol) 是一种广泛使用的 WAN protocol，专门设计用于在 serial links（如 leased lines、dial-up 或 synchronous serial connections）上建立直接连接。它既提供网络层数据包的 **encapsulation**，又支持 **authentication**（通常使用 PAP 或 CHAP）。

以下是其他选项错误的原因：  
- **A) RIP** – Routing Information Protocol 是一种 routing protocol，而不是 WAN link-layer protocol。它不处理 serial links 上的 encapsulation 或 authentication。  
- **B) OSPF** – Open Shortest Path First 也是一种用于网络内 dynamic routing 的 routing protocol，不用于 link-layer encapsulation 或 authentication。  
- **D) VLAN** – Virtual LAN 是一种用于在 Ethernet switches 上划分网络的 Layer 2 技术。它不是 WAN protocol，也不适用于 serial links。

**使 PPP 成为正确选择的关键特性**：  
- 运行在 data link layer (Layer 2)  
- 为 IP 和其他网络协议提供 encapsulation  
- 支持 authentication (PAP, CHAP, 或 MS-CHAP)  
- 常用于 WAN 环境中的 serial interfaces（例如通过 T1/E1 线路或 modem 连接的 routers）  

**Final Answer: C) PPP**

References:  
- Cisco 关于 PPP 的官方文档：[https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/bbdsl/configuration/xe-16/bba-16-ppp-over-ethernet.html](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/bbdsl/configuration/xe-16/bba-16-ppp-over-ethernet.html)  
- RFC 1661 – The Point-to-Point Protocol (PPP) [https://datatracker.ietf.org/doc/html/rfc1661](https://datatracker.ietf.org/doc/html/rfc1661)