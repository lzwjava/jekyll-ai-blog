---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络中的隧道技术
translated: true
type: note
---

问题：网络中的隧道技术是什么？

答案：

隧道技术是一种网络技术，它将一个网络协议封装在另一个协议内部，使数据能够穿越原本不支持它的网络。可以把它想象成把一封信放进另一个信封——外层信封负责投递，内层信封则包含真正的负载。

**工作原理**

1. **封装** — 原始数据包（包含其头部）被包裹在另一个使用不同协议的数据包中。
2. **传输** — 封装后的数据包像普通流量一样穿越传输网络。
3. **解封装** — 在目标端点，外层包装被移除，原始数据包被交付。

**常见应用场景**

- **VPN（虚拟专用网络）** — 通过公共互联网安全地连接远程用户或办公室（例如 IPSec、OpenVPN、WireGuard）。
- **IPv6 over IPv4** — 过渡机制如 6in4 或 Teredo，通过 IPv4 基础设施隧道传输 IPv6 流量。
- **GRE（通用路由封装）** — 连接不同网络，或通过仅支持单播的路径传输组播流量。
- **SSH 隧道** — 通过 SSH 连接安全地转发任意 TCP 端口。
- **SD-WAN / 覆盖网络** — 抽象物理网络拓扑，创建逻辑的、软件定义的路径。

**关键隧道协议**

| 协议 | 层 | 典型用途 |
|---|---|---|
| IPSec | L3 | VPN，加密站点到站点 |
| GRE | L3 | 封装任意 L3 协议 |
| L2TP | L2 | 远程访问 VPN |
| VXLAN | L2 over L4 | 数据中心覆盖网络 |
| WireGuard | L3 | 现代轻量级 VPN |
| SSH | L7 | 端口转发，SOCKS 代理 |

**安全注意事项**

隧道如果不受监控，可以绕过防火墙和安全控制——因此它们既是工程师的强大工具，也是潜在的攻击载体（例如用于数据窃取的 DNS 隧道）。

参考：
- [RFC 2784 – 通用路由封装（GRE）](https://datatracker.ietf.org/doc/html/rfc2784)
- [Cloudflare – 什么是隧道技术？](https://www.cloudflare.com/learning/network-layer/what-is-tunneling/)
- [RFC 4026 – 提供商预配 VPN 术语](https://datatracker.ietf.org/doc/html/rfc4026)