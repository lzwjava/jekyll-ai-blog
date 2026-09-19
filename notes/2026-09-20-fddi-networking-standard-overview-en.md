---
audio: false
generated: true
image: false
lang: en
layout: post
title: FDDI Networking Standard Overview
translated: false
type: note
---

Question: What is FDDI in networking?

Answer:

FDDI (Fiber Distributed Data Interface) is a high-speed networking standard that uses fiber optic cables to transmit data at 100 Mbps over a dual-ring topology. Here's a breakdown of its key aspects:

**Architecture**

- Uses two counter-rotating token rings (primary and secondary) for redundancy
- If the primary ring fails, the secondary ring automatically takes over — this is called "ring wrapping"
- Supports up to **500 nodes** per network and a maximum ring length of **200 km**

**Key Characteristics**

- Data rate: **100 Mbps**
- Uses a **token-passing** access method (similar to Token Ring)
- Originally designed for use as a **backbone network** connecting multiple LANs
- Operates at the **Physical and Data Link layers** (OSI Layer 1 & 2)

**Types of FDDI Nodes**

- **DAS (Dual Attachment Station)** — connected to both rings; more fault-tolerant
- **SAS (Single Attachment Station)** — connected only to the primary ring via a concentrator

**Advantages**

- High reliability due to dual-ring redundancy
- Long-distance coverage (up to 200 km)
- Good fault tolerance and self-healing capability

**Limitations**

- Expensive to implement compared to Ethernet
- Largely **obsolete** today — replaced by Fast Ethernet, Gigabit Ethernet, and modern fiber standards like 10GbE

**Use Cases (Historical)**

- Campus and enterprise backbone networks
- Medical imaging and CAD/CAM environments requiring high bandwidth in the 1990s

---

References:

- [FDDI – Wikipedia](https://en.wikipedia.org/wiki/Fiber_Distributed_Data_Interface)
- [FDDI Overview – GeeksforGeeks](https://www.geeksforgeeks.org/fddi-full-form/)
- [Network Topologies and Standards – Cisco Press](https://www.ciscopress.com)
