---
audio: false
generated: true
image: false
lang: en
layout: post
title: LAN Broadcast Transmission Basics
translated: false
type: note
---

Question: What is the general transmission method used in local area networks (LANs)?

Answer:

The correct answer is **广播** (broadcast).

**Explanation:**

In traditional LANs (especially those using Ethernet with hubs or in early bus topologies), the most common and fundamental transmission method at the data link layer is **broadcast**.

Main characteristics:
- When a device sends a data frame, the frame is transmitted to **all devices** on the same local network segment.
- All devices on the LAN receive the frame.
- Only the device whose MAC address matches the destination address in the frame will process it, while other devices discard it.

This is why LANs are often described as using **broadcast transmission** (or one-to-all transmission within the broadcast domain).

Common related concepts:
- **Unicast**（单播）：one-to-one (most common for actual data transfer after knowing the target MAC)
- **Broadcast**（广播）：one-to-all (used for ARP, DHCP, discovery protocols, etc.)
- **Multicast**（组播）：one-to-many (specific group)

But when textbooks or exam questions ask about the **general / typical transmission method** of a local area network, especially in the context of classic Ethernet LANs, the standard answer is **广播方式** (broadcast mode).

Even though modern switched Ethernet has greatly reduced unnecessary broadcast traffic through MAC address learning and forwarding, the essential nature of the LAN broadcast domain remains, and the classic/typical description still uses "broadcast".

So the reference answer **广播** is correct.

References:
None
