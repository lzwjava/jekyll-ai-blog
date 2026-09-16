---
audio: false
generated: true
image: false
lang: en
layout: post
title: Broadcast Network Overview
translated: false
type: note
---

Question: What is a broadcast network (广播式网络)?

Answer: A **broadcast network** is a type of communication network where data transmitted by one node is received by **all other nodes** on the same network simultaneously — whether or not those nodes are the intended recipients.

Key characteristics:

- **Single shared channel**: All nodes share the same transmission medium (e.g., a cable or wireless frequency).
- **One-to-all delivery**: When a node sends a packet, every other node on the network receives it.
- **Address filtering**: Each node inspects the destination address in the packet and decides whether to process it or discard it.
- **No routing needed**: Unlike point-to-point networks, there's no need to route data through intermediate nodes.

Common examples:

- **Ethernet (early bus topology)** — all devices on the same segment receive every frame.
- **Wi-Fi (802.11)** — frames are broadcast over radio waves to all devices in range.
- **Cable TV networks** — the same signal is distributed to all subscribers.
- **Satellite broadcasting** — one uplink transmits to all receivers in the footprint.

Contrast with **点对点网络 (point-to-point network)**, where data travels through a dedicated link between exactly two nodes, and routing is required to reach a destination.

In modern networking, broadcast domains are typically segmented using **switches** and **VLANs** to reduce unnecessary broadcast traffic and improve efficiency.

References:

- [Broadcast Network – Wikipedia](https://en.wikipedia.org/wiki/Broadcast_network)
- [Broadcast vs Point-to-Point – Cisco](https://www.cisco.com/c/en/us/tech/lan-switching/ethernet-technologies/index.html)
