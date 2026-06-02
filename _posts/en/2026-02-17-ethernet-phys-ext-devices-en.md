---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ethernet Physical Layer Extension Devices
translated: false
type: note
---

Question: Ethernet expansion is divided into physical layer extension and data link layer extension. The main devices used for physical layer extension are repeaters (Repeater) and what other device?

A. Hub
B. Bridge
C. Switch
D. Router

Answer:

**A. Hub**

**Detailed explanation:**

Ethernet network extension methods are classified based on the layer at which the extending device operates:

- **Physical layer extension** (Layer 1):
  Devices operate at the bit/signal level and simply amplify, regenerate, or repeat the electrical/optical signals to extend the transmission distance or connect more devices. They do **not** understand frame structure or MAC addresses.
  Main devices used:
  - **Repeater** — regenerates and forwards signals in both directions (classic device for extending cable length)
  - **Hub** (also called multi-port repeater) — a multi-port repeater that connects multiple devices in a star topology, broadcasting all received frames to every port (except the incoming one). It operates purely at the physical layer.

- **Data link layer extension** (Layer 2):
  Devices understand MAC addresses and Ethernet frames. They can filter traffic, reduce collisions, and create separate collision domains.
  Main devices used:
  - **Bridge** — connects two network segments, forwards frames based on MAC addresses, and learns addresses via a forwarding table
  - **Switch** (Layer 2 switch) — a multi-port bridge that creates separate collision domains for each port (full-duplex communication possible), greatly improving performance

**Why the other options are incorrect:**

- **B. Bridge** → Operates at **data link layer** (Layer 2), used for data link layer extension
- **C. Switch** → Also operates at **data link layer** (Layer 2), modern replacement for bridges/hubs, used for data link layer extension
- **D. Router** → Operates at **network layer** (Layer 3), connects different networks using IP addresses, not used for simple Ethernet extension

**Summary table of devices and their layers:**

| Device     | OSI Layer     | Main Function in Ethernet Extension          | Collision Domains Created |
|------------|---------------|----------------------------------------------|----------------------------|
| Repeater   | Physical (1)  | Signal regeneration, distance extension      | 1 (shared)                |
| Hub        | Physical (1)  | Multi-port repeater, star topology           | 1 (shared)                |
| Bridge     | Data Link (2) | Segment isolation, MAC-based forwarding      | 2 (one per segment)       |
| Switch     | Data Link (2) | Multi-port bridge, per-port collision domain | 1 per port                |
| Router     | Network (3)   | Connects different networks/subnets          | N/A (different networks)  |

Your previous answer (C. Switch) was incorrect because switches operate at the data link layer, not the physical layer.

The correct answer is **A. Hub**.

References:

- None (standard computer networking and Ethernet extension concepts from IEEE 802.3 and common textbooks)
