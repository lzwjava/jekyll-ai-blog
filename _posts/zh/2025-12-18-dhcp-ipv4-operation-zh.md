---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: DHCP IPv4 操作解析
translated: true
type: note
---

**问题：** DHCP在IPv4中是如何工作的？

**答案：**

IPv4中的动态主机配置协议（DHCP）是一种客户端-服务器协议，它自动为网络上的设备（客户端）分配IP地址和其他网络配置参数（例如子网掩码、默认网关和DNS服务器）。这消除了手动配置的需要，减少了错误，并有效地管理了IP地址池中的分配。

### 关键组件
- **DHCP Client**：请求配置的设备（例如，计算机、电话）。
- **DHCP Server**：维护IP地址池并以租用时间分配它们。
- **DHCP Relay Agent**（可选）：如果服务器不在同一个本地网络上，则转发跨子网的请求。

DHCP使用UDP端口：67（服务器）和68（客户端）。

### DHCP过程：DORA
获取新IP地址的核心过程称为**DORA**（Discover, Offer, Request, Acknowledge）。所有初始消息都是广播的，因为客户端尚未拥有IP地址。

1. **Discover (DHCPDISCOVER)**  
   客户端广播DHCPDISCOVER消息以查找可用的服务器。  
   - 源IP: 0.0.0.0  
   - 目标IP: 255.255.255.255 (广播)  
   - 它包含客户端的MAC地址用于识别。

2. **Offer (DHCPOFFER)**  
   一个或多个DHCP服务器以DHCPOFFER消息响应，提议一个IP地址和配置选项。  
   - 广播（因为客户端尚未拥有IP）。  
   - 包括提议的IP、租用期限、子网掩码、网关、DNS等。

3. **Request (DHCPREQUEST)**  
   客户端选择一个Offer（通常是第一个收到的）并广播DHCPREQUEST以接受它。  
   - 这会通知其他服务器它们的Offer已被拒绝。

4. **Acknowledge (DHCPACK)**  
   选定的服务器发送DHCPACK以确认分配。  
   - 客户端现在可以使用IP地址。  
   - 如果服务器无法履行（例如，地址已被使用），它会发送DHCPNAK（否定确认）。

### 其他消息类型
- **DHCPRELEASE**：客户端将IP地址释放回服务器。
- **DHCPDECLINE**：客户端拒绝一个提供的地址（例如，如果它检测到冲突）。
- **DHCPINFORM**：客户端请求额外的选项而无需新的IP。
- **DHCPNAK**：服务器拒绝请求。

### 租约管理
- IP地址租用期限有限。
- 客户端使用单播DHCPREQUEST向原始服务器续订租约（通常在租约时间的50%时）。
- 如果续订失败，客户端会在稍后间隔重试或重新启动DORA。

此过程确保了IPv4网络中高效的动态IP管理。

**参考文献：**

- [Dynamic Host Configuration Protocol - Wikipedia](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol)
- [What is DHCP (Dynamic Host Configuration Protocol)? | TechTarget](https://www.techtarget.com/searchnetworking/definition/DHCP)
- [DHCP defined and how it works | Network World](https://www.networkworld.com/article/966242/dhcp-defined-and-how-it-works.html)
- [What is the DHCP DORA Process? | nwkings.com](https://www.nwkings.com/dora-process-in-dhcp)