---
audio: false
generated: true
image: false
lang: en
layout: post
title: Half-Duplex Design of BSC Adapter
translated: false
type: note
---

Question: How should we understand that the IBM PC BSC Communication Adapter was primarily designed for half-duplex transmission lines?

Answer:

The IBM PC **BSC (Binary Synchronous Communication)** adapter was built around the operational model of half-duplex communication, which means data can flow in **both directions, but only one direction at a time** — not simultaneously.

Here's how to understand this design choice:

**What is BSC?**
BSC (also called Bisync) is a character-oriented synchronous data link protocol developed by IBM in the 1960s. It was widely used for mainframe and terminal communications before async serial took over.

**Why half-duplex fits BSC naturally**

BSC is a **stop-and-wait** protocol by design:

- The sender transmits a block of data
- Then *stops* and waits for an ACK (acknowledgment) or NAK (negative acknowledgment) from the receiver
- Only after receiving the reply does it send the next block

This inherently alternating send/receive pattern maps perfectly onto a half-duplex line — full-duplex capability would be wasted, since both sides never need to transmit at the exact same moment.

**Practical implications for the adapter**

- The adapter controls the **RTS/CTS (Request To Send / Clear To Send)** handshake to flip the line direction
- It handles **modem turnaround time** — the delay needed when switching the line from transmit to receive mode
- It was optimized for **leased telephone lines** and **2-wire circuits**, which are inherently half-duplex

**In summary**

| Concept | Detail |
| --- | --- |
| Protocol | IBM Binary Synchronous (Bisync) |
| Direction | One way at a time |
| Flow | Send block → wait for ACK → send next block |
| Line type | Typically 2-wire leased or switched telephone lines |
| Why not full-duplex? | BSC's ACK/NAK cycle doesn't require simultaneous two-way transmission |

The design is not a limitation so much as a deliberate fit — the protocol's logic and the physical line infrastructure of that era both pointed to half-duplex as the practical and sufficient choice.

References:

- [IBM Binary Synchronous Communications - Wikipedia](https://en.wikipedia.org/wiki/Binary_Synchronous_Communications)
- [IBM PC Hardware Reference Library - BSC Adapter](https://www.pcjs.org/documents/manuals/ibm/)
- [Half-duplex vs Full-duplex Explained](https://en.wikipedia.org/wiki/Duplex_(telecommunications))
