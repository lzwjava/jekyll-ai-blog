---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Link Aggregation Benefits and Uses
translated: false
type: note
---

Question: What is link aggregation in networking?

Answer: 

Link aggregation, also known as **Ethernet bonding**, **port trunking**, **link bundling**, or **NIC teaming**, is a networking technique that combines multiple physical network links (such as Ethernet ports or cables) into a single logical link. This provides higher bandwidth, redundancy, and improved performance.

### Key Benefits
- **Increased Bandwidth**: Traffic is distributed across the aggregated links, allowing throughput greater than a single link can provide. For example, aggregating four 1 Gbps links can theoretically provide up to 4 Gbps of bandwidth.
- **Load Balancing**: Incoming and outgoing traffic is balanced across the member links using algorithms (e.g., based on source/destination MAC addresses, IP addresses, or ports).
- **Fault Tolerance/Redundancy**: If one physical link fails, traffic is automatically redistributed to the remaining links without interrupting the connection.
- **No Single Point of Failure** (for the link itself).

### Common Standard
The most widely used standard is **IEEE 802.1AX** (previously known as 802.3ad), which defines the **Link Aggregation Control Protocol (LACP)**. LACP is a dynamic protocol that negotiates and maintains the aggregation between devices.

### Modes
- **Static Aggregation**: Manually configured on both ends; no protocol negotiation.
- **Dynamic Aggregation (LACP)**: Preferred method; automatically negotiates aggregation and detects faults.

### Requirements
- Both ends of the connection (e.g., switch and server, or switch-to-switch) must support and be configured for link aggregation.
- Member links should have the same speed, duplex mode, and typically the same VLAN configuration.
- Devices often limit the number of links per group (e.g., 8 links max).

### Common Use Cases
- Connecting servers with NIC teaming to switches for higher bandwidth and failover.
- Switch-to-switch uplinks in data centers or enterprise networks.
- Improving performance in storage networks (e.g., iSCSI or NAS).

### Limitations
- It does **not** increase the speed of a single traffic flow beyond the speed of one member link (due to load balancing hashing).
- For a single connection (e.g., one TCP session), traffic typically uses only one physical link.

In summary, link aggregation is an effective way to scale bandwidth and provide redundancy between two directly connected devices without requiring higher-speed individual interfaces.