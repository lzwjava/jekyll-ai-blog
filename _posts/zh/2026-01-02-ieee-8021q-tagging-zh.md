---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 深入理解 IEEE 802.1Q VLAN 标记机制
translated: true
type: note
---

Question: Explain VLAN tagging in detail

Answer:

### What is VLAN Tagging?

VLAN tagging 是由 IEEE 802.1Q 标准定义的一种机制，用于在传输携带多个 VLAN 流量的链路时，识别以太网帧（Ethernet frame）属于哪个 Virtual Local Area Network (VLAN)。它允许 Switch 在共享交换机或其他设备之间的物理链路（Trunk ports）时，逻辑上分割广播域（Broadcast domains）。

如果没有 Tagging，标准的 Ethernet frames 没有字段来指示 VLAN 归属，从而无法在共享链路上区分来自不同 VLAN 的流量。

### The 802.1Q Tag Format

802.1Q 协议在以太网帧头的源 MAC 地址（Source MAC Address）与 EtherType/Length 字段之间插入一个 **4-byte (32-bit) tag**。

该 Tag 由两个主要部分组成：

- **Tag Protocol Identifier (TPID)**：16 bits，固定值为 **0x8100**。这表示该帧已标记 802.1Q。
- **Tag Control Information (TCI)**：16 bits，细分为：
  - **Priority Code Point (PCP)**：3 bits（取值 0–7），用于 Class of Service (CoS) 或 Quality of Service (QoS) 优先级排序 (IEEE 802.1p)。
  - **Drop Eligible Indicator (DEI)**：1 bit（以前称为 Canonical Format Indicator 或 CFI），用于标记在拥塞期间可以丢弃的帧。
  - **VLAN Identifier (VID)**：12 bits，指定 VLAN ID (1–4094)。VID 0 仅用于优先级标记的帧（无 VLAN ID），VID 4095 为保留值。

这使得最大 Ethernet frame 尺寸从 1518 bytes 增加到 1522 bytes，并且在 Tagging 后会重新计算 Frame Check Sequence (FCS)。

### How VLAN Tagging Works on Switches

- **Access Ports**（Untagged Ports）：连接到终端设备（如 PC）。帧以 **Untagged** 形式发送/接收。Switch 将该端口与单个 VLAN（Port VLAN ID 或 PVID）关联。进入的 Untagged 帧被分配到该 VLAN；发往该 VLAN 的传出帧将剥离任何内部 Tag。
- **Trunk Ports**（Tagged Ports）：连接 Switch 或支持 VLAN 的设备。它们承载多个 VLAN。
  - **Ingress (Incoming Frames)**：
    - Tagged frames：Switch 读取 VID 并根据其进行转发（如果该 VLAN 是被允许的）。
    - Untagged frames：分配给 **Native VLAN**（默认通常为 VLAN 1）。
  - **Egress (Outgoing Frames)**：
    - 对于非 Native VLAN：Switch 会**添加**带有相应 VID 的 802.1Q tag。
    - 对于 Native VLAN：帧以 **Untagged** 形式发送（如果内部存在 Tag 则将其剥离）。
    - 许多 Switch（例如 Cisco）会丢弃与 Native VLAN VID 匹配的传入 Tagged 帧，以防止不一致或攻击。

终端设备通常无法识别 Tag，因此 Tag 由边缘的 Switch 进行添加/删除。

### Native VLAN

Native VLAN 处理 Trunk ports 上的 **Untagged traffic**：
- 传入的 Untagged 帧被放置在 Native VLAN 中。
- 发往 Native VLAN 的传出帧以 Untagged 形式发送。
- Trunk 链路两端的 Native VLAN 必须匹配，以避免不匹配（这可能导致 CDP 警告或丢帧等问题）。
- 最佳实践：出于安全性考虑，将 Native VLAN 从默认的 VLAN 1 更改为其他 ID（以减轻 VLAN hopping 攻击）。

### Benefits and Use Cases

- 允许跨 Switch 扩展 VLAN，而无需为每个 VLAN 设置专用链路。
- 通过 PCP 支持 QoS。
- 保持与不支持 Tagging 的设备的向后兼容性。

### Potential Issues

- Native VLAN 不匹配可能导致意外转发或安全风险。
- 双重标记（Double tagging，如 QinQ, 802.1ad）可用于提供商网络扩展，但增加了复杂性。

VLAN tagging 对于企业环境中高效、安全的跨 VLAN 网络至关重要。

References:

- [IEEE 802.1Q - Wikipedia](https://en.wikipedia.org/wiki/IEEE_802.1Q)
- [Fundamentals of 802.1Q VLAN Tagging - Cisco Meraki Documentation](https://documentation.meraki.com/Platform_Management/Dashboard_Administration/Design_and_Configure/Configuration_Guides/Routing_and_Firewall/Fundamentals_of_802.1Q_VLAN_Tagging)
- [802.1Q Encapsulation Explained - NetworkLessons](https://networklessons.com/switching/802-1q-encapsulation-explained)
- [Tagged, Untagged, and Native VLANs - Network Direction](https://networkdirection.net/articles/network-theory/taggeduntaggedandnativevlans/)
