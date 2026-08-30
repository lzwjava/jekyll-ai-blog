---
audio: false
generated: true
image: false
lang: en
layout: post
title: VLANs and Trunks Explained
translated: false
type: note
---

Question: What is a VLAN, and what is a trunk (in networking)?

Answer:

**VLAN (Virtual Local Area Network)**

A VLAN is a logical segmentation of a physical network into multiple isolated broadcast domains. Even if devices are connected to the same physical switch, VLANs allow you to group them as if they were on separate networks. Key points:

- Each VLAN has its own ID (e.g., VLAN 10, VLAN 20)
- Traffic in one VLAN cannot reach another without going through a router or Layer 3 switch
- Improves security, reduces broadcast traffic, and simplifies network management
- Example: separating HR, Finance, and Engineering departments on the same physical switch

**Trunk (Trunk Link)**

A trunk is a network link that carries traffic from **multiple VLANs simultaneously** between switches, routers, or other network devices. Key points:

- Uses tagging protocols (most commonly **IEEE 802.1Q**) to label each frame with its VLAN ID
- Allows a single physical cable to transport many VLANs at once
- Typically used for switch-to-switch or switch-to-router connections
- The opposite of a trunk is an **access port**, which carries traffic for only one VLAN

**Simple Analogy**

| Concept | Analogy |
| --- | --- |
| VLAN | A separate lane on a highway |
| Trunk | The highway itself carrying all lanes |

References:

- [IEEE 802.1Q – VLAN Tagging](https://en.wikipedia.org/wiki/IEEE_802.1Q)
- [Cisco – VLAN Overview](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4500/12-2/25ew/configuration/guide/conf/vlans.html)
- [Cisco – Trunking Concepts](https://www.cisco.com/c/en/us/support/docs/lan-switching/8021q/17056-741-4.html)
