---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two Key Advantages of Stop-and-Wait ARQ
translated: false
type: note
---

Question: What are the advantages of Stop-and-Wait ARQ, and why is "simple" considered one of them?

Answer: Stop-and-Wait ARQ is considered **simple** because of the following reasons:

1. **Minimal logic**: The sender transmits one frame and then waits for an ACK (acknowledgment) before sending the next. This straightforward one-at-a-time mechanism requires very little control logic.

2. **No sequencing complexity**: Since only one frame is in transit at any time, you only need a 1-bit sequence number (0 or 1) to distinguish the current frame from a retransmission.

3. **Trivial error handling**: If no ACK is received within a timeout, the sender simply retransmits the same frame — no need to track a window or buffer multiple frames.

4. **Small buffer requirement**: Both sender and receiver only need to buffer a single frame at a time, keeping memory management straightforward.

In summary, the two main advantages are:
- ✅ **Simple** (implementation and logic are minimal)
- ✅ **Small buffer space required** (only 1 frame buffered at a time)

The main disadvantage is **low channel efficiency**, because the sender sits idle waiting for each ACK, wasting bandwidth — especially on high-latency links.

References:
- [Stop-and-Wait ARQ – Wikipedia](https://en.wikipedia.org/wiki/Stop-and-wait_ARQ)
- [ARQ Protocols – GeeksforGeeks](https://www.geeksforgeeks.org/stop-and-wait-arq/)
