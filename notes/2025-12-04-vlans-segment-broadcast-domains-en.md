---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: VLANs Segment Layer 2 Broadcast Domains
translated: false
type: note
---

Question: What is the main purpose of VLANs in a switched network?

Answer:
The primary purpose of VLANs (Virtual Local Area Networks) is to **segment Layer 2 broadcast domains**.

In a standard switched network without VLANs, all devices connected to the same switch (or interconnected switches) belong to a single broadcast domain—every broadcast frame is flooded to all ports. By creating multiple VLANs on a switch, you logically divide it into separate broadcast domains. Broadcast traffic from one VLAN stays confined to that VLAN and does not reach devices in other VLANs, even though they may share the same physical infrastructure. This improves security, reduces unnecessary traffic, and allows better network organization.

- **A) Increase broadcast domain size** → Incorrect. VLANs actually decrease the effective size of each broadcast domain by splitting it.
- **B) Segment Layer 2 broadcast domains** → Correct.
- **C) Replace the need for routers** → Incorrect. Inter-VLAN communication still requires a Layer 3 device (router or Layer 3 switch).
- **D) Provide Layer 3 encryption** → Incorrect. VLANs operate at Layer 2 and do not provide encryption.

Thus, the correct answer is **B**.
