---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP's Three Core Problems
translated: false
type: note
---

**Question:** How does TCP connection work, and what are the three core problems that need to be solved?

**Answer:** TCP (Transmission Control Protocol) is a connection-oriented protocol that guarantees reliable, ordered, and error-checked delivery of data between two endpoints. Before any data flows, TCP must solve three fundamental problems:

**1. Reliability** — The network can lose, corrupt, or drop packets. TCP solves this with **acknowledgments (ACKs)** and **retransmission**. Every segment sent must be acknowledged by the receiver; if no ACK arrives within a timeout, the sender retransmits.

**2. Ordering** — Packets may arrive out of order (taking different network paths). TCP assigns a **sequence number** to every byte of data, so the receiver can reassemble them in the correct order even if they arrive scrambled.

**3. Flow Control / Congestion Control** — The sender must not overwhelm the receiver's buffer or flood the network. TCP uses a **window size** (advertised by the receiver) to cap how much unacknowledged data can be in-flight at once, and **congestion control algorithms** (slow start, AIMD) to back off when the network is stressed.

These three problems are addressed through the famous **three-way handshake** to establish a connection, then the ongoing segment exchange:Here's a summary of the three problems mapped to the handshake:

**① Reliability** → Solved by SYN/ACK exchange + retransmission timers. The handshake ensures both sides agree to communicate and can detect lost packets.

**② Ordering** → Solved by sequence numbers. Each byte gets a number; the receiver buffers out-of-order segments and delivers them in the right order.

**③ Flow & Congestion Control** → Solved by the `win=` (window size) field in every ACK. The receiver advertises how much buffer space it has, and TCP's congestion control (slow start → congestion avoidance) prevents overloading the network itself.

The three-way handshake (SYN → SYN-ACK → ACK) is essentially both sides exchanging their initial sequence numbers and confirming they can receive — all three problems are baked into this design from the start.