---
audio: false
generated: true
image: false
lang: en
layout: post
title: Go-Back-N Sliding Window Protocol
translated: false
type: note
---

Question: Intro to Go-Back-N (GBN) sliding-window protocol.

Answer:

**Go-Back-N (GBN)** is a reliable data-transfer protocol built on top of an unreliable network. The key idea is:

> Send multiple packets without waiting for each ACK, but if one packet is lost, retransmit that packet **and everything after it**.

### 1. Stop-and-wait → sliding window

Stop-and-wait:

```text
Sender                         Receiver
  | ---- packet 0 ------------> |
  | <---- ACK 0 --------------- |
  | ---- packet 1 ------------> |
  | <---- ACK 1 --------------- |
```

Only one packet can be "in flight".

GBN allows a **window** of packets:

```text
Sender                         Receiver

  | ---- packet 0 ------------> |
  | ---- packet 1 ------------> |
  | ---- packet 2 ------------> |
  | ---- packet 3 ------------> |
  | <---- ACK 0 --------------- |
  | <---- ACK 1 --------------- |
```

If:

```text
window_size = 4
```

the sender can have up to 4 unacknowledged packets.

---

### 2. The sender window

Suppose:

```text
seq = 0 1 2 3 4 5 6 7 ...
             ^
          window = 4
```

Initially:

```text
[0 1 2 3] 4 5 6 7
 ^       ^
base    nextseqnum
```

* `base` = oldest unacknowledged packet
* `nextseqnum` = next packet we can send
* `N` = window size

The sender can send while:

```python
nextseqnum < base + N
```

When ACKs arrive, the window slides:

```text
ACK 0

    [1 2 3 4] 5 6 7
```

Then:

```text
ACK 1

      [2 3 4 5] 6 7
```

Hence **sliding window**.

---

### 3. The important GBN behavior

Consider:

```text
Sender                         Receiver

packet 0 --------------------> OK
packet 1 --------------------> OK
packet 2 --------X             LOST
packet 3 --------------------> 
packet 4 -------------------->
```

The receiver expects packet `2`.

It receives `3`, but:

```text
expected = 2
received = 3
```

GBN receiver generally **discards packet 3**.

Then discards 4 too.

It keeps sending an ACK for the last correctly received **in-order** packet:

```text
ACK 1
```

Eventually the sender's timer for packet 2 expires:

```text
timeout(packet 2)
```

Then:

```text
packet 2 -------------------->
packet 3 -------------------->
packet 4 -------------------->
```

This is where the name comes from:

> **Go back to N** — go back to the missing packet and retransmit from there.

---

### 4. Minimal sender state

You can think of GBN as basically:

```python
base = 0
next_seq = 0
N = 4

while True:
    if next_seq < base + N:
        send(packet[next_seq])
        next_seq += 1

    ack = receive_ack()

    if ack is not None:
        # cumulative ACK
        base = ack + 1

        if base == next_seq:
            stop_timer()
        else:
            restart_timer()
```

The critical property is that ACKs are usually **cumulative**.

If receiver sends:

```text
ACK 4
```

it means roughly:

```text
"I have received 0..4 in order."
```

So the sender can advance:

```text
base = 5
```

---

### 5. Receiver is extremely simple

Conceptually:

```python
expected = 0

while True:
    pkt = receive()

    if pkt.seq == expected:
        deliver(pkt)
        send_ack(expected)
        expected += 1
    else:
        # out of order
        discard(pkt)
        send_ack(expected - 1)
```

This simplicity is one of GBN's main characteristics.

The receiver does **not** buffer out-of-order packets.

---

### 6. GBN vs Selective Repeat

This distinction is the important part:

```text
                 Lost 2

GBN:

0 ✓
1 ✓
2 ✗
3 discarded
4 discarded

timeout →

2 retransmit
3 retransmit
4 retransmit
```

Selective Repeat:

```text
0 ✓
1 ✓
2 ✗
3 buffered ✓
4 buffered ✓

timeout →

2 retransmit only
```

So:

|                      | Go-Back-N        | Selective Repeat   |
| -------------------- | ---------------- | ------------------ |
| Out-of-order packet  | Discard          | Buffer             |
| ACK                  | Cumulative       | Usually individual |
| Loss of packet 2     | Retransmit 2,3,4 | Retransmit 2 only  |
| Receiver complexity  | Low              | Higher             |
| Bandwidth efficiency | Lower            | Higher             |

---

### 7. Why use a window at all?

Because network latency is expensive.

Suppose:

```text
RTT = 100 ms
packet transmission = 1 ms
```

Stop-and-wait:

```text
send 1ms
wait ~99ms
send
wait
...
```

Link utilization is roughly:

```text
1 / 100 = 1%
```

With:

```text
window = 100
```

you can pipeline packets:

```text
0 1 2 3 4 5 6 7 8 9 ...
→ → → → → → → → → →
```

while earlier packets are traveling through the network.

The rough requirement for keeping the pipe full is:

```text
window_size ≳ bandwidth × RTT / packet_size
```

or in packets:

```text
W ≳ RTT / packet_transmission_time
```

This is the core connection between **sliding windows and high-throughput reliable transport**.

---

### 8. Mental model

Think of GBN as:

```text
                 sender window
                       ↓
        ┌──────────────────────────┐
        │  10  11  12  13  14     │
        └──────────────────────────┘
         ↑              ↑
       base          next_seq

                 network
                    ↓
             10 → 11 → 12 → 13
                       X
                      lost

timeout(12)
    ↓

retransmit:

             12 → 13 → 14
```

The three concepts to internalize are:

```text
Sliding window
      +
Cumulative ACK
      +
Timeout → retransmit everything after the loss
      =
Go-Back-N
```

References:

* [RFC 793 — Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc793)
* [Computer Networking: A Top-Down Approach — Reliable Data Transfer](https://gaia.cs.umass.edu/kurose_ross/online_lectures.htm)
