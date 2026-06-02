---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Broadcast Storm Caused by Network Loops
translated: false
type: note
---

Question: In a switched network, what causes a broadcast storm?

Answer:

The correct answer is **B) Network loops without STP**.

### Explanation

In an Ethernet switched network, broadcast frames (such as ARP requests) are forwarded out of all ports except the incoming port by every switch. If there is a **loop** in the network topology (e.g., two switches connected by multiple links without proper controls), a broadcast frame can circulate indefinitely:

- The frame enters the loop, gets flooded by each switch, and keeps looping around.
- Each iteration multiplies the number of broadcast frames, rapidly consuming bandwidth and CPU resources on switches and end devices.

This phenomenon is known as a **broadcast storm**.

**Spanning Tree Protocol (STP)** prevents this by detecting loops and logically blocking redundant paths, ensuring a loop-free topology while maintaining redundancy for failover.

### Why not the other options?

- **A) Too many unicast frames**: Unicast floods can occur with unknown destinations, but they do not multiply exponentially like broadcasts in a loop, and do not typically cause a "broadcast" storm.
- **C) Misconfigured VLANs**: This can cause issues like unintended traffic leakage or isolation problems, but it does not create endless frame multiplication leading to a broadcast storm.
- **D) High bandwidth usage**: This is a symptom or result of various problems (including a broadcast storm), but it is not the root cause of a broadcast storm itself.

Thus, the primary cause of a broadcast storm in a switched network is the presence of **network loops without STP** (or another loop-prevention mechanism).
