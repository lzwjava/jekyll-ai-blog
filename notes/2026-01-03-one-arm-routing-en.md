---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: One-Arm Routing Technology Overview
translated: false
type: note
---

Question: What technology enables inter-VLAN communication using a single physical router interface?

Answer: 

The correct answer is **B) One-arm routing**.

One-arm routing (also known as router-on-a-stick) allows a router to handle communication between multiple VLANs using only a single physical interface. The interface is configured as an 802.1Q trunk, with logical subinterfaces created for each VLAN. Each subinterface is assigned an IP address in the corresponding VLAN's subnet, and the router performs inter-VLAN routing by forwarding traffic received on one subinterface to another.

- **A) Link aggregation** is incorrect—it bundles multiple physical links for increased bandwidth and redundancy but does not enable inter-VLAN routing.
- **C) Spanning Tree Protocol** is incorrect—it prevents Layer 2 loops in switched networks but has no role in inter-VLAN routing.
- **D) VRRP** is incorrect—it provides gateway redundancy (virtual IP failover) but does not facilitate routing between VLANs on a single interface.

This configuration is commonly used in smaller networks where dedicating multiple physical router interfaces to VLANs is impractical.