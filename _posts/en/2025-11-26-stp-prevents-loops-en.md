---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: STP Prevents Switching Loops
translated: false
type: note
---

**Correct Answer: B) STP (Spanning Tree Protocol)**

### Detailed Analysis of Each Option

- **A) VLAN**
  VLANs (Virtual Local Area Networks) are used to segment a physical network into multiple logical broadcast domains for security, performance, and management purposes.
  → VLANs **do not prevent switching loops**. A loop can still occur within a single VLAN if there are redundant physical links between switches.

- **B) STP (Spanning Tree Protocol)**
  This is the **correct answer**.
  STP (defined in IEEE 802.1D, with modern variants like RSTP 802.1w and MSTP 802.1s) runs on switches in a LAN and performs the following:
  - Elects a **root bridge** (the switch with the lowest Bridge ID).
  - Determines the best path to the root bridge for every switch.
  - Places redundant ports into **blocking state** so that only one active path exists between any two points in the network.
  - Continuously monitors the topology and recalculates if a link fails (convergence).
  → Its primary purpose is **to prevent Layer-2 bridging loops** that would otherwise cause broadcast storms, MAC table instability, and network meltdown.

- **C) OSPF**
  Open Shortest Path First is a **Layer-3 (IP) routing protocol** used in routed networks (routers, not switches).
  It calculates shortest paths using Dijkstra’s algorithm and builds loop-free routing tables.
  → It does **not run on switches** and has nothing to do with preventing Layer-2 loops in a switched LAN.

- **D) RIP**
  Routing Information Protocol is another **Layer-3 routing protocol** (distance-vector).
  Like OSPF, it operates on routers, not switches, and is irrelevant to Layer-2 loop prevention.

### Why STP is Essential in Redundant Switched Topologies
In a network with multiple switches connected by redundant links (common for high availability), a frame can loop forever (broadcast storm) without a loop-prevention mechanism. STP solves this by logically breaking loops while keeping physical redundancy for failover.

### Quick Summary Table

| Option | Layer   | Device     | Prevents L2 Loops? | Purpose                              |
|--------|---------|------------|---------------------|--------------------------------------|
| A) VLAN| L2      | Switch     | No                  | Broadcast domain segmentation        |
| B) STP | L2      | Switch     | Yes                 | Blocks redundant paths → no loops    |
| C) OSPF| L3      | Router     | No (L3)             | IP routing, loop-free forwarding     |
| D) RIP | L3      | Router     | No (L3)             | Simple IP routing                    |

**Final Answer: B) STP (Spanning Tree Protocol)** is the protocol specifically designed to prevent loops in switched LANs by blocking redundant paths.
