---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Interior Gateway Protocols Explained
translated: false
type: note
---

Question: What are Interior Gateway Protocols?

Answer:

Interior Gateway Protocols (IGPs) are a class of routing protocols used to exchange routing information between routers within a single **autonomous system (AS)**—a network or group of networks under common administration, such as a corporate or ISP network.

IGPs enable routers to dynamically discover and maintain routes for efficient packet forwarding inside the AS, using metrics like bandwidth, delay, or hop count to determine the best paths.

### Key Characteristics
- **Scope**: Limited to one AS.
- **Contrast with EGPs**: Unlike Exterior Gateway Protocols (e.g., BGP), which handle routing between different ASes on the internet, IGPs focus solely on internal routing.

### Main Types of IGPs
IGPs are generally categorized into three types:

- **Distance-Vector Protocols**
  Routers share their entire routing table with neighbors, using simple metrics (e.g., hop count).
  Example: **Routing Information Protocol (RIP)** – Simple but limited scalability (max 15 hops).

- **Link-State Protocols**
  Routers flood link-state advertisements to build a complete network topology map, then compute shortest paths (e.g., via Dijkstra's algorithm). Faster convergence and better scalability.
  Examples:
  - **Open Shortest Path First (OSPF)** – Widely used, supports large networks.
  - **Intermediate System to Intermediate System (IS-IS)** – Similar to OSPF, often in ISP environments.

- **Hybrid/Advanced Distance-Vector Protocols**
  Combine distance-vector simplicity with link-state features for faster convergence.
  Example: **Enhanced Interior Gateway Routing Protocol (EIGRP)** – Originally Cisco-proprietary, now open standard; uses composite metrics.

As of 2025, the most commonly deployed IGPs remain OSPF, IS-IS, and EIGRP, with RIP used mainly in small or legacy networks.

References:

- [Interior gateway protocol - Wikipedia](https://en.wikipedia.org/wiki/Interior_gateway_protocol)
- [Understanding Interior Gateway Protocol (IGP) - JumpCloud](https://jumpcloud.com/it-index/understanding-interior-gateway-protocol-igp)
- [Routing: IGP and EGP Protocols | Baeldung on Computer Science](https://www.baeldung.com/cs/routing-igp-egp-protocols)
- [IGP, EGP, and Autonomous System Explained](https://www.computernetworkingnotes.com/ccna-study-guide/igp-egp-and-autonomous-system-explained.html)
