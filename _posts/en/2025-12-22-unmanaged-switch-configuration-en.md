---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unmanaged Switch Lacks Configuration Interface
translated: false
type: note
---

Question: My Mercury 5-port 1000Mbps switch (model 5G105C, dark color, 5V 0.4A) does not act like a router and has no IP address for configuration. Is it not accessible via 192.168.2.1 or similar addresses?

Answer:

Your device is a **Mercury** (or likely rebranded **Mercusys**) 5-port Gigabit Ethernet switch, with a model similar to SG105C, SG105M, or MS105G. These are **unmanaged desktop switches** designed for simple plug-and-play operation.

### Key Characteristics
- **Unmanaged switch**: It has no web interface, no configuration page, and no assignable IP address. Unlike a router (which typically uses addresses like 192.168.1.1, 192.168.0.1, or 192.168.2.1 for setup), an unmanaged switch operates at Layer 2 of the network. It simply forwards Ethernet frames between connected devices without any management features.
- **No IP address**: The device itself does not obtain or use an IP address for access. You cannot log in to it via a browser or configure settings like VLANs, port mirroring, or QoS.
- **Power specs match**: Many similar models (e.g., Mercusys MS105G) use a 5V power adapter (often around 0.6A, but 0.4A is close and common in variants).
- **Behavior is normal**: It "doesn't act like a router" because it is not a router—it's just a basic switch to expand your network ports and connect multiple devices (e.g., computers, TVs, printers) at Gigabit speeds.

### What You Can Do
- Connect your main router to one port on the switch.
- Plug other devices into the remaining ports.
- Everything should work immediately—no setup required.

If you need advanced features (e.g., a web config page), you would require a **managed switch** instead.

References:

- https://skit.com.sg/products/mercury-sg105c-5-port-gigabit-ethernet-network-desktop-switch (Mercury SG105C described as plug-and-play hub)
- https://www.mercusys.com/en/product/details/ms105g/ (Mercusys MS105G: 5-port Gigabit unmanaged desktop switch, plug-and-play, no configuration)
- https://www.newegg.com/luom-sg105m-5-x-rj45/p/0XP-018B-00003 (Similar Mercury SG105M listed as unmanaged, plug-and-play)
