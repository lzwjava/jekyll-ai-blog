---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ethernet Expansion Device Layer Classification
translated: false
type: note
---

Question: Is the answer to this Ethernet expansion question correct — that physical layer expansion uses Repeaters and Hubs, while data link layer expansion uses Bridges and Switches?

Answer: Yes, that is correct.

The classification is:

**Physical Layer (Layer 1):** Repeater and **Hub** — these devices simply regenerate or broadcast signals without any awareness of MAC addresses or frames.

**Data Link Layer (Layer 2):** Bridge and **Switch** — these devices make forwarding decisions based on MAC addresses, operating at the frame level.

So the answer **A (Hub)** is right. Hubs, like repeaters, operate purely at the physical layer — they amplify and retransmit signals to all ports with no intelligence about the data being carried.

References:

- [Ethernet Hub - Wikipedia](https://en.wikipedia.org/wiki/Ethernet_hub)
- [Network Repeater - Wikipedia](https://en.wikipedia.org/wiki/Repeater)
