---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: Ethernet Switch in OSI Model
translated: false
type: note
---

The question asks at which layer of the OSI model an Ethernet switch operates.

## Correct Answer: **B (Data Link Layer)**

### Explanation

An **Ethernet switch** is a multi-port network bridge that operates at **Layer 2 (Data Link Layer)** of the OSI seven-layer reference model.

### Why Data Link Layer?

**Key characteristics of Ethernet switches:**

- **MAC Address Processing**: Switches make forwarding decisions based on **MAC addresses** (physical addresses), which are defined at Layer 2
- **Frame Forwarding**: They forward Ethernet frames from one port to another based on the destination MAC address in the frame
- **Learning and Filtering**: Switches learn MAC addresses from incoming frames and build MAC address tables to determine where to forward frames
- **No IP Address Involvement**: Unlike routers (Layer 3 devices), switches don't examine IP addresses

### Why Not Other Layers?

- **Physical Layer (A)**: Hubs operate at this layer, not switches
- **Network Layer (C)**: Routers operate at this layer, making decisions based on IP addresses
- **Transport Layer (D)**: This layer handles end-to-end communication and protocols like TCP/UDP

### Additional Note

Ethernet switches are also called **Layer 2 switches** or **Layer 2 devices** because they operate specifically at the Data Link Layer, making them more intelligent than hubs but less capable than routers in terms of network-layer routing.

**Congratulations! Your answer was correct! ✓**
