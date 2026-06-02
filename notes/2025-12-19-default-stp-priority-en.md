---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Default STP Bridge Priority
translated: false
type: note
---

Question: What is the default priority value for a switch in Spanning Tree Protocol (STP)?

Answer:

The correct answer is **B) 32768**.

In the original Spanning Tree Protocol (IEEE 802.1D), the default bridge priority value for a switch is 32768. The bridge priority is a 16-bit field in the Bridge ID (BID), which consists of the priority (higher 16 bits, in multiples of 4096) and the MAC address (lower 48 bits).

By default, the priority is set to 32768 (which is 0x8000 in hexadecimal), making the full extended priority portion align with this value when no modifications are made. This default allows for manual configuration in increments of 4096 (from 0 to 61440) to influence root bridge election, where lower BID wins.

Options A (0), C (61440), and D (65535) are incorrect:
- 0 is a valid configurable priority but not the default.
- 61440 is the highest configurable priority (least likely to become root).
- 65535 is not a valid priority value in standard STP (max is 61440 for the priority field).

This default has remained consistent across STP variants like RSTP and PVST unless explicitly changed.
