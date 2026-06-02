---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Calculating TCP Segments for Data Transfer
translated: false
type: note
---

Yes, your calculation is roughly correct.

Let's compute it precisely:

- 1 MB = 1,000,000 bytes (using the common network approximation; strictly 1 MiB = 1,048,576 bytes, but the difference is small)
- Maximum TCP payload per segment on Ethernet with IPv4 and no options: **1460 bytes**
  (This comes from: Ethernet MTU 1500 bytes − 20 bytes IPv4 header − 20 bytes TCP header = 1460 bytes)

So:

1,000,000 bytes ÷ 1460 bytes/segment ≈ **684.93**

→ **685 TCP segments** (the last one will be smaller)

If you use the more precise 1 MiB = 1,048,576 bytes:

1,048,576 ÷ 1460 ≈ **718.47** → **719 segments**

### Quick reference table (IPv4, no TCP/IP options, standard Ethernet):

| Application data size | Approx. number of TCP segments (1460 B payload) |
|-----------------------|-------------------------------------------------|
| 1 KB                  | ~1                                              |
| 100 KB                | ~69                                             |
| 1 MB                  | ~685                                            |
| 1 MiB                 | ~719                                            |
| 10 MB                 | ~6,850                                          |
| 100 MB                | ~68,500                                         |
| 1 GB                  | ~685,000                                        |

Note: Real-world numbers can be slightly higher because:
- TCP/IP headers sometimes have options (timestamps, SACK, etc.) → reduces payload to ~1448–1452 bytes
- IPv6 has a 40-byte header instead of 20 → reduces payload further
- Path MTU discovery or smaller interface MTU can lower it even more

So yes — for typical internet transfers, **~700 TCP segments per megabyte** is a very reasonable ballpark. Your "around 1000" was a bit high, but the order of magnitude is correct!
