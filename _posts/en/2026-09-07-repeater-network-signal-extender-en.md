---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Repeater: Network Signal Extender"
translated: false
type: note
---

Question: What is a "中继器" (Repeater) in the context of internet/network extension devices?

Answer:

A **repeater** (中继器) is a network device that **receives a signal and retransmits it at a higher power level**, allowing the signal to travel longer distances without degrading. Here's a breakdown:

**Core Function**

- Operates at **Layer 1 (Physical Layer)** of the OSI model
- It simply amplifies or regenerates signals — it does *not* filter, route, or interpret data
- Works with both wired and wireless signals

**Common Use Cases**

- Extending Wi-Fi coverage in large homes or offices (wireless repeater / Wi-Fi extender)
- Extending Ethernet cable runs beyond the standard 100-meter limit
- Boosting cellular signals in dead zones

**Types**

- **Wired repeater** — used in older coaxial or twisted-pair networks
- **Wireless repeater / Wi-Fi extender** — the most common modern form; connects to your router wirelessly and rebroadcasts the signal
- **Optical repeater** — used in fiber optic networks to regenerate light signals

**Repeater vs. Similar Devices**

| Device | OSI Layer | Intelligence |
| --- | --- | --- |
| Repeater (中继器) | Layer 1 | None — just boosts signal |
| Bridge (桥接器) | Layer 2 | Filters by MAC address |
| Router (路由器) | Layer 3 | Routes by IP address |
| Switch (交换机) | Layer 2–3 | Switches by MAC/IP |

**Key Limitation**: Because it blindly repeats everything — including noise and collisions — it doesn't improve network *efficiency*, only *reach*.

References:

- [Repeater – Wikipedia](https://en.wikipedia.org/wiki/Repeater)
- [What is a Network Repeater? – Cisco](https://www.cisco.com/c/en/us/products/switches/what-is-a-network-switch.html)
- [Wi-Fi Extenders vs. Repeaters – HowToGeek](https://www.howtogeek.com/845669/wi-fi-extender-vs-repeater-whats-the-difference/)
