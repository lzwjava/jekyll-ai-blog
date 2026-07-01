---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 虚拟路由冗余协议概述
translated: true
type: note
---

Question: 请全面介绍网络中的 VRRP 协议。

Answer:

### VRRP 简介

**Virtual Router Redundancy Protocol (VRRP)** 是一种标准化的计算机网络协议，旨在为 IP 网络中的默认网关（default gateway）提供高可用性（high availability）。它通过允许物理上的多个路由器作为一个逻辑上的“虚拟路由器”工作，消除了静态默认网关带来的单点故障（single point of failure）。局域网（LAN）上的主机将此虚拟路由器的 IP 地址配置为默认网关，从而在主路由器发生故障时确保无缝的故障转移（failover）。

VRRP 是由 Internet Engineering Task Force (IETF) 定义的开放标准。当前版本是 **VRRPv3**（详见 2010 年发布的 RFC 5798），它同时支持 IPv4 和 IPv6，并取代了早期版本（针对 IPv4 的 RFC 3768 中的 VRRPv2）。

### 目的与核心优势

- **冗余（Redundancy）**：为默认网关提供自动故障转移，无需更改主机配置。
- **高可用性（High Availability）**：最大限度地减少网络停机时间；故障转移通常在几秒钟内发生。
- **透明性（Transparency）**：主机只看到一个虚拟网关 IP，察觉不到底层的物理路由器。
- **对路由表无影响**：VRRP 仅管理网关冗余；它不发布路由，也不修改路由表（routing tables）。
- **范围（Scope）**：限制在单个子网/局域网内；不会跨越子网。

### VRRP 工作原理

VRRP 将多台路由器分组为一个由 **Virtual Router Identifier (VRID)**（1-255）和一个或多个 **virtual IP addresses (VIPs)** 标识的**虚拟路由器**。

- **角色**：
  - **Master Router**：活动状态的路由器，负责转发发送到 VIP 的流量。它拥有 VIP，并使用 **virtual MAC address** 响应 ARP (IPv4) 或 ND (IPv6) 请求。
  - **Backup Routers**：备用路由器，监控 Master 的状态，并在 Master 故障时接管。

- **Virtual MAC Address**：自动生成的格式为 `0000.5E00.01XX`（针对 IPv4）或类似的 IPv6 格式，其中 XX 是十六进制的 VRID。

- **选举过程（Election Process）**：
  - 路由器被分配一个**优先级（priority）**（0-255；默认值为 100）。优先级最高者胜出。
  - 决胜局：如果优先级相同，则物理 IP 地址最高的路由器胜出。
  - 拥有实际 VIP 地址的路由器（如果配置了）会获得优先级提升，通常直接成为 Master。

- **通告（Advertisements）**：
  - Master 定期发送 **VRRP advertisement packets**（组播地址为 224.0.0.18，针对 IPv4；默认间隔为 1 秒）。
  - Backup 监听这些数据包；如果超过 **Master Down Interval**（通常是通告间隔的 3 倍）未收到，则会选举产生新的 Master。

- **抢占（Preemption）**：默认开启；当优先级更高的路由器上线时，它可以从优先级较低的 Master 手中接管权限。

- **故障检测**：
  - 快速检测（通过调整定时器可以实现亚秒级检测）。
  - 支持 **object tracking**（对象跟踪），如果上行链路/接口发生故障，可以降低优先级。

### 版本

- **VRRPv2**：仅限 IPv4 (RFC 3768)。
- **VRRPv3**：统一支持 IPv4 和 IPv6 (RFC 5798)；改进了定时器（timers），允许 VIP 作为真实 IP。

### 与同类协议的比较

| 特性 | VRRP | HSRP (Cisco 私有) | GLBP (Cisco 私有) |
| ------------------------ | ------------------------------- | ------------------------------ | ------------------------------ |
| 标准 | 开放标准 (IETF) | 私有 (Proprietary) | 私有 (Proprietary) |
| 活动路由器 | 一个 Master | 一个 Active | 多个 (负载均衡) |
| 负载均衡 | 否 (单一活动) | 否 (或手动配置) | 是 |
| 组播地址 | 224.0.0.18 | 224.0.0.2 / 224.0.0.102 | 224.0.0.102 |
| 抢占 (Preemption) | 是 (默认) | 是 | 是 |
| IPv6 支持 | 是 (v3) | 是 | 否 |
| 最佳用途 | 多供应商混合环境 | 纯 Cisco 网络 | 需要负载均衡的 Cisco 网络 |

由于其开放标准的特性，VRRP 在异构环境中更受青睐，而 HSRP/GLBP 则提供了 Cisco 特有的增强功能。

### 安全性与局限性

- **身份验证**：VRRPv3 中已弃用；早期版本支持明文或 MD5（现在被认为是不安全的）。
- **局限性**：没有内置的负载均衡（load balancing）；除非配置多个组，否则所有流量都通过 Master 传输。

VRRP 被各大厂商的路由器/交换机广泛支持，是构建弹性局域网设计的核心要素。

参考文献：

- [Virtual Router Redundancy Protocol - Wikipedia](https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol)
- [RFC 5798 - Virtual Router Redundancy Protocol (VRRP) Version 3 for IPv4 and IPv6](https://datatracker.ietf.org/doc/html/rfc5798)
- [Introduction of Virtual Router Redundancy Protocol (VRRP) - GeeksforGeeks](https://www.geeksforgeeks.org/introduction-of-virtual-router-redundancy-protocol-vrrp-and-its-configuration/)
- [VRRP (Virtual Router Redundancy Protocol) - NetworkLessons](https://networklessons.com/cisco/ccie-routing-switching/vrrp-virtual-router-redundancy-protocol)
- [HSRP vs VRRP vs GLBP Protocols - GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/hsrp-vs-vrrp-vs-glbp-protocols/)
