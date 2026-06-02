---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Distance Vector vs Path Vector Protocols
translated: false
type: note
---

**Question:** What are distance-vector and path-vector routing protocols? What is the difference between them, especially since path-vector is described as an advanced form of distance-vector?

**Answer:**

Distance-vector and path-vector are two classes of dynamic routing protocols used in computer networks to determine the best paths for forwarding packets.

### Distance-Vector Routing Protocols

- Routers exchange **vectors** (lists) of known destinations along with a **distance metric** (e.g., hop count or composite metric) to each destination.
- Each router shares its entire routing table periodically with directly connected neighbors.
- Routers do not have knowledge of the full path—only the distance and the next-hop neighbor.
- They use algorithms like Bellman-Ford to compute the lowest-cost path.
- Common issues: Susceptible to routing loops and the "count-to-infinity" problem (mitigated by techniques like split horizon and poison reverse).
- Examples: RIP (Routing Information Protocol), IGRP.
- Typically used in smaller, intra-domain (interior gateway) environments.

### Path-Vector Routing Protocols

- An enhanced or advanced variant of distance-vector, specifically designed for large-scale, inter-domain routing.
- Routers exchange not only a metric (often AS path length) but also the **full path** (sequence of autonomous systems or nodes traversed).
- This path information is appended as routes are advertised, allowing easy detection and prevention of loops (if a router sees its own identifier in the path, it discards the route).
- Supports complex policy-based routing (e.g., preferring certain paths for business or security reasons).
- Primary example: BGP (Border Gateway Protocol), the protocol that glues the Internet together by routing between autonomous systems (ASes).
- No periodic full table updates like classic distance-vector; updates are incremental and triggered.

### Key Differences

| Aspect                  | Distance-Vector                          | Path-Vector                              |
|-------------------------|------------------------------------------|------------------------------------------|
| Information Shared     | Distance/metric + next hop               | Full path (e.g., AS sequence) + metric   |
| Loop Prevention        | Relies on heuristics (e.g., split horizon) | Inherent (checks own ID in path)        |
| Scalability            | Limited (intra-domain, smaller networks) | High (inter-domain, Internet-scale)     |
| Policy Support         | Minimal                                  | Extensive (path attributes for decisions)|
| Convergence            | Slower, prone to count-to-infinity       | Slower but stable, policy-driven        |
| Typical Use            | Interior routing (e.g., within an organization) | Exterior routing (between ASes)         |

Path-vector is considered "advanced" because it addresses key limitations of traditional distance-vector protocols—particularly routing loops and lack of policy control—by including explicit path information, making it suitable for the global Internet.

References:

- [Path-vector routing protocol - Wikipedia](https://en.wikipedia.org/wiki/Path-vector_routing_protocol)
- [What is the difference between distance vector protocol and path vector protocol - Network Engineering Stack Exchange](https://networkengineering.stackexchange.com/questions/5595/what-is-the-difference-between-distance-vector-protocol-and-path-vector-protocol)
- [Path Vector vs Distance Vector - Lab1918](https://lab1918.com/posts/dv-vs-ps/)
- [Routing Protocols Compared - Packetcoders](https://www.packetcoders.io/routing-protocols-compared-distance-vector-path-vector-link-state-and-hybrid/)
- [Distance Vector, Link State, and Path Vector - InformIT](https://www.informit.com/articles/article.aspx?p=331613&seqNum=2)
