---
audio: false
generated: true
image: false
lang: en
layout: post
model: moonshotai/kimi-k2-thinking
title: QUIC Solves Head-of-Line Blocking
translated: false
type: note
---

Here’s an introduction to that dialogue, providing context and explaining the technical concepts:

---

### The Problem: Head-of-Line Blocking in Real-Time Communication

**Person A** is referring to a fundamental limitation of **TCP (Transmission Control Protocol)**. While TCP is reliable—it ensures packets arrive in order and retransmits lost ones—this very reliability creates a problem: **head-of-line (HOL) blocking**.

Imagine sending a file with 10 packets. If packet 3 gets lost, TCP holds *everything* after it (packets 4-10) until packet 3 is retransmitted and arrives. In real-time applications like video calls or online gaming, this creates noticeable lag or stuttering: newer data waits for old data, even if it's no longer useful.

Traditional workarounds involve using **UDP (User Datagram Protocol)**, which is fast and unordered but lacks reliability features like retransmission and congestion control—so developers had to rebuild these from scratch.

---

### The Solution: QUIC Protocol

**Person B** introduces **QUIC (Quick UDP Internet Connections)**, a modern protocol developed by Google in 2012 and now standardized as **RFC 9000**:

- **Runs on top of UDP**: QUIC leverages UDP’s speed as a foundation while adding built-in reliability, encryption, and congestion control at the application level.
- **Avoids Head-of-Line Blocking**: QUIC introduces **multiplexed streams**—independent data channels within a single connection. If one stream’s packet is lost, only *that* stream pauses; other streams continue flowing. This is crucial for web pages loading many resources simultaneously or video calls where audio and video are separate streams.
- **TCP-like Features**: It provides reliability, flow control, and congestion management, but more efficiently and with faster connection establishment (often 0-RTT handshake).

QUIC is the foundation of **HTTP/3**, now used by major platforms like YouTube, Facebook, and Cloudflare to improve performance and user experience.

---
