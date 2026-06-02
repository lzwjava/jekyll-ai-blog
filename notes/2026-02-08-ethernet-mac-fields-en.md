---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: Ethernet MAC Address Field Sizes
translated: false
type: note
---

The question asks about the size of the address fields in an IEEE 802.3 MAC frame.

## Correct Answer: **C (48 bits)**

### Explanation

In IEEE 802.3 (Ethernet) MAC frame structure, both the **destination address (DA)** and **source address (SA)** are **48 bits long**, which equals **6 bytes**.

This 48-bit address is also known as a **MAC address** or **physical address**, and it's typically represented in hexadecimal notation with colons or hyphens, such as: `00:1A:2B:3C:4D:5E`

### Why 48 bits?

- **First 24 bits (3 bytes)**: Organizationally Unique Identifier (OUI) - identifies the manufacturer
- **Last 24 bits (3 bytes)**: Device-specific identifier assigned by the manufacturer

### Why Your Answer (B - 32 bits) Was Incorrect

32 bits would only be 4 bytes, which is insufficient to uniquely identify devices across different manufacturers and networks. The 48-bit address space is necessary to accommodate the large number of devices in modern networks while maintaining the hierarchical structure needed for efficient network administration.

The 48-bit MAC address has been the standard since Ethernet was first standardized and remains in use today.
