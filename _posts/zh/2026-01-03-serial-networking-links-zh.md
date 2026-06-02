---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 了解网络中的串行链路
translated: true
type: note
---

Question: What are serial links in networking?

Answer:

在 computer networking 中，**serial links**（串行链路）是指点对点（point-to-point）连接，它们在单个通道上按顺序一次传输一个 bit，与之相对的是同时发送多个 bit 的 parallel links。

### Key Characteristics

- **Point-to-Point Nature**：serial links 通常是两个设备（例如 routers）之间的专用连接，不需要像 MAC addresses 这样的 link-layer 寻址。在 IP 层级，它们通常是 "unnumbered" 的，因为只有一个可能的目的地。
- **Common Use in WANs**：从历史上看，routers 上的 serial interfaces 用于 Wide Area Network (WAN) 连接，例如 leased lines（T1/E1, DS3）、Frame Relay 或 PPP links。这些连接通过电信运营商提供可靠的长距离连接，运营商提供 clocking，链路运行速度从 56 kbps 到大约 52 Mbps（例如通过 HSSI）。
- **DTE/DCE Roles**：一端是 Data Terminal Equipment（DTE，例如 router），另一端是 Data Circuit-terminating Equipment（DCE，例如 CSU/DSU 或 modem），后者为 synchronous transmission 提供 clocking。
- **Encapsulation Protocols**：常见的 Layer 2 协议包括 HDLC（Cisco serial interfaces 的默认协议）、PPP 或 Frame Relay。

### Comparison to Ethernet Links

- Ethernet 专为 Local Area Networks (LANs) 设计，支持多设备连接（通过 switches），使用 MAC addressing，并以更高的速度运行（100 Mbps+）。
- Serial links 在专用点对点 WANs 中优先考虑距离和简单性，而 Ethernet 在共享的高带宽本地环境中表现出色。

### Modern Relevance

虽然 serial links 过去是 WANs 的标准（在 CCNA/CCNP 学习和旧部署中很常见），但如今它们在很大程度上已被 Ethernet handoffs、Metro Ethernet、MPLS 或基于 fiber 的服务所取代，以实现更高的速度和更简单的管理。它们仍然出现在 legacy systems、工业控制、console access (RS-232) 或特定的低速应用中。

References:

- [Serial communication - Wikipedia](https://en.wikipedia.org/wiki/Serial_communication)
- [What's the difference between Ethernet link and Serial link? - Network Engineering Stack Exchange](https://networkengineering.stackexchange.com/questions/55016/whats-the-difference-between-ethernet-link-and-serial-link)
- [Serial Connections and HDLC | CCNA Blog](https://www.ccnablog.com/serial-connections-and-hdlc/)
- [Serial Point-to-Point Overview - Cisco Press](https://www.ciscopress.com/articles/article.asp?p=2202412&seqNum=4)
