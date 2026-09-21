---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Receive Window Flow Control
translated: false
type: note
---

Question: How does TCP manage flow control?

Answer:

TCP flow control answers one specific question:

> **How fast can the sender transmit without overflowing the receiver's buffer?**

The key mechanism is the **receive window (`rwnd`)** advertised by the receiver.

### 1. Receiver advertises how much buffer is available

Suppose the receiver has a TCP receive buffer:

```text
+---------------------------------------------+
| already consumed | received | free space    |
+---------------------------------------------+
                     ↑           ↑
                  bytes       rwnd = 8 KB
```

The receiver puts `rwnd = 8192` in its TCP header.

Conceptually:

```text
Receiver → Sender:
ACK=1000
Window=8192
```

This means:

```text
"I have received everything through byte 999,
and you may have at most 8192 unacknowledged bytes outstanding."
```

---

### 2. Sender tracks the usable window

TCP sequence numbers are byte-oriented.

Suppose:

```text
SND.UNA = 1000   # oldest unacknowledged byte
SND.NXT = 5000   # next byte sender will transmit
rwnd    = 8192
```

Then:

```text
bytes_in_flight = SND.NXT - SND.UNA
                = 4000
```

So the sender can send:

```text
rwnd - bytes_in_flight
= 8192 - 4000
= 4192 bytes
```

The fundamental constraint is:

```text
SND.NXT - SND.UNA <= rwnd
```

Or equivalently:

```text
in_flight <= receive_window
```

---

### 3. As the receiver consumes data, the window opens

Imagine:

```text
rwnd = 8192
```

Sender fills it:

```text
Sender ──────────────── 8192 bytes ────────────────> Receiver

                                               buffer:
                                               [########]
                                               free = 0
                                               rwnd = 0
```

The receiver's application then reads 4 KB:

```text
Application
     │
     │ read()
     ▼
+------------------+
| TCP receive buf  |
|      4 KB free   |
+------------------+
```

TCP can advertise:

```text
ACK=...
Window=4096
```

Now the sender can transmit another 4 KB.

So flow control continuously follows:

```text
application consumes data
        ↓
receive buffer gets free space
        ↓
receiver advertises larger rwnd
        ↓
sender is allowed to send more
```

---

## 4. What happens when the receiver is too slow?

Suppose:

```text
Receiver buffer = 64 KB
Application consumption = 1 MB/s
Sender rate       = 10 MB/s
```

The receive buffer fills:

```text
                    TCP receive buffer
                ┌──────────────────────┐
incoming ──────►│######################│
                └──────────────────────┘
                         free = 0
                         rwnd = 0
```

Receiver sends:

```text
Window = 0
```

The sender must stop sending new data.

This is **TCP flow control**.

It prevents:

```text
fast sender
    ↓
slow receiver
    ↓
receiver buffer overflow
```

---

## 5. Zero-window probing

A subtle problem appears when:

```text
Receiver → Sender:
rwnd = 0
```

What if the receiver later opens the window, but the sender somehow misses that update?

TCP has **zero-window probes**.

The sender periodically sends a small probe asking essentially:

```text
"What's your current receive window?"
```

The receiver responds with its current ACK/window.

So a zero window doesn't permanently deadlock the connection.

---

## 6. Window scaling

The TCP header's Window field is only **16 bits**.

Maximum raw window:

```text
2^16 - 1 = 65,535 bytes
```

That's far too small for modern high-bandwidth/high-latency links.

TCP therefore negotiates the **Window Scale** option during the three-way handshake.

For example:

```text
Window field = 32768
scale = 7
```

Effective window:

```text
32768 << 7
= 4,194,304 bytes
≈ 4 MB
```

The scale factor is negotiated during:

```text
SYN
SYN-ACK
```

and then applies to subsequent window advertisements.

---

# Flow control vs congestion control

This distinction is extremely important.

TCP actually has **two independent limits**:

```text
                   Sender
                     │
             ┌───────┴────────┐
             │                │
          rwnd             cwnd
             │                │
       receiver limit    network limit
             │                │
             └───────┬────────┘
                     ↓
             actual send window
```

Approximately:

```text
send_window = min(rwnd, cwnd)
```

### `rwnd` — flow control

Controlled by:

```text
receiver
```

Question:

> "Can my receive buffer handle more data?"

### `cwnd` — congestion control

Controlled by:

```text
sender
```

based on observations of the network.

Question:

> "Can the network handle more data?"

So imagine:

```text
rwnd = 10 MB
cwnd = 2 MB

send_window = min(10 MB, 2 MB)
            = 2 MB
```

The receiver is fine; the **network** is the bottleneck.

Conversely:

```text
rwnd = 64 KB
cwnd = 10 MB

send_window = 64 KB
```

The network is fine; the **receiver** is the bottleneck.

---

## The mental model

You can reduce TCP's flow-control mechanism to this:

```text
Receiver:

    receive buffer
          │
          ▼
     free capacity
          │
          ▼
         rwnd
          │
          │ advertised in ACKs
          ▼
Sender:

     can send only while

     unacked_bytes < rwnd
```

And in real TCP:

```text
                    ┌── receiver ──► rwnd
                    │
application ──► TCP ┤
                    │
                    └── network ───► cwnd

              sendable =
              min(rwnd, cwnd)
```

The interesting part is that **TCP flow control is fundamentally a sliding-window protocol**: ACKs move the left edge of the sender's window, while the advertised receive window determines how far the right edge may extend.

If you want to understand TCP at packet level, the next useful step is to walk through **10 packets with `SEQ`, `ACK`, `SND.UNA`, `SND.NXT`, `RCV.NXT`, `rwnd`, and `cwnd` after every packet**.
