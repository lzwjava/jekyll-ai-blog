---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLC and MAC Sublayer Split
translated: false
type: note
---

**Question:** How is the Data Link Layer divided into the LLC and MAC sublayers?

**Answer:**

The IEEE decided to split Layer 2 (Data Link) into two sublayers so that hardware-specific concerns could be separated from protocol-multiplexing concerns.

**LLC — Logical Link Control (upper sublayer, IEEE 802.2)**

LLC sits right below Layer 3 and provides a uniform interface to the network layer regardless of what physical medium is being used underneath. Its main jobs are:

- **Protocol multiplexing** — uses Service Access Points (SAPs) to let multiple Layer-3 protocols (IPv4, IPv6, IPX, etc.) share the same link.
- **Framing** — adds headers/trailers to delimit packets into frames.
- **Error detection & optional flow control** — depending on the mode (connectionless vs. connection-oriented), it can detect lost or corrupted frames.

**MAC — Media Access Control (lower sublayer, IEEE 802.x)**

MAC is the sublayer that faces the physical hardware. Its responsibilities are:

- **Addressing** — the 48-bit MAC (hardware) address lives here; it identifies a specific NIC on a local network segment.
- **Medium access** — determines who gets to transmit when multiple devices share the same channel (e.g., CSMA/CD for Ethernet 802.3, CSMA/CA for Wi-Fi 802.11).
- **Frame delimiting at the hardware level** — adds preamble bits, start-of-frame delimiters, and FCS (CRC checksum).

**Why the split matters**

The LLC/MAC boundary lets the same LLC logic (IEEE 802.2) sit on top of completely different physical media — Ethernet, Wi-Fi, Token Ring, etc. — without change. Each medium gets its own MAC standard (802.3, 802.11, 802.5…), while the LLC above them all stays constant. You can click any box in the diagram for more detail.

**References:**
- [IEEE 802.2 LLC standard overview – Wikipedia](https://en.wikipedia.org/wiki/Logical_link_control)
- [IEEE 802 LAN/MAN standards overview – Wikipedia](https://en.wikipedia.org/wiki/IEEE_802)
- [MAC sublayer – Wikipedia](https://en.wikipedia.org/wiki/Medium_access_control)