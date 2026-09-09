---
audio: false
generated: true
image: false
lang: en
layout: post
title: Store-and-Forward Switching Explained
translated: false
type: note
---

Question: What does **存储转发交换 (store-and-forward switching)** mean in a network switch?

Answer:

**Store-and-forward** means the switch **receives the entire Ethernet frame first, stores it in a buffer, checks it, and then forwards it** to the destination port.

The flow is:

```text
Host A
  |
  | Ethernet frame
  v
+------------------+
|      Switch      |
|                  |
|  1. Receive ALL  |
|       frame      |
|        ↓         |
|  2. Store buffer |
|        ↓         |
|  3. Check FCS   |
|        ↓         |
|  4. Lookup MAC  |
|        ↓         |
|  5. Forward     |
+------------------+
  |
  v
Host B
```

### Why "store"?

Suppose A sends a 1500-byte Ethernet frame:

```text
A
|
|  [Ethernet frame: 1500 bytes]
|  ----------------------------->
|
Switch
```

The switch **doesn't immediately forward the first bytes**.

It waits until:

```text
first byte
    ↓
...
    ↓
last byte
    ↓
complete frame in memory
```

Then it can verify the **FCS/CRC** at the end of the frame.

If the frame is corrupted:

```text
FCS check ❌
       ↓
discard frame
```

If valid:

```text
FCS check ✅
       ↓
MAC table lookup
       ↓
send out destination port
```

### Compare with cut-through

There are two important switching approaches:

|                                    | Store-and-forward | Cut-through                              |
| ---------------------------------- | ----------------- | ---------------------------------------- |
| Receive entire frame first?        | ✅ Yes             | ❌ No                                     |
| CRC/FCS checking before forwarding | ✅                 | Usually ❌                                |
| Latency                            | Higher            | Lower                                    |
| Corrupted frame propagated?        | No                | Potentially                              |
| Implementation                     | More buffering    | More latency-sensitive                   |
| Common today                       | **Very common**   | Used in specialized low-latency networks |

Cut-through can start forwarding after reading enough of the Ethernet header to know the destination MAC:

```text
Frame arrives:

[Dst MAC][Src MAC][Type][Payload........]
   ↑
   |
read this
   |
   +----> immediately start forwarding
```

Whereas store-and-forward does:

```text
[Dst MAC][Src MAC][Type][Payload........][FCS]
                                      ↑
                              receive everything
                                      ↓
                                  check FCS
                                      ↓
                                   forward
```

### Why switches normally use store-and-forward

The big advantage is **error isolation**.

Imagine:

```text
PC A ---- Switch ---- PC B
```

A sends a damaged frame:

```text
A
 |
 | corrupted frame
 v
Switch
 |
 | FCS ❌
 X
```

The switch prevents the bad frame from reaching B.

This becomes especially useful because modern switches have substantial packet buffers and operate at very high speeds.

### One subtle point

**Store-and-forward is not the same thing as routing.**

A Layer-2 Ethernet switch can do store-and-forward entirely based on MAC addresses:

```text
Ethernet frame
      ↓
receive
      ↓
FCS check
      ↓
destination MAC
      ↓
MAC address table
      ↓
output port
```

For example:

```text
MAC table

AA:AA:AA... → Port 1
BB:BB:BB... → Port 2
CC:CC:CC... → Port 3
```

If the destination is `BB:BB:BB...`, the switch forwards the frame from Port 1 → Port 2.

So, in one sentence:

> **存储转发交换 = the switch completely receives and buffers a frame, validates it (especially FCS), then forwards the frame through the appropriate port.**

This is also why **store-and-forward introduces a small forwarding latency proportional to frame size**, especially at the input link speed.
