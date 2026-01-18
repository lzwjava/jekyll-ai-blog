---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Hysteria 代理协议简介
translated: true
type: note
---

**Question:** 什么是用于 Proxy 的 Hysteria 协议？

**Answer:**

Hysteria（特别是当前版本 **Hysteria 2**）是一种高性能、具备抗审查能力的 Proxy 协议/工具，旨在针对劣质、高丢包或受严格审查的网络环境（如卫星链路、拥挤的 Wi-Fi 或中国等有严格互联网过滤的地区）提供快速且稳定的连接。

### 核心特性

- **底层技术** — 基于 **QUIC**（驱动 HTTP/3 的传输协议）构建，运行在 UDP 而非 TCP 之上。这使得它在丢包严重的网络中具有优势，而传统的 TCP 在遇到丢包时通常会大幅减速。
- **伪装 (Masquerading)** — 该协议被设计成在外部观察者（审查系统、DPI 系统、ISP）看来与标准的 **HTTP/3** 流量完全一致。如果没有有效的身份验证凭据，Hysteria 服务器的表现就像一个普通的 HTTP/3 Web 服务器（例如返回 404、提供文件下载或作为反向代理）。这使得在不封锁大量合法 Web 流量的情况下，很难对其进行屏蔽。
- **拥塞控制 (Congestion Control)** — 使用名为 **Brutal** 的自定义算法（在 Hysteria 2 中），即使在严重丢包的情况下也能尝试维持用户指定的带宽（例如 100 Mbps 下行），这在不稳定网络中非常有用（也可以回退到 BBR 算法）。
- **性能导向** — 优化目标是最大吞吐量而非最小损耗，使其在差劲的网络条件下比许多传统代理（Shadowsocks, V2Ray/VMess, Trojan）速度更快。

### 代理模式与用法

Hysteria 本身不是传统的 VPN；它主要是一种具有多种输出模式的 Proxy 协议：

- **SOCKS5** 代理（最常用）
- **HTTP** 代理
- **TCP/UDP 端口转发**
- **Linux TProxy**（透明代理）
- **TUN 模式**（Windows, macOS, Linux 上的全系统代理虚拟网卡 —— 仅处理 TCP + UDP）

你通常在 VPS/云主机上运行 Hysteria **Server**（配备域名和 TLS 证书），然后使用官方客户端或支持 Hysteria 2 的第三方 App（如 Nekobox, sing-box, Shadowrocket 等）进行连接。

### 典型使用场景

- 在 UDP 未被严格屏蔽的环境环境下绕过网络审查（GFW 等）
- 在移动网络、国际航班或卫星互联网上获得稳定的高速连接
- 解决传统基于 TCP 的代理因丢包而变得极其缓慢的场景

### 快速对比

- 相比 Shadowsocks/Trojan → 在高丢包链路上的性能好得多，且更难被检测。
- 相比 WireGuard/OpenVPN → 隐蔽性更强（看起来像 HTTPS），在恶劣条件下通常更快，但它不是完整的 L3 VPN（在 TUN 模式下默认不支持 ICMP/Ping）。
- 相比 Reality/VLESS → 伪装策略不同（HTTP/3 vs TLS-in-TLS）；Hysteria 通常在不稳定链路上胜出。

官方项目：https://github.com/apernet/hysteria
文档 (Hysteria 2)：https://v2.hysteria.network/

**References:**

- [Hysteria 2 Official Site](https://v2.hysteria.network/)
- [Protocol Documentation](https://v2.hysteria.network/docs/developers/Protocol)
- [GitHub Repository](https://github.com/apernet/hysteria)
- [Sing-box Hysteria2 Integration](https://sing-box.sagernet.org/manual/proxy-protocol/hysteria2)