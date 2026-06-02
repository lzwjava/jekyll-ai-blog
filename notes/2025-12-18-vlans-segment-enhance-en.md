---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: VLANs Segment Networks and Enhance Security
translated: false
type: note
---

Question: What is the purpose of VLANs in a switched network?

Answer:

Virtual LANs (VLANs) are used in switched networks to logically segment a physical network into multiple separate broadcast domains without requiring additional physical hardware.

The primary purposes are:

- **Reducing broadcast domains**: In a flat Layer 2 switched network, broadcasts (e.g., ARP requests) flood to all devices, consuming bandwidth and potentially causing performance issues in large networks. VLANs confine broadcasts to only the devices within the same VLAN.
- **Improving security**: By placing devices into different VLANs, traffic is isolated at Layer 2—devices in one VLAN cannot directly communicate with devices in another VLAN without a Layer 3 device (router or Layer 3 switch) enforcing access controls. This limits the scope of attacks and sensitive data exposure.
- **Better network organization**: VLANs allow grouping of devices by function, department, or policy rather than physical location.

Evaluating the options:

- **A) To increase broadcast domains** → Incorrect. VLANs decrease the size of each broadcast domain (or create more smaller ones instead of one large one).
- **B) To segment broadcast domains and improve security** → Correct. This accurately describes the core benefits.
- **C) To route traffic between switches** → Incorrect. Routing (Layer 3) between VLANs requires inter-VLAN routing; VLANs themselves operate at Layer 2 and do not route.
- **D) To assign IP addresses dynamically** → Incorrect. Dynamic IP assignment is handled by DHCP, not VLANs.

The correct answer is **B**.
