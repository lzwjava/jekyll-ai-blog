---
audio: false
generated: true
image: false
lang: en
layout: post
title: Go Back N Window Sizes Explained
translated: false
type: note
---

Question: In the Go-Back-N sliding window protocol, what are the sizes of the sending window and receiving window?

Answer:

## Go-Back-N (GBN) Protocol — Window Sizes

The correct answer is **B: Sending Window > 1, Receiving Window = 1**

---

## Explanation of All Three Sliding Window Protocols

| Protocol | Sending Window | Receiving Window |
|---|---|---|
| Stop-and-Wait | = 1 | = 1 |
| **Go-Back-N (GBN)** | **> 1** | **= 1** |
| Selective Repeat (SR) | > 1 | > 1 |

---

## Why Go-Back-N Has Receiving Window = 1?

**Go-Back-N** allows the sender to transmit multiple frames without waiting for acknowledgment (sending window > 1), but the **receiver only accepts frames in strict sequential order**.

- If a frame is received **out of order**, the receiver **discards it** and does not buffer it.
- Because the receiver only needs to track the **next expected frame** (no buffering of out-of-order frames), the receiving window size is **1**.
- When an error occurs at frame *n*, the sender must **go back and retransmit frame n and all subsequent frames** — hence the name "Go-Back-N."

## Why NOT Option C (both > 1)?

Option C describes the **Selective Repeat (SR)** protocol, not Go-Back-N. In SR:

- The receiver **buffers out-of-order frames**, so receiving window > 1.
- Only the specific erroneous frame needs to be retransmitted (not all subsequent ones).

## Summary

Go-Back-N trades off **receiver buffer simplicity** (window = 1, no buffering needed) against **retransmission efficiency** (must resend multiple frames on error). This is the key distinction from Selective Repeat.
