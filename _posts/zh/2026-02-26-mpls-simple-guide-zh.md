---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MPLS 简单清晰地解释
translated: true
type: note
---

问题：MPLS 是什么意思？

答案：

**MPLS** 是 **Multi-Protocol Label Switching** 的缩写。

它是一种高性能路由技术，用于电信和企业网络，根据简短的 **labels** 而非长网络地址（如 IP addresses）将数据从一个网络节点定向到下一个。

### MPLS 的关键点

- **工作原理**
  包在进入 MPLS 网络时（在 Label Edge Router – LER 处）被分配一个简短、固定长度的标签（MPLS 头部中的 20-bit label）。
  在网络内部，路由器（Label Switch Routers – LSR）仅基于标签值转发包 — 无需为每个跳数查找完整的 IP 目标地址。
  在出口 LER 处，移除标签，包继续进行正常的 IP 转发。

- **主要优势**（为什么 MPLS 在 2000s–2020s 非常流行）
  - 快速转发（label lookup 比 IP longest-prefix match 更简单/更快）
  - Traffic engineering（显式路由路径，而非仅最短路径）
  - Quality of Service (QoS) 支持 — 不同流量类别可以获得不同处理
  - Virtual Private Networks (MPLS VPNs) — 广泛用于安全的 Layer 3 和 Layer 2 服务（L3VPN, VPLS, EVPN 等）
  - Fast reroute / protection（使用 FRR 的 sub-50 ms 故障转移）
  - Protocol-agnostic（“Multi-Protocol”） — 可以承载 IP、Ethernet、ATM、Frame Relay 等。

- **典型用例（在 2026 年仍非常常见）**
  - Service provider 主干和核心网络
  - Enterprise WAN 连接（运营商提供的 MPLS VPN 服务）
  - Carrier Ethernet 传输
  - SD-WAN underlay（许多 SD-WAN 解决方案仍使用 MPLS 作为可靠传输）
  - 大规模网络的 Traffic engineering（Google、Microsoft 和许多 telcos 仍大量使用 MPLS TE）

- **MPLS 与旧技术的比较**
  - 在运营商主干中取代了大部分 native ATM（MPLS 提供类似的 traffic engineering 和 QoS，但效率更高、成本更低）
  - 与现代 Segment Routing（SR-MPLS 或 SRv6）共存并常在其上运行，后者正在一些网络中逐步简化或取代传统 MPLS

- **当前状态（2026 年 2 月）**
  MPLS 仍是全球 service provider 和大型 enterprise WAN 中部署最广泛的技术之一。
  虽然 **Segment Routing (SR-MPLS / SRv6)**、**EVPN** 和 **SD-WAN** 等新方法正在逐渐流行，但纯 IP/MPLS 网络在大多数大规模 carrier 和 enterprise 环境中仍占主导地位。

简而言之：**MPLS = Multi-Protocol Label Switching** — 一种基于 label 的转发技术，为 IP 网络带来了 traffic engineering、VPN 服务和快速 QoS，并很大程度上取代了核心中的 ATM。

参考文献：

- 无（标准网络术语和行业知识）
