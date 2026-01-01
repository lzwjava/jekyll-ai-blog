---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: VLAN 标记与端口帧处理
translated: true
type: note
---

Question: How does the overall process of VLAN tagging and frame handling work on switch ports, particularly with access ports and tagged frames?

Answer: 

### VLANs 和 Switch Ports 概述

Virtual Local Area Networks (VLANs) 将物理网络分割为逻辑广播域。Switches 主要使用两种端口类型来处理 VLAN：

- **Access ports**：连接到不识别 VLAN tags 的终端设备（如 PC、打印机）。一个 access port 仅属于**一个特定的 VLAN**（配置为 access VLAN）。
- **Trunk ports**：连接到其他 switches 或支持 VLAN 的设备。它们承载**多个 VLAN** 的流量，使用 802.1Q tags 来识别每个 frame 属于哪个 VLAN。

IEEE 802.1Q 标准通过在 Ethernet frame header 中插入一个 4-byte 的 tag（包含 VLAN ID）来定义 VLAN tagging。

### Access Ports 上的 Frame 处理

**Ingress（进入 access port 的数据帧）：**

- **Untagged frames**（来自终端设备的普通帧）：Switch 内部将该 frame 分配给配置的 access VLAN。在线路上的 frame 中不会添加 tag；tagging 仅在内部处理以进行 switching 决策。
- **Tagged frames**：Access ports 预期仅接收 untagged traffic。接收到 tagged frame 被视为无效。
  - 在大多数现代 Cisco switches（如 Catalyst 2960 及更高版本）中，**所有 tagged frames 都会被丢弃 (dropped)**。
  - 在某些旧型号（如 2950、3550，以及某些情况下的 Nexus）上，如果 tag 与 access VLAN ID 匹配，则剥离 tag 并处理该 frame；否则丢弃。
  - 总体标准行为（特别是在 CCNA/CCNP 等考试语境下）：**丢弃所有 tagged frames**，以维护安全并防止 VLAN hopping 攻击。

**Egress（从 access port 发出的数据帧）：**

- 发往所连设备的 Frames：Switch **移除任何内部 VLAN tag** 并以 untagged 形式发送该 frame。

### Trunk Ports 上的 Frame 处理

**Ingress：**

- **Tagged frames**：如果 VLAN ID 在 trunk 允许范围内则进行处理；否则丢弃。
- **Untagged frames**：分配给 **native VLAN**（默认为 VLAN 1）。注意：Trunk ports 可以接收 native VLAN 的 untagged frames。

**Egress：**

- 非 native VLAN 的 Frames：添加 802.1Q tag 后发送。
- Native VLAN 的 Frames：以 untagged 形式发送（除非全局配置了 "vlan dot1q tag native"，该配置会为所有内容打 tag 并丢弃 untagged ingress）。

### 整体 Frame 流程示例（Host A 在 VLAN 10 → 通过两个 switches → Host B 在 VLAN 10）

1. Host A 发送一个 **untagged** frame。
2. Switch1 的 access port 接收它 → 内部分配到 VLAN 10。
3. Switch1 内部转发 → 到 trunk port → 添加 VLAN 10 tag → 发送到 Switch2。
4. Switch2 的 trunk port 接收 tagged frame → 验证 VLAN 10 已允许 → 如果转发到 access port 则移除 tag。
5. Switch2 的 access port 向 Host B 发送 **untagged** frame。

这确保了终端设备只看到 untagged traffic，而 switches 在内部和 trunks 上使用 tags 进行正确的分割。

### 为什么 Access Ports 会丢弃 Tagged Frames

- Security：防止恶意设备通过注入 tagged traffic 来访问未授权的 VLAN（VLAN hopping）。
- Design：终端设备不应该发送 tags。

此行为符合 IEEE 802.1Q 原则和 Cisco 最佳实践。

References:  

- [Cisco Community: Tagged frames on access ports](https://community.cisco.com/t5/switching/tagged-frames-on-access-ports/td-p/1074967)
- [Network Engineering Stack Exchange: What happens with tagged traffic on access port of Cisco switch?](https://networkengineering.stackexchange.com/questions/28888/what-happens-with-tagged-traffic-on-access-port-of-cisco-switch)
- [NetworkLessons: VLANs - when a tagged frame arrives on an access port](https://notes.networklessons.com/vlans-when-a-tagged-frame-arrives-on-an-access-port)
- [Cisco: Understanding VLAN Tagging](https://www.cisco.com/c/en/us/support/docs/lan-switching/vlan/17056-741.html)