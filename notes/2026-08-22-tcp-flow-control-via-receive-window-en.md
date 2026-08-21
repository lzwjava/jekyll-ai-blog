---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Flow Control via Receive Window
translated: false
type: note
---

**Question:** Briefly describe the basic working mechanism of TCP's Flow Control.

**Answer:**

**Purpose**
Flow control ensures the sender does not transmit data faster than the receiver can process it, preventing the receiver's buffer from overflowing.

**Mechanism — Receive Window (rwnd)**

1. **Receiver advertises buffer space** — With every ACK (or pure acknowledgment) sent back to the sender, the receiver includes a *receive window* (`rwnd`) field indicating how many bytes of free buffer space remain.

2. **Sender respects the window** — The sender ensures that the total amount of unacknowledged (in-flight) application data never exceeds the most recently advertised `rwnd` value:

$$\text{LastByteSent} - \text{LastByteAcked} \leq rwnd$$

3. **Dynamic adjustment** — As the receiver consumes buffered data (passes it to the application), its free buffer grows, and it advertises a larger `rwnd` in subsequent ACKs, allowing the sender to speed up again.

4. **Zero-window probe** — If `rwnd = 0`, the sender stops transmitting but periodically sends a 1-byte probe segment to check whether buffer space has been freed.

**Summary Flow**

```
Sender                         Receiver
  |------- Data Segment -------->|  (consumes buffer)
  |<--- ACK + rwnd = 2048 -------|  (2 KB free)
  |------- up to 2048 bytes ---->|
  |<--- ACK + rwnd = 0 ----------|  (buffer full)
  |--- zero-window probe ------->|  (polling)
  |<--- ACK + rwnd = 1024 -------|  (app read some data)
  |------- resumes sending ------>|
```

This mechanism decouples the sender's speed from the receiver's processing capacity, guaranteeing no buffer overflow at the receiver side.
