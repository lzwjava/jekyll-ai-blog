---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stop and Wait ARQ Basics Explained
translated: false
type: note
---

Question: What are the characteristics of the Stop-and-Wait ARQ error control mechanism?

Answer:

The correct answer is **A: Small buffer space required, low channel efficiency**.

### Detailed Explanation

**Stop-and-Wait ARQ (Automatic Repeat reQuest)** is the simplest form of error control protocol used in data link layers. Its operational characteristics are defined by the following logic:

1. **Window Size**: Both the sender's window and the receiver's window have a size of **1**. This means the sender can only transmit one frame at a time.
2. **Operation Flow**:
    * The sender transmits a single frame.
    * The sender must then **stop** and wait for an acknowledgment (ACK) from the receiver.
    * If the ACK is received correctly, the sender proceeds to transmit the next frame.
    * If a timeout occurs or a negative acknowledgment (NAK) is received, the sender retransmits the same frame.
3. **Buffer Space (Small)**: Since the system only handles one frame at a time (waiting for confirmation before sending the next), the required buffer storage space at both the sender and receiver ends is minimal.
4. **Channel Efficiency (Low)**: The major drawback of this method is inefficiency, especially on links with high bandwidth or long propagation delays. During the time the sender is waiting for the ACK, the communication channel remains idle and unused. This results in low throughput and poor utilization of the available channel capacity.

Therefore, the defining characteristics are that it requires **small buffer space** but suffers from **low channel efficiency**.

References:

* [Stop-and-Wait ARQ - GeeksforGeeks](https://www.geeksforgeeks.org/stop-and-wait-arq/)
* [Automatic Repeat Request - Wikipedia](https://en.wikipedia.org/wiki/Automatic_repeat_request)
