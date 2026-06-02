---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Maximum MAC Addresses Limit Ports
translated: false
type: note
---

Question: Which port security feature limits the number of MAC addresses on a port?

Answer:

The correct answer is **C) Maximum MAC addresses**.

In Cisco switch port security, the feature that directly limits the number of MAC addresses allowed on a port is configured using the command `switchport port-security maximum <number>`. This sets the maximum number of secure MAC addresses (either dynamically learned or statically configured) that the port can accommodate.

- **A) Sticky MAC**: This refers to the `switchport port-security mac-address sticky` feature, which dynamically learns MAC addresses and converts them to sticky (persistent) entries in the running configuration. It does not limit the number of addresses.
- **B) Violation Restrict**: This is a violation mode (`switchport port-security violation restrict`) that increments violation counters and drops traffic from unauthorized MACs when the maximum is exceeded, but it is not the feature that sets the limit itself.
- **D) Portfast**: This is a Spanning Tree Protocol (STP) feature that bypasses listening and learning states on access ports, enabling immediate transition to forwarding. It has no relation to MAC address limiting.

The "maximum MAC addresses" setting is the core mechanism for restricting the quantity of source MAC addresses permitted on a secured port.
