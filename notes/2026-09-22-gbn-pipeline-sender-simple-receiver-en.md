---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GBN: Pipeline Sender, Simple Receiver"
translated: false
type: note
---

Question: Why does Go-Back-N use `send_window > 1` but `receive_window = 1`?

Answer:

Because **GBN's goal is to pipeline packets at the sender while keeping the receiver extremely simple**.

### 1. Sender window > 1 = pipeline

If the sender could only have one packet outstanding:

```text
send 0 ──────────────> ACK 0
send 1 ──────────────> ACK 1
send 2 ──────────────> ACK 2
```

The sender spends most of its time waiting for the RTT.

With `send_window = 4`:

```text
send 0 ──>
send 1 ──>
send 2 ──>
send 3 ──>

             <── ACK 0
             <── ACK 1
             <── ACK 2
             <── ACK 3
```

Now the network is a **pipeline**.

The sender doesn't need to wait for each packet's ACK before sending the next one.

---

### 2. Why `receive_window = 1`?

GBN deliberately makes the receiver **in-order only**.

Suppose:

```text
sender                  receiver

  0 --------------------> receive 0
  1 --------------------> receive 1
  2 --------X
  3 --------------------> ???
```

Receiver is expecting `2`.

It gets `3`.

With:

```text
receive_window = 1
```

the receiver says:

```python
if packet.seq == expected:
    deliver(packet)
    expected += 1
else:
    discard(packet)
```

So:

```text
3 → discard
4 → discard
5 → discard
```

It only remembers:

```text
expected = 2
```

and keeps ACKing:

```text
ACK 1
```

Eventually:

```text
timeout(2)
```

Sender goes back:

```text
2 → retransmit
3 → retransmit
4 → retransmit
```

That's **Go-Back-N**.

---

### 3. Why not make receive window > 1?

You *can*. But then you're moving toward **Selective Repeat**.

For example:

```text
sender                  receiver

0 --------------------> ✓
1 --------------------> ✓
2 --------X
3 --------------------> buffer[3]
4 --------------------> buffer[4]
```

Now the receiver needs:

```python
buffer = {}

if pkt.seq == expected:
    deliver(pkt)
    expected += 1

    # maybe deliver buffered packets
elif pkt.seq > expected:
    buffer[pkt.seq] = pkt
```

And the sender needs to know that:

```text
2 is missing
3 is already received
4 is already received
```

So it should retransmit **only 2**, not 3 and 4.

That's essentially Selective Repeat.

---

### 4. The design tradeoff

Think of the two protocols like this:

```text
                  Receiver complexity
                         ↑
                         |
               Selective Repeat
                         |
                         |  buffer out-of-order
                         |
                         |
GBN --------------------+----------------→ bandwidth efficiency
                         |
                         |
                         |
```

**GBN:**

```text
send_window = N
recv_window = 1

sender:   complicated enough to pipeline
receiver: extremely simple
```

**Selective Repeat:**

```text
send_window = N
recv_window = N

sender:   tracks individual packets
receiver: buffers out-of-order packets
```

---

### 5. The subtle point

`receive_window = 1` does **not** mean the network only sends one packet at a time.

It means:

> **The receiver is only willing to accept one sequence position—the next packet it expects.**

There can still be many packets physically in flight:

```text
                    network

sender                              receiver
  │                                    │
  │── 0 ──────────────────────────────>│ ✓
  │── 1 ──────────────────────────────>│ ✓
  │── 2 ─────────── X                  │
  │── 3 ──────────────────────────────>│ discard
  │── 4 ──────────────────────────────>│ discard
  │                                    │
  │<────────────── ACK 1 ──────────────│
```

So:

```text
send window = "how many I can have outstanding"

receive window = "how far ahead I am willing to accept"
```

For GBN:

```text
             Sender                     Receiver

             [ 0 1 2 3 ]  ───────────>  [ 0 ]
               ↑                           ↑
          multiple in flight          only next one
```

That's the whole trick: **pipeline on the sender side, simplicity on the receiver side**.

I can next walk through the exact `base / nextseqnum / expectedseqnum` state transitions for one lost packet—the easiest way to make GBN click.