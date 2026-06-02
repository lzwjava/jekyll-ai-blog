---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Network Layer Handles Logical Addressing
translated: false
type: note
---

Question: Which layer of the OSI model is responsible for logical addressing and routing?

Answer:

The correct answer is **C) Network Layer**.

### Explanation

The OSI (Open Systems Interconnection) model consists of seven layers, each with specific responsibilities:

- **Physical Layer (Layer 1)**: Handles the transmission of raw bits over a physical medium (e.g., cables, signals).
- **Data Link Layer (Layer 2)**: Provides node-to-node data transfer, error detection, and physical (MAC) addressing.
- **Network Layer (Layer 3)**: Responsible for **logical addressing** (e.g., IP addresses) and **routing** (determining the best path for data packets across networks). Key protocols include IP, ICMP, and routing protocols like OSPF or BGP.
- **Transport Layer (Layer 4)**: Ensures end-to-end reliable data delivery, segmentation, and flow control (e.g., TCP, UDP).

Logical addressing (such as IPv4/IPv6 addresses) and routing functions are exclusively handled at the Network Layer, making option C the correct choice. Option B is incorrect because the Data Link Layer uses physical (MAC) addresses, not logical ones, and does not perform routing across networks.
