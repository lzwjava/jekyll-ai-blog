---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Handshake Problems and Process Explained
translated: false
type: note
---

Question: What are the three main problems that need to be solved during the establishment of a TCP connection, and describe the three-way handshake process between A and B (including the flag settings and sequence/acknowledgment numbers in each step)?

Answer:

The TCP three-way handshake is designed to solve the following three key problems:

1. **Make sure both communicating parties are aware of each other's existence** (mutual confirmation that the other side is reachable and active).
2. **Allow both sides to negotiate relevant parameters** during the connection (such as maximum segment size, window size, options, etc.).
3. **Allocate necessary resources** for the transport entities on both sides (e.g., buffers, control blocks, etc.).

The detailed three-way handshake process between host A (client) and host B (server) is as follows:

**Step 1 – SYN (Connection Request)**
- A → B: Connection request segment
- Flags: **SYN = 1**, **ACK = 0**
- Sequence number: **seq = x** (A's initial sequence number)
- Meaning: A tells B: "I want to establish a connection; my starting sequence number is x."

**Step 2 – SYN-ACK (Acknowledgment + Connection Request)**
- B → A: Acknowledgment and connection request segment
- Flags: **SYN = 1**, **ACK = 1**
- Acknowledgment number: **ack = x + 1** (confirms receipt of A's SYN)
- Sequence number: **seq = y** (B's own initial sequence number)
- Meaning: B tells A: "I received your request (ack = x+1), I agree to connect, and my starting sequence number is y."

**Step 3 – ACK (Final Acknowledgment)**
- A → B: Confirmation segment
- Flags: **SYN = 0**, **ACK = 1**
- Sequence number: **seq = x + 1** (next byte A will send)
- Acknowledgment number: **ack = y + 1** (confirms receipt of B's SYN)
- Meaning: A tells B: "I received your SYN-ACK and agree; the connection is now fully established."

After these three steps, both sides have synchronized their sequence numbers and confirmed each other's existence, and the TCP connection is successfully established. Data transfer can begin from this point.

This three-way (not two-way) handshake is necessary to avoid the "old duplicate connection request" problem in networks with delayed or duplicated packets.

References:
- None (standard TCP protocol description from RFC 793 and computer networking textbooks)
