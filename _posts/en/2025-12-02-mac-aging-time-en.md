---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: MAC Aging Time Controls Dynamic Entry Removal
translated: false
type: note
---

Question: In a switch MAC address table, what does the term “aging time” refer to?

Answer: The correct answer is **B) Time before a dynamic MAC entry is removed**.

**Explanation**:
The MAC address table (also called CAM table) on a switch contains dynamic entries learned through incoming frames. The **aging time** (or MAC aging timer) is the period of inactivity (no frames received from that MAC address on that port) after which the switch removes the dynamic entry from the table to keep it current and prevent stale entries. Typical default values are 300 seconds (5 minutes), but this is configurable.

- **A)** Incorrect – That relates to STP port states (learning/forwarding timers).
- **C)** Incorrect – VLANs do not have an aging concept tied to the MAC table.
- **D)** Incorrect – ARP cache aging is a Layer-3 feature, unrelated to the switch’s Layer-2 MAC table.

So, **aging time** specifically controls how long a dynamically learned MAC address remains in the table before being flushed if the device stops sending traffic.
