---
audio: false
generated: true
image: false
lang: en
layout: post
title: DDR3 vs DDR4 RAM Comparison
translated: false
type: note
---

Question: Compare **DDR3 vs DDR4 RAM**.

Answer:

| Feature                  |                       DDR3 |                          DDR4 |
| ------------------------ | -------------------------: | ----------------------------: |
| Typical voltage          |     **1.5V** (1.35V DDR3L) |                      **1.2V** |
| Typical speed            |             1333–2133 MT/s |               2133–3200+ MT/s |
| Common desktop capacity  |              4–8 GB/module |                8–32 GB/module |
| Theoretical bandwidth    |                      Lower |                        Higher |
| Latency                  | Often lower in absolute ns | Often similar in real latency |
| Pin count (desktop DIMM) |                        240 |                           288 |
| Notch position           |                  Different |                     Different |
| Compatibility            |      DDR3 motherboard only |         DDR4 motherboard only |
| IMC architecture         |                      Older |                         Newer |
| Power efficiency         |                      Worse |                        Better |

### The important part: DDR4 is NOT backward compatible

You **cannot put DDR3 into a DDR4 motherboard**, even though both are called DIMM and look physically similar.

For example:

```text
Intel B85 / H81 / Z97
        │
        └── DDR3

Intel B150 / B250 / B360 / B365
        │
        └── DDR4

Intel B760 DDR4
        │
        └── DDR4
```

The physical key notch is in a different position, and the electrical interface is different.

### Performance

A simplified bandwidth calculation:

```text
bandwidth = MT/s × 8 bytes
```

So:

```text
DDR3-1600
1600 × 8 = 12.8 GB/s per channel

DDR4-3200
3200 × 8 = 25.6 GB/s per channel
```

For dual channel:

```text
DDR3-1600 → 25.6 GB/s
DDR4-3200 → 51.2 GB/s
```

So DDR4-3200 has roughly **2× the theoretical memory bandwidth** of DDR3-1600.

But don't expect applications to become 2× faster—the CPU cache hierarchy and workload matter enormously.

### For your cheap motherboard/GPU test-bench projects

This distinction is particularly useful when buying used hardware:

```text
B85 / H97 / Z97  → DDR3
B150 / B250      → DDR4
B360 / B365      → DDR4
B660 / B760      → DDR4 OR DDR5 depending on exact board
```

And **B760M DDR4** and **B760M DDR5** are separate motherboard variants. A DDR4 B760 board cannot use DDR5.

If you're buying used RAM, I can also give you a **DDR3/DDR4 compatibility cheat sheet by Intel CPU generation (4th → 14th gen)**, which is handy for your Xianyu hardware hunting.
