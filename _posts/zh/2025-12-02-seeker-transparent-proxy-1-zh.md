---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Seeker 透明代理技术概述
translated: true
type: note
---

问题：基于 Rust 的 Seeker 透明代理在底层是如何工作的？

答案：
Seeker 通过将**虚拟 TUN 接口**与用 Rust 编写的**用户空间路由 + 代理引擎**结合起来，创建了一个**完全透明的系统级代理**。它无需任何应用程序感知代理（无需 PAC、浏览器或应用程序中的 SOCKS/HTTP 设置）即可工作。

以下是详细的技术流程：

### 1. TUN 接口创建

- Seeker 创建一个虚拟网络接口（在 macOS 上通常是 `utun10`，在 Linux 上是 `tun0`）。
- 它分配一个 IP 地址（默认为 198.18.0.1/24）并启动该接口。
- 然后它**更改系统的默认路由**，以便**所有 IP 数据包**（除了发送到真实网关或本地网络的）都被路由到这个 TUN 设备中。
- 从内核的角度来看，每个出站数据包现在都通过 TUN 文件描述符到达用户空间。

### 2. 数据包读取循环 (Rust async/tokio)

- 主循环持续从 TUN 文件描述符中读取原始 IP 数据包。
- 使用 `etherparse` crate 解析数据包：
  - IPv4/IPv6 → TCP/UDP/ICMP
- 它提取**原始目标 IP + 端口**（这对于透明性至关重要）。

### 3. 规则匹配 (Clash 兼容)

- 对于每个新的 TCP 或 UDP 流，Seeker 在其规则集中查找目标域/IP：
  - 如果需要，首先解析域（通过其自己的 127.0.0.1:53 上的 DNS 服务器）
  - 支持 `DOMAIN-SUFFIX,netflix.com,PROXY`、`GEOIP,CN,DIRECT` 等规则。
  - 动作：**PROXY**、**DIRECT** 或 **REJECT**

### 4. 连接处理路径

**A. DIRECT（直连）**

- 数据包被直接写回到 TUN 中，并保留原始源 IP。
- 内核正常路由它 → 通过你的真实网关出去。

**B. REJECT（拒绝）**

- 向 TUN 发送 TCP RST 或 ICMP 不可达。

**C. PROXY（代理，有趣的情况）**

- Seeker **建立一个新的连接**到选定的代理服务器（Shadowsocks、SOCKS5 或 HTTP CONNECT）。
- 然后它在以下两者之间双向**传输数据**：
  - 原始应用程序 ↔ Seeker（通过 TUN 数据包）
  - Seeker ↔ 远程代理服务器（真实的 TCP/UDP socket）
- 对于 TCP：使用 tokio 异步流进行简单的双向复制。
- 对于 UDP：实现类似 UDP NAT 的映射（源端口 → 代理关联），以便回复可以正确路由回来。
- 对于 ICMP ping：使用 Fake-IP 模式（像 Clash 一样）——将真实目标 IP 映射到 198.19.0.0/16 范围，以便 ping 可以通过基于 TCP 的代理工作。

### 5. DNS 劫持

- 在 127.0.0.1:53 启动一个本地 DNS 服务器（接管系统 DNS）。
- 对于应该通过代理的域，它可以返回 **Fake-IPs**（以便后续的数据包命中 TUN）。
- 干净退出时恢复原始 DNS 设置。

### 6. 网关 / 局域网模式（可选）

- 将 DNS 绑定到 0.0.0.0:53，并期望其他设备将网关/DNS 指向你的机器。
- 整个局域网的所有流量都通过相同的 TUN + 代理逻辑流过。

### 使用的核心 Rust Crate

- `tokio` + `async-std` – 异步运行时
- `etherparse` – IP/TCP/UDP/ICMP 数据包解析和序列化
- `tun` / `smoltcp` 风格 – TUN 接口处理
- `shadowsocks-rust` 风格代码 – Shadowsocks 加密
- `yaml-rust` / `serde` – 配置解析

简而言之：Seeker 将你的机器变成一个**虚拟的类似 VPN 的路由器**，它根据域/IP 规则智能地通过代理重定向流量——完全采用安全、高性能的 Rust 实现。

*[GitHub - gfreezy/seeker](https://github.com/gfreezy/seeker)*
*[主要入口点 (main.rs)](https://github.com/gfreezy/seeker/blob/master/src/main.rs)*
*[TUN 处理模块](https://github.com/gfreezy/seeker/blob/master/src/tun.rs)*
*[规则引擎](https://github.com/gfreezy/seeker/blob/master/src/rule/mod.rs)*
