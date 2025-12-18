---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Switch Flooding for Unknown MAC Addresses
translated: false
type: note
---

Question: In Ethernet switching, what happens when a switch receives a frame with a destination MAC address that is not in its MAC address table?

Answer: 

When an Ethernet switch receives a frame with a destination MAC address that is **unknown** (not present in its MAC address table), it performs **flooding**. The switch forwards the frame out **all ports except the incoming port** on which the frame was received. This ensures the frame reaches the intended destination if it is connected to the switch, while allowing the switch to learn the destination's port when a reply comes back.

This behavior is fundamental to how Layer 2 switches operate in **unknown unicast** situations.

- **Option A** is incorrect: The switch does not drop the frame; dropping would break connectivity for unknown destinations.
- **Option B** is correct: Flooding out all ports except the incoming one.
- **Option C** is incorrect: Sending to the default gateway is a Layer 3 (router) function, not a Layer 2 switch.
- **Option D** is incorrect: Buffering indefinitely is not standard behavior; the switch forwards the frame immediately.

The correct answer is **B**.

References:  

- [Cisco - Understanding and Configuring the Switch CAM Table](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/12013-17.html)
- [IEEE 802.1D - Media Access Control (MAC) Bridges](https://standards.ieee.org/ieee/802.1D/5001/)