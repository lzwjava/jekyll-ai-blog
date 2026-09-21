---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pros and Cons of Stop-and-Wait ARQ
translated: false
type: note
---

Question: What are the advantages of **Stop-and-Wait ARQ (停止等待 ARQ)**?

Answer:

**Stop-and-Wait ARQ** is basically:

```text
Sender                         Receiver

  DATA #1  ------------------->
           <------------------- ACK #1

  DATA #2  ------------------->
           <------------------- ACK #2
```

If the ACK doesn't arrive before a timeout:

```text
  DATA #1  ------------------->
           X  (lost)

        timeout
  DATA #1  ------------------->  retransmit
           <------------------- ACK #1
```

### Pros

1. **Very simple to implement**

   The sender only needs to track **one outstanding packet**:

   ```python
   send(packet)
   start_timer()

   if ack_received:
       send(next_packet)
   elif timeout:
       resend(packet)
   ```

   No sliding window, congestion/window management, or complex ACK bookkeeping.

2. **Very small receiver state**

   The receiver essentially does:

   ```text
   receive packet
       ↓
   verify checksum
       ↓
   if valid:
       deliver
       ACK
   else:
       discard
   ```

   With a **1-bit sequence number** (`0/1`), it can also detect duplicate retransmissions.

3. **Reliable delivery over an unreliable link**

   Assuming the underlying channel eventually delivers packets/ACKs, Stop-and-Wait ARQ can recover from:

   * packet loss
   * corrupted packets
   * lost ACKs

   The key mechanism is:

   ```text
   DATA → ACK
          ↓
       timeout
          ↓
       retransmit
   ```

4. **No receiver buffer pressure**

   Since there is only one packet in flight:

   ```text
   sender → [one packet] → receiver
   ```

   The receiver doesn't need to buffer a large out-of-order window.

5. **Easy to reason about correctness**

   The protocol state is tiny:

   ```text
   Sender:
       WAIT_FOR_DATA
       WAIT_FOR_ACK

   Receiver:
       WAIT_FOR_DATA
   ```

   This makes it useful for **teaching, simple embedded protocols, low-speed links, and very small systems**.

### The big tradeoff

The killer downside is **poor link utilization when RTT is large**.

Suppose:

```text
packet size = 1 KB
bandwidth   = 1 Gbps
RTT         = 100 ms
```

Transmitting 1 KB takes only:

```text
8192 bits / 1e9 ≈ 8.2 μs
```

but then the sender waits roughly:

```text
100 ms
```

for the ACK.

So the link is busy for ~8 μs and idle for ~100 ms.

Approximately:

```text
utilization ≈ transmission_time / RTT
           ≈ 8.2 μs / 100 ms
           ≈ 0.0082%
```

That's why **sliding-window ARQ** exists: keep many packets in flight instead of waiting after every packet.

A useful mental model:

```text
Stop-and-Wait:

DATA → ACK → DATA → ACK → DATA → ACK
       ^^^^^
       lots of idle time


Sliding Window:

DATA DATA DATA DATA DATA DATA
       → → → → →
ACK  ACK  ACK  ACK
```

So the core tradeoff is:

| Stop-and-Wait ARQ               | Sliding Window ARQ                 |
| ------------------------------- | ---------------------------------- |
| Very simple                     | More complex                       |
| 1 packet in flight              | Many packets in flight             |
| Tiny buffers                    | Larger buffers                     |
| Easy correctness                | More state                         |
| Poor high-BDP utilization       | Good high-BDP utilization          |
| Good for simple/low-speed links | Good for high-speed/long-RTT links |

I can also derive the **Stop-and-Wait throughput formula** \\(\eta = \frac{T_t}{T_t + 2T_p + T_{ack}}\\) from first principles.
