---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bridge vs Switch Differences
translated: false
type: note
---

Question: What is the difference between a Bridge and a Switch?

Answer:

Both operate at **Layer 2 (Data Link Layer)** and use MAC addresses to forward frames, but they differ in several ways:

| Feature | Bridge | Switch |
| --- | --- | --- |
| **Ports** | Typically 2–4 ports | Many ports (8, 24, 48…) |
| **Processing** | Software-based | Hardware-based (ASICs) |
| **Speed** | Slower | Much faster |
| **Forwarding** | Store-and-forward only | Store-and-forward + cut-through |
| **Collision domains** | One per port | One per port |
| **Usage today** | Largely obsolete | Standard in modern networks |

**Key insight:** A switch is essentially a **multi-port bridge** — it does the same job (learning MAC addresses, filtering/forwarding frames between segments) but at much greater scale and speed.

Historically, bridges were used to connect two LAN segments. Switches replaced them by bringing the same logic to every single port, making each device its own isolated collision domain.

> Both still share one broadcast domain per VLAN, which is why routers (Layer 3) are needed to separate broadcast traffic.

References:

- [Network Bridge - Wikipedia](https://en.wikipedia.org/wiki/Network_bridge)
- [Network Switch - Wikipedia](https://en.wikipedia.org/wiki/Network_switch)
