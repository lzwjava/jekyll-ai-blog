---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ethernet Switches Versus Passive RJ45 Splitters
translated: false
type: note
---

Question: If I connect one WAN port from the router to my 5-port Gigabit Ethernet switch (like Mercusys SG105 series), and then connect my laptop and other devices to the remaining ports on the switch, can those devices access the internet? Is this different from a simple RJ45 splitter that only allows one downstream device?

Answer:

**Yes, your laptop and other devices connected to the switch will be able to access the internet.**

A 5-port unmanaged Gigabit Ethernet switch (such as Mercusys MS105G, SG105, SG105C, etc.) works completely differently from a passive RJ45 splitter / Y-splitter.

Here's the key difference:

- **Passive RJ45 splitter / 1-to-2 adapter**
  These are not real network switches. They try to split a single 100 Mbps Ethernet connection (usually only using 2 pairs of wires) into two connections.
  → They only support **one active downstream device** at a time.
  → They do not work properly (or at all) with Gigabit Ethernet.
  → They cause serious performance problems or simply don't work when more than one device tries to communicate.

- **Real Ethernet switch (your 5-port device)**
  This is a proper, active, multi-port network switch (even though it's unmanaged).
  It has its own internal switching chip that can:
  - Learn MAC addresses
  - Forward frames only to the correct port
  - Support full-duplex communication
  - Handle Gigabit speeds (1000 Mbps) on every port simultaneously
  - Allow **multiple devices to communicate at the same time**

Typical correct setup:

```
Internet
   ↓
Router (LAN port 1) ────→ Switch port 1 (any port)
                            ├── Switch port 2 → Laptop
                            ├── Switch port 3 → Desktop / NAS
                            └── Switch port 4 → Smart TV / another device
```

As long as:

1. The cable from the router's LAN port to the switch is good
2. The switch is powered on (most Mercusys unmanaged switches need power)
3. You are using standard Ethernet cables (Cat5e or better for Gigabit)

Then **all devices plugged into the switch will get internet access** and will be able to communicate with each other on the local network — exactly the same way as if they were plugged directly into different LAN ports on the router.

You can use any of the 5 ports on the switch for the uplink to the router — there is no special "WAN" or "Uplink" port on these simple unmanaged switches. All ports are equal.

**Summary**
Your switch is a **real network switch**, not a splitter.
You can connect multiple devices (laptop + phone + TV + printer + etc.) and they will all have internet access and full Gigabit local network performance — unlike cheap splitters that only fake supporting one extra device and usually fail with modern equipment.

References:

- [Mercusys MS105G product page](https://www.mercusys.com/en/product/details/ms105g)
- [Mercusys SG105 product description](https://www.mercusys.com/en/product/details/sg105)
