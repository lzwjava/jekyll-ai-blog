---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: RIP Uses Hop Count Metric
translated: false
type: note
---

Question: Which routing protocol uses hop count as its metric?  
A) OSPF  
B) RIP  
C) BGP  
D) EIGRP

Answer: 

The correct answer is **B) RIP**.

- **RIP (Routing Information Protocol)**: Uses hop count (the number of routers a packet must pass through) as its primary and only metric. The maximum hop count is 15, and 16 indicates an unreachable network.
- **OSPF (Open Shortest Path First)**: Uses cost, primarily based on bandwidth (cumulative interface costs), not hop count.
- **BGP (Border Gateway Protocol)**: Uses path attributes like AS path length, local preference, and others; hop count is not its metric.
- **EIGRP (Enhanced Interior Gateway Routing Protocol)**: Uses a composite metric based on bandwidth, delay, load, reliability, and MTU (though bandwidth and delay are the primary factors); it does not rely solely on hop count.

RIP is the classic distance-vector protocol designed for smaller networks where simplicity (hop count) is prioritized over more accurate metrics like bandwidth.