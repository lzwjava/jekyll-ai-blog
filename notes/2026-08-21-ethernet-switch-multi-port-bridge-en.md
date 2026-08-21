---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Ethernet Switch: Multi-Port Bridge"
translated: false
type: note
---

Question: What is an Ethernet switch, why does it work at the Data Link Layer, and what is a "bridge" — and why is a switch called a "multi-port bridge"?

Answer:

## What is a Bridge (网桥)?

A **bridge** is a network device that connects two or more network segments and forwards frames between them based on **MAC addresses**. It operates at **Layer 2 (Data Link Layer)** of the OSI model.

Key behaviors of a bridge:

- It reads the **source MAC address** of incoming frames to learn which device is on which port
- It reads the **destination MAC address** to decide where to forward the frame
- It maintains a **MAC address table** (also called a forwarding table)
- It **filters traffic** — it only forwards a frame to the segment where the destination actually lives

## Why is an Ethernet Switch a "Multi-Port Bridge"?

A traditional bridge typically has **only 2 ports** — connecting two segments.

An Ethernet switch is essentially the **same concept, but scaled up** to many ports (8, 24, 48, etc.). Each port on a switch is its own **collision domain**, just like a bridge separating two segments.

| Feature | Traditional Bridge | Ethernet Switch |
| --- | --- | --- |
| Ports | 2 (typically) | Many (8–48+) |
| MAC learning | ✅ | ✅ |
| Forwarding by MAC | ✅ | ✅ |
| OSI Layer | Layer 2 | Layer 2 |
| Collision domains | 2 | One per port |

So a switch = a bridge with **many ports** → "multi-port bridge."

## Why Layer 2 (Data Link Layer)?

Because the switch makes forwarding decisions based on **MAC addresses**, which are Layer 2 addresses. It does **not** look at IP addresses (that's Layer 3 / routers).

The Data Link Layer is responsible for:

- **MAC addressing**
- **Frame formatting**
- **Error detection** (CRC)
- **Access control** to the physical medium

A switch reads and uses all of these — so it lives at Layer 2.

## Quick Summary

```
Physical Layer (L1)  →  Hub (repeats all signals blindly)
Data Link Layer (L2) →  Switch / Bridge (forwards by MAC address) ✅
Network Layer (L3)   →  Router (forwards by IP address)
```

References:

- [OSI Model - Cisco](https://www.cisco.com/c/en/us/solutions/enterprise-networks/what-is-osi-model.html)
- [Network Bridges vs Switches - Cloudflare](https://www.cloudflare.com/learning/network-layer/what-is-a-network-bridge/)
