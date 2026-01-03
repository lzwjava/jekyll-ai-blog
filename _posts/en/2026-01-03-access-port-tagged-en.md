---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Access Port Handling of Tagged Frames
translated: false
type: note
---

Question: How does an access port handle VLAN-tagged frames?

Answer: 

An **access port** on a switch is designed to connect to end devices (e.g., PCs, printers, IP phones) and belongs to a single VLAN (configured as the access VLAN). It operates in **untagged** mode for that VLAN.

When an access port receives a frame:

- If the frame is **untagged**, the switch adds the configured access VLAN tag internally and forwards it to the appropriate VLAN.
- If the frame is **VLAN-tagged** (i.e., it already has an 802.1Q tag), the default and standard behavior on most switches (including Cisco) is to **drop the tagged frame**. This is because access ports expect traffic from end devices that do not tag frames themselves, and receiving a tagged frame typically indicates a misconfiguration or potential security issue.

Therefore, the correct answer is **D) It drops all tagged frames**.

Options A, B, and C are incorrect for access ports:
- A) Forwarding unchanged would imply treating it as a trunk port.
- B) Adding a tag is done only for untagged ingress frames.
- C) Removing the tag (stripping) occurs on **egress** when sending frames out an access port to an untagged device, not on ingress.

This behavior is defined in IEEE 802.1Q and implemented consistently by major vendors like Cisco, Juniper, and Arista.