---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: OSPF Routing Protocol Type
translated: false
type: note
---

Question: Which type of routing protocol is OSPF?

Answer:

OSPF (Open Shortest Path First) is a **Link State** routing protocol.

### Explanation

- **Link State** protocols (like OSPF and IS-IS) flood detailed topology information (link states) throughout the routing domain. Each router builds a complete map of the network and uses Dijkstra's Shortest Path First (SPF) algorithm to calculate the best paths to all destinations.
- In contrast:
  - **Distance Vector** protocols (e.g., RIP, EIGRP in its classic mode) share only distance metrics and next-hop information with neighbors, without full topology visibility.
  - **Path Vector** protocols (e.g., BGP) exchange full path attributes (AS paths) to prevent loops in inter-domain routing.
  - **Hybrid** protocols (sometimes used to describe EIGRP) combine elements of both distance vector and link state but are not pure link state.

Thus, the correct answer is **B) Link State**.

(Note: Option A is incorrect as it applies to protocols like RIP.)
