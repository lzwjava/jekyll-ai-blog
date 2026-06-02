---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 帧中继基础与演进
translated: true
type: note
---

**Frame Relay 全面介绍**

Frame Relay 是一种**高性能**、**分组交换**的广域网 (WAN) 协议，主要在 OSI 模型的**数据链路层** (Layer 2) 运行。它旨在高效传输地理分散位置之间的数据，特别是用于通过 WAN 连接 LAN。

### 历史背景

- 在 1980 年代后期开发，是从 **X.25** 分组交换的演进，并受早期 **ISDN** 规范影响。
- 由 **ANSI** (T1 委员会) 从 1988 年左右开始标准化，从 1990 年代初开始广泛商业可用。
- 在 1990 年代和 2000 年代初非常流行，作为专线经济有效的替代方案。
- 如今主要被 **MPLS**、**基于 Internet 的 VPN**、**SD-WAN** 和基于 Ethernet 的服务取代，但仍存在于遗留安装中。

### 核心概念：虚拟电路而非物理线路

与传统的点对点专线（每对站点需要专用物理电路）不同，Frame Relay 使用承运商提供的**共享“云”基础设施**。

- 客户通过单个物理链路连接到提供商的 Frame Relay 网络（“云”）。
- 称为**虚拟电路**的逻辑连接提供站点之间的连通性。
- 这种统计复用允许许多客户高效共享相同的高速骨干网。

### 关键组件和术语

- **DTE** (Data Terminal Equipment) — 客户设备（通常是路由器）。
- **DCE** (Data Circuit-terminating Equipment) — 提供商设备（Frame Relay 开关）。
- **Access link** — 从 DTE 到 DCE 的物理连接（通常是串行）。
- **Virtual Circuit (VC)** — 通过云的逻辑路径。
  - **PVC** (Permanent Virtual Circuit) — 预配置、始终可用（最常见）。
  - **SVC** (Switched Virtual Circuit) — 按需建立（很少使用）。
- **DLCI** (Data Link Connection Identifier) — 局部有效的编号（10 位字段，通常 16–1007 可使用），用于在接入链路上标识虚拟电路。
  - DLCI 仅具有**局部意义** — 相同 DLCI 可在不同链路上重用。
- **LMI** (Local Management Interface) — DTE 和 DCE 之间的信令协议。
  - 主要类型：**Cisco**（Cisco 默认）、**ANSI** (T1.617 Annex D)、**Q.933** (ITU)。
  - 携带状态信息（active/inactive/deleted）、多播和 DLCI 映射。

### Frame Relay 帧结构（简化）

```
+---------------------------------------------+
| Flag (0x7E)                                 |
+---------------------------------------------+
| Address Field (2–4 bytes)                   |
|   → DLCI (10 bits) + control bits + FECN/BECN/DE |
+---------------------------------------------+
| Data (variable length, up to ~1600–4096 bytes typical) |
+---------------------------------------------+
| FCS (Frame Check Sequence – CRC)            |
+---------------------------------------------+
| Flag (0x7E)                                 |
+---------------------------------------------+
```

地址字段中的重要标志：

- **FECN** (Forward Explicit Congestion Notification) — 前方拥塞。
- **BECN** (Backward Explicit Congestion Notification) — 后方拥塞。
- **DE** (Discard Eligibility) — 拥塞期间可首先丢弃该帧。

### 承诺信息速率 (CIR) 和突发

- **CIR** — 提供商承诺交付的保证最小带宽。
- **Bc** (Committed Burst size) — 可在 CIR 下无风险发送的数据量。
- **Be** (Excess Burst size) — 如果网络有容量，可发送的额外数据。
- 超过 CIR + Bc 的帧可能设置**DE 位**，并在拥塞期间被丢弃。

### Frame Relay 的优势

- 与专用专线相比成本效益高（支付共享带宽）。
- 对**突发流量**高效（LAN 到 LAN 互连）。
- 支持更高速度（通常 56 kbps 到 45 Mbps，有时更高）。
- 灵活拓扑（星型、部分网状、全网状只需更少物理链路）。
- 简化网络（需要更少物理电路）。

### 缺点和限制

- 无内置错误校正（依赖上层 — 端到端）。
- 可变延迟/抖动（不适合实时语音/视频，除非仔细设计）。
- 复杂故障排除（云对客户不透明）。
- 遗留技术 — 比现代 Ethernet/MPLS/SD-WAN 慢。
- 安全问题（共享基础设施，无原生加密）。

### 典型用例（1990 年代–2000 年代）

- 连接分支机构到总部（星型）。
- 跨区域 LAN 互连。
- 替换多个点对点专线。
- 通过单链路承载 SNA、IP、语音 (VoFR) 和其他流量。

### 现代状态（2026 年视角）

Frame Relay 在新部署中几乎完全被淘汰。现有的安装大多是遗留环境，正在迁移到：

- MPLS VPN
- Internet VPN (IPsec、SD-WAN)
- Metro Ethernet
- 直连光纤 / DWDM 服务

然而，理解 Frame Relay 仍很有价值，用于：

- 遗留支持
- 理解 WAN 技术演进
- 虚拟电路、统计复用、CIR、拥塞通知等概念，这些在 MPLS 和 SD-WAN 中以修改形式出现。

References:

- [Introduction to Frame-Relay](https://networklessons.com/wide-area-network/introduction-to-frame-relay)
- [Comprehensive Guide to Configuring and Troubleshooting Frame Relay - Cisco](https://www.cisco.com/c/en/us/support/docs/wan/frame-relay/16563-12.html)
- [How Frame Relay Operates in Networking: A Comprehensive Guide](https://www.exam-labs.com/blog/how-frame-relay-operates-in-networking-a-comprehensive-guide)
- [Frame Relay: Advantages and Disadvantages Explained](https://www.rfwireless-world.com/terminology/frame-relay-advantages-and-disadvantages)
- [How does Frame Relay Work? - GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/how-does-frame-relay-work)
