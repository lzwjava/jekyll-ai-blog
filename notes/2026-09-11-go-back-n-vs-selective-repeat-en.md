---
audio: false
generated: true
image: false
lang: en
layout: post
title: Go-Back-N vs Selective Repeat
translated: false
type: note
---

Question: Explain **Go-Back-N ARQ** and **Selective Repeat ARQ**.

Answer:

Both are **ARQ (Automatic Repeat reQuest)** protocols. The basic idea is:

> Sender sends packets → receiver detects loss/error → receiver asks for retransmission.

The key difference is **what gets retransmitted when one packet is lost**.

### 1. Go-Back-N ARQ（回退 N 步）

Suppose the sender sends:

```text
Sender:   [1] [2] [3] [4] [5] [6]
                    X
                  lost
```

Packet **3** is lost.

The receiver gets:

```text
1 ✓
2 ✓
3 ✗
4 ✓   ← received, but discarded because 3 is missing
5 ✓   ← discarded
6 ✓   ← discarded
```

The receiver essentially says:

```text
ACK 2
```

meaning:

> "I have everything up to packet 2. Send packet 3 onward again."

So the sender **goes back to 3**:

```text
             retransmit
                  ↓
Sender:   [3] [4] [5] [6]
```

That's why it's called **Go-Back-N**.

#### Example

```text
Send:       1  2  3  4  5
                X

Receive:    1  2     4  5
            ✓  ✓     ✗  ✗

Retransmit:       3  4  5
```

The good packets 4 and 5 are retransmitted even though they were successfully received.

**Advantage:** simple receiver implementation.

**Disadvantage:** wastes bandwidth when packet loss is high.

---

### 2. Selective Repeat ARQ（选择重传）

Same situation:

```text
Sender:   [1] [2] [3] [4] [5]
                    X
```

Receiver receives:

```text
1 ✓
2 ✓
3 ✗
4 ✓
5 ✓
```

Unlike Go-Back-N, the receiver **buffers 4 and 5**.

It tells the sender:

```text
ACK 1
ACK 2
ACK 4
ACK 5
```

or equivalently indicates:

```text
3 needs retransmission
```

Then sender only retransmits:

```text
[3]
```

After receiving 3:

```text
1 2 3 4 5
✓ ✓ ✓ ✓ ✓
```

So:

> **Selective Repeat retransmits only the packets that were actually lost/damaged.**

---

### The core difference

|                                        | Go-Back-N           | Selective Repeat  |
| -------------------------------------- | ------------------- | ----------------- |
| Packet 3 lost                          | Retransmit 3,4,5... | Retransmit only 3 |
| Receiver buffers out-of-order packets? | Usually no          | Yes               |
| Implementation                         | Simpler             | More complicated  |
| Bandwidth efficiency                   | Worse               | Better            |
| High packet-loss network               | Less efficient      | More efficient    |
| Receiver memory                        | Lower               | Higher            |

### Think of it like TCP

Imagine you're downloading:

```text
1 2 3 4 5 6 7 8
```

Packet 3 disappears.

**Go-Back-N:**

```text
1 2 [3 4 5 6 7 8]
      ↑
    resend all
```

**Selective Repeat:**

```text
1 2 [3] 4 5 6 7 8
      ↑
    resend only 3
```

The fundamental tradeoff is:

```text
Go-Back-N
    ↓
simpler receiver
    ↓
more retransmission

Selective Repeat
    ↓
more receiver state/buffering
    ↓
less retransmission
```

One subtle point: **modern TCP is not literally pure Go-Back-N or pure Selective Repeat**. TCP's cumulative ACK behavior resembles Go-Back-N, while **SACK (Selective Acknowledgment)** gives it selective-repeat-like retransmission behavior.

I can also walk through **sliding-window ARQ with sequence numbers and ACK/timeout timing**, which makes GBN vs SR much easier to visualize.
