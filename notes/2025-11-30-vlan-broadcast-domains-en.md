---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: VLANs Segment Broadcast Domains
translated: false
type: note
---

**Answer for Question 1: B) Segment Layer 2 broadcast domains**

**Explanation:**
The primary purpose of VLANs (Virtual Local Area Networks) in a switched network is to logically separate a single physical switch into multiple independent broadcast domains at Layer 2.

- Without VLANs, all ports on a switch belong to the same broadcast domain (broadcasts from one device reach every other device on the same switch/Layer 2 network).
- By creating VLANs, you confine Layer 2 broadcast traffic (ARP requests, etc.) to only the ports that belong to that specific VLAN, reducing unnecessary traffic, improving performance, and enhancing security.

Why the other options are incorrect:
- **A) Increase broadcast domain size** → Wrong. VLANs actually decrease the effective size of each broadcast domain.
- **C) Replace the need for routers** → Wrong. VLANs are Layer 2 constructs. Communication between different VLANs still requires a Layer 3 device (router or Layer 3 switch) for inter-VLAN routing.
- **D) Provide Layer 3 encryption** → Wrong. VLANs have nothing to do with encryption (that’s handled by protocols like IPsec, SSL/TLS, etc.).

So the correct and main purpose is **B**.

Let me know if you have Question 2 ready!
