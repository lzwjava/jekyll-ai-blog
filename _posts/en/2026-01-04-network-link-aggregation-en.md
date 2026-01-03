---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Benefits of Network Link Aggregation
translated: false
type: note
---

Question: What is the primary benefit of link aggregation?

Answer: 

The correct answer is **B) It increases bandwidth and provides redundancy on backbone links**.

Link aggregation (also known as EtherChannel in Cisco terminology, or LACP/IEEE 802.1AX) combines multiple physical Ethernet links into a single logical link. This primarily achieves two key benefits:

- **Increased bandwidth**: Traffic is load-balanced across the bundled links, allowing higher aggregate throughput than a single link could provide.
- **Redundancy/fault tolerance**: If one physical link fails, traffic is redistributed over the remaining links, preventing outage.

The other options are incorrect because:
- **A)** Preventing network loops is the role of Spanning Tree Protocol (STP), not link aggregation.
- **C)** Automatic IP address assignment is handled by DHCP.
- **D)** Traffic encryption between switches is provided by protocols like MACsec, not link aggregation.