---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bridge Forwards Frames at Layer Two
translated: false
type: note
---

Question: In the OSI seven-layer reference model, a bridge operates at the data link layer, and the forwarding function it implements is:

A. Bit forwarding
B. Frame forwarding
C. Packet forwarding
D. Message forwarding

Answer:

**B. Frame forwarding**

**Explanation:**

A **bridge** (网桥) is a network device that operates at **Layer 2** (the **Data Link Layer**) of the OSI model.

At the data link layer, the protocol data unit (PDU) is called a **frame** (帧).

Therefore, a bridge makes forwarding decisions based on the MAC addresses contained in the frame header and forwards entire **frames** from one segment to another.

- **Bit forwarding** (A): This is not a standard term and does not correspond to any real layer's forwarding behavior.
- **Packet forwarding** (C): This is performed by routers, which operate at **Layer 3** (Network Layer), where the PDU is a **packet** (containing IP headers).
- **Message forwarding** (D): "Message" is a more general/application-layer term and is not used in the context of data link layer forwarding.

Correct answer: **B. Frame forwarding** (帧转发)

The bridge reads the destination MAC address in the frame, looks it up in its MAC address table (also called the forwarding table or CAM table), and decides which port to forward the frame out of — this is classic **frame forwarding**.

References:

- None (standard networking knowledge from OSI model and IEEE 802.1D bridging specification)
