---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: BGP Established State Explanation
translated: false
type: note
---

Question: Which BGP neighbor state indicates that a TCP three-way handshake has been completed?
A) Idle
B) Connect
C) Active
D) Established

Answer:

**D) Established**

The **Established** state in the BGP finite state machine is reached only after the TCP three-way handshake is successfully completed and the BGP peers have exchanged valid Open messages, followed by Keepalive messages. This is the only state in which the BGP session is fully operational and routing information (Update messages) can be exchanged.

For reference, the relevant BGP neighbor states related to TCP connection setup are:

- **Idle**: Initial state, no connection attempt yet.
- **Connect**: Waiting for the TCP three-way handshake to complete.
- **Active**: TCP handshake failed or timed out; actively retrying to establish TCP.
- **Established**: TCP connection is up, BGP Open messages exchanged successfully → peering is fully up.

So, the correct answer is **D) Established**.
