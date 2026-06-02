---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ethernet Broadcast MAC Address
translated: false
type: note
---

The correct answer is **B) FFFF.FFFF.FFFF**

### Explanation:
In an Ethernet network, a **broadcast frame** is sent to all devices on the same local network segment (Layer 2 broadcast).

- The destination MAC address for an Ethernet broadcast frame is **all ones** in hexadecimal: **FF-FF-FF-FF-FF-FF** (often written as **FFFF.FFFF.FFFF**).
- This is the reserved broadcast MAC address defined in the Ethernet standard.

### Why the others are wrong:
- **A) 0000.0000.0000** → This is an invalid or null MAC address (sometimes used as source in special cases, but never for broadcast).
- **C) 0100.5E00.0000** → This is the base for IPv4 multicast MAC addresses (not broadcast).
- **D) The MAC of the default gateway** → This would be a unicast frame, not broadcast.

**Correct Answer: B) FFFF.FFFF.FFFF**
