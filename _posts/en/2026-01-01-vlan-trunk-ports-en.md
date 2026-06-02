---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding VLAN Trunk Ports
translated: false
type: note
---

Question: Which type of switch port allows multiple VLANs to pass through?
A) Access port
B) Trunk port
C) Hybrid port
D) Console port

Answer:

The correct answer is **B) Trunk port**.

- **Access port**: Configured to belong to a single VLAN only. It carries traffic for one VLAN and is typically used to connect end devices like computers or printers. Untagged frames are sent and received.
- **Trunk port**: Designed to carry traffic for multiple VLANs simultaneously. It uses tagging (usually 802.1Q) to identify which VLAN each frame belongs to, allowing VLANs to extend across switches.
- **Hybrid port**: A proprietary mode found on some switches (e.g., Huawei) that can handle both tagged and untagged traffic for multiple VLANs, but it is not the standard term for this function across vendors.
- **Console port**: A management port used for out-of-band configuration via a serial connection; it does not carry network traffic or VLANs.

In standard networking (e.g., Cisco), the port type that allows multiple VLANs to pass through is the **trunk port**.
