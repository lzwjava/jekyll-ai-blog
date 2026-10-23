---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Hub: Layer 1 Broadcasting Device"
translated: false
type: note
---

Question: What does "hub" mean in networking?

Answer:

A **hub** is a basic Layer 1 (Physical Layer) network device used to connect multiple devices in a Local Area Network (LAN). Here's how it works:

**Core behavior:**

- When a hub receives a data packet on one port, it **broadcasts** (copies and sends) that packet out to **all other ports**, regardless of the intended destination.
- It has no intelligence — it doesn't know which device is connected to which port, and it doesn't filter or direct traffic.

**Key characteristics:**

- Operates at the **OSI Physical Layer (Layer 1)**
- Creates a single **collision domain** — only one device can transmit at a time, or data collides and must be retransmitted
- All connected devices share the same bandwidth
- Half-duplex communication only

**Hub vs. Switch vs. Router:**

| Device | Layer | Traffic Handling |
| -------- | ------- | ----------------- |
| Hub | L1 | Broadcasts to all ports |
| Switch | L2 | Forwards only to the target MAC address |
| Router | L3 | Routes between different networks using IP |

**Why hubs are obsolete:**
Because hubs broadcast everything to every device, they create unnecessary network congestion and are a security risk (any device can "sniff" all traffic). **Switches** replaced hubs in virtually all modern networks, as they are smarter, faster, and more secure.

References:

- [Network Hub – Wikipedia](https://en.wikipedia.org/wiki/Ethernet_hub)
- [Hub vs Switch vs Router – Cisco](https://www.cisco.com/c/en/us/solutions/small-business/resource-center/networking/network-switch-vs-router.html)
