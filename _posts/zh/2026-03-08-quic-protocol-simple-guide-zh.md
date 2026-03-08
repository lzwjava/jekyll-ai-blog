---
audio: false
generated: true
image: false
lang: zh
layout: post
title: QUIC 协议简单解释
translated: true
type: note
---

## QUIC 协议 — 全面介绍

---

### 1. QUIC 是什么？

QUIC，由 Internet Engineering Task Force (IETF) 定义，是一种加密的面向连接协议，在 OSI 模型的传输层（第 4 层）运行。它最初由 Google 的 Jim Roskind 设计，于 2012 年首次实现和部署，并于 2013 年公开宣布。虽然其名称最初被提议为“Quick UDP Internet Connections”的缩写，但在 IETF 的用法中，QUIC 不是缩写——它只是协议的名称。

QUIC 于 2021 年 5 月由 IETF 正式发布为 RFC 9000。

---

### 2. 为什么创建 QUIC？TCP 的问题

TCP 旨在为两个端点之间发送数据流提供接口。它将数据拆分为网络数据包，添加序列号和校验和，并使用 Automatic Repeat Request (ARQ) 重新发送丢失或损坏的数据包。在大多数实现中，TCP 将任何错误视为阻塞操作，在错误解决或连接被视为失败之前停止进一步传输。

这导致了一个众所周知的问题，称为 **Head-of-Line (HoL) Blocking**：单个丢失的数据包会阻塞共享同一 TCP 连接的所有其他流。

此外，由于 TCP 实现在操作系统内核和中间设备中，对 TCP 进行重大更改几乎不可能。QUIC 基于 UDP 构建，因此不受此类限制。

---

### 3. QUIC 的架构：基于 UDP

QUIC 在传输层运行，并基于 UDP (User Datagram Protocol) 构建。这使其能够避免与 TCP 相关的一些开销和延迟。

QUIC 为应用程序提供流控流，用于结构化通信、低延迟连接建立和网络路径迁移。它包括确保在各种部署情况下机密性、完整性和可用性的安全措施。

---

### 4. QUIC 的关键特性

#### 4.1 降低延迟 & 更快的握手

初始 QUIC 握手将典型的 TCP 三次握手与 TLS 1.3 握手结合，提供端点认证和加密参数协商。典型的 QUIC 握手仅需客户端和服务器之间的一次往返，而 TCP 和 TLS 1.3 结合需要两次往返。

#### 4.2 零往返时间 (0-RTT)

在某些情况下，QUIC 可以在第一次连接周期中发送数据——称为 0-RTT（零往返时间）。当服务器与客户端有先前缓存的连接时，这成为可能。

#### 4.3 无队头阻塞的多路复用

与 TCP 不同，在 TCP 中单个数据包丢失会阻塞后续数据包的交付，QUIC 允许多个流通过单一连接发送，而不会发生队头阻塞。QUIC 通过使每个流（“通道”）独立运行来解决此问题。该协议仅重新传输单个流中的数据，而不是阻塞所有流。

#### 4.4 内置安全 (TLS 1.3)

QUIC 本质上安全，因为它强制使用 TLS 1.3。通过将认证和加密嵌入协议本身，QUIC 简化了安全通信，同时保留了 UDP 的轻量级优势。

通过 QUIC 发送的所有数据默认加密，且没有明文通信选项。这有助于防止窃听和其他形式的攻击。

#### 4.5 连接迁移

QUIC 包含一个连接标识符，用于唯一标识连接到服务器，无论客户端的源 IP 地址如何。这解决了 TCP 在用户从 Wi-Fi 热点切换到移动网络时出现的问题——在 TCP 中，每个现有连接都会逐一超时并必须重新建立。

连接迁移使用连接标识符允许连接转移到新的网络路径。此设计还允许连接在网络拓扑或地址映射更改后继续，例如由 NAT 重新绑定引起的情况。

#### 4.6 加密元数据

QUIC 还会加密额外的连接元数据，这些元数据可能被中间设备滥用来干扰连接。例如，数据包编号否则可能被被动在路径攻击者用于关联用户在多个网络路径上的活动。

---

### 5. QUIC 与 TCP+TLS 和 UDP — 比较

| 特性 | TCP + TLS | UDP | QUIC |
|---|---|---|---|
| 连接建立 | 慢（2+ RTT） | 无 | 快（1 RTT / 0-RTT） |
| 加密 | TLS（单独） | 无 | TLS 1.3 内置 |
| 多路复用 | 有限（HoL 阻塞） | 无 | 是，独立流 |
| 连接迁移 | 否 | 否 | 是（Connection ID） |
| HoL 阻塞 | 是 | 不适用 | 否 |
| 数据包丢失处理 | 阻塞所有流 | 无 | 仅每个流 |

---

### 6. QUIC 和 HTTP/3

HTTP/3 旨在利用 QUIC 的特性，包括流之间缺乏队头阻塞。QUIC 项目最初作为 TCP+TLS+HTTP/2 的替代方案启动，目标是改善用户体验，特别是页面加载时间。

QUIC 是针对 HTTP 开发的，而 HTTP/3 是其第一个应用。DNS-over-QUIC 是 QUIC 的另一个应用，用于名称解析，为解析器之间传输的数据提供类似于 DNS-over-TLS 的安全性。

---

### 7. gQUIC 与 IETF QUIC

事实上，有两个共享相同名称的协议：“Google QUIC”（gQUIC），由 Google 工程师设计的原始协议，后来被 IETF 采纳用于标准化；以及“IETF QUIC”，它与 gQUIC 差异足够大，被视为单独协议。IETF QUIC 使用标准的 TLS 1.3 进行加密握手，并采用模块化数据包和连接设计，旨在实现更广泛的互操作性。

---

### 8. 使用场景

- **网页浏览：** Google Chrome 大量使用 QUIC（在 Chrome 中，QUIC 用于连接到 Google 服务器的一半以上连接）。
- **IoT 设备：** QUIC 可以为 IoT 设备提供更可靠和高效的替代方案，因为它设计用于高延迟和丢包网络。
- **车联网 (IoV)：** QUIC 的低延迟、多路复用能力和对数据包丢失的弹性可以确保车辆与基础设施组件之间可靠高效的通信。
- **电子商务 & 支付：** QUIC 使用 TLS 加密和可靠的 HTTP/3 流，使其成为支付应用中安全可靠数据传输的良好选择。
- **云/负载均衡：** AWS Network Load Balancer 现在支持 QUIC 直通，使用 QUIC Connection ID 实现超低延迟转发和会话粘性。

---

### 9. 挑战和限制

- QUIC 不支持 SSL 解密，这是企业防火墙常用的一种检查和保护网络流量的机制。这为 IT 团队的网络可见性创造了重大盲点。
- 互联网基础设施中的许多中间设备针对 TCP 进行了调优，可能会限速甚至阻塞 UDP 流量。Google 的解决方案是让 Chromium 同时启动 QUIC 和 TCP 连接，实现无缝回退。
- 作为较新协议，其采用仍在增长，QUIC 流量甚至可能被某些网络组件阻塞。

---

### 10. 标准化时间线

| 年份 | 里程碑 |
|---|---|
| 2012 | Google 首次实现 |
| 2013 | 公开宣布；Chrome 实验开始 |
| 2017 | IETF 开始与 gQUIC 分歧 |
| 2020 | Chrome 大规模实验 IETF QUIC |
| 2021 年 5 月 | IETF 正式发布 QUIC 为 **RFC 9000** |

---

### 总结

QUIC 是一种现代、安全且高效的传输协议，旨在取代大多数互联网应用的 TCP。其低延迟（0-RTT/1-RTT）、多路复用独立流、内置 TLS 1.3 加密和连接迁移的结合，使其特别适合移动优先和性能敏感的应用。作为 HTTP/3 的传输骨干，QUIC 代表了传输层互联网通信的未来方向。

参考资料：

- [QUIC - Wikipedia](https://en.wikipedia.org/wiki/QUIC)
- [What is QUIC? Everything You Need to Know | Auvik](https://www.auvik.com/franklyit/blog/what-is-quic-protocol/)
- [The Road to QUIC | Cloudflare Blog](https://blog.cloudflare.com/the-road-to-quic/)
- [RFC 9000 - QUIC: A UDP-Based Multiplexed and Secure Transport](https://datatracker.ietf.org/doc/rfc9000/)
- [QUIC Protocol Overview | Chromium](https://www.chromium.org/quic/)
- [QUIC Protocol Features & Use Cases | EMQ](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov)
- [What is QUIC Protocol? | Check Point](https://www.checkpoint.com/cyber-hub/network-security/what-is-quic/)
- [QUIC Support in .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/quic/quic-overview)