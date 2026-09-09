---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Window Size Explained
translated: false
type: note
---

Question: What does the TCP window size do?

Answer:

The **TCP window size controls how much unacknowledged data the sender is allowed to have “in flight” at once**.

Think of TCP as:

```text
Sender                                  Receiver
  |                                        |
  |---- packet 1 ------------------------->|
  |---- packet 2 ------------------------->|
  |---- packet 3 ------------------------->|
  |---- packet 4 ------------------------->|
  |                                        |
  |<--- ACK: received 1-4, window=8 ------|
```

If the receiver advertises:

```text
window = 8 KB
```

the sender can have roughly **8 KB of data outstanding** before it must wait for ACKs.

### 1. Why do we need a window?

Without a window, TCP would effectively do:

```text
send 1 packet
wait for ACK
send 1 packet
wait for ACK
...
```

That would be terrible on a high-latency network.

Suppose:

```text
RTT = 100 ms
packet = 1 KB
```

You could only get roughly:

```text
1 KB / 0.1 s = 10 KB/s
```

With a 1 MB TCP window:

```text
1 MB / 0.1 s ≈ 10 MB/s
```

So the window allows TCP to **pipeline** many packets.

---

### 2. The important equation

A useful approximation is:

```text
throughput ≈ TCP window / RTT
```

More precisely, to fully utilize a link:

```text
window >= bandwidth × RTT
```

This is called the **bandwidth-delay product (BDP)**.

Example:

```text
Bandwidth = 1 Gbit/s
RTT       = 100 ms

BDP = 1 Gbit/s × 0.1 s
    = 100 Mbit
    = 12.5 MB
```

So you need around **12.5 MB of in-flight data** to completely fill a 1 Gbit/s link.

If your TCP window were only 64 KB:

```text
64 KB / 100 ms ≈ 640 KB/s
```

You'd dramatically underutilize the 1 Gbit/s connection.

---

### 3. TCP actually has two important windows

This is where TCP becomes interesting.

#### Receive window — `rwnd`

The receiver tells the sender:

> "I have this much buffer space available."

For example:

```text
ACK
Window = 64 KB
```

This is **flow control**.

It prevents:

```text
fast sender
    ↓
slow receiver
    ↓
receiver buffer overflow
```

#### Congestion window — `cwnd`

The sender maintains another limit:

> "Based on the network, I think I can safely have this much data in flight."

This is **congestion control**.

Therefore the sender is roughly limited by:

```text
send_window = min(rwnd, cwnd)
```

This is one of the most important ideas in TCP.

```text
                    TCP sender
                       |
             +---------+---------+
             |                   |
          rwnd limit          cwnd limit
        receiver capacity   network capacity
             |                   |
             +---------+---------+
                       |
                 min(rwnd,cwnd)
                       |
                  data in flight
```

---

### 4. Example

Suppose:

```text
rwnd = 1 MB
cwnd = 200 KB
```

Then:

```text
max outstanding data = min(1 MB, 200 KB)
                     = 200 KB
```

The receiver can accept 1 MB, but TCP's congestion-control algorithm only permits 200 KB in flight.

Later:

```text
rwnd = 100 KB
cwnd = 500 KB
```

Now:

```text
max outstanding data = 100 KB
```

The network could handle more, but the receiver doesn't have enough buffer.

---

### 5. Sliding window

The window **moves forward** as ACKs arrive.

Imagine:

```text
Sequence numbers:

0       10      20      30      40      50
|-------|-------|-------|-------|-------|

[====== WINDOW ======]
        ↑
    unacknowledged
```

After the receiver acknowledges the first 10 bytes:

```text
0       10      20      30      40      50
|-------|-------|-------|-------|-------|

        [====== WINDOW ======]
```

The window **slides forward**.

That's why TCP is often called a **sliding-window protocol**.

---

### 6. Window scaling

Classic TCP has a 16-bit advertised window:

```text
max = 65,535 bytes
```

That's too small for modern high-speed/high-latency networks.

TCP Window Scale extends it:

```text
actual_window = advertised_window × 2^scale
```

For example:

```text
advertised = 65,535
scale      = 7

window ≈ 65,535 × 128
       ≈ 8 MB
```

The scale factor is negotiated during the TCP handshake.

---

### The mental model I'd keep

TCP has two separate questions:

```text
Receiver:
"How much more can I receive?"
             ↓
            rwnd

Network:
"How much can I safely send?"
             ↓
            cwnd

             ↓

sender can have at most:

        min(rwnd, cwnd)

bytes in flight
```

And the key performance relationship is:

```text
             window
throughput ≈ -------
              RTT
```

So **TCP window size is fundamentally about controlling the amount of data that can be outstanding before ACKs arrive**, which is what lets TCP efficiently use networks with non-trivial RTTs.

I can next walk through a real TCP transfer packet-by-packet, including `seq`, `ack`, `rwnd`, `cwnd`, and retransmission.
