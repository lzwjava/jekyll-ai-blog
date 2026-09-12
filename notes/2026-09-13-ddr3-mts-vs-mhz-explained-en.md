---
audio: false
generated: true
image: false
lang: en
layout: post
title: DDR3 MT/s vs MHz Explained
translated: false
type: note
---

Question: What does **1330 MT/s** mean for your DDR3 RAM?

Answer: **MT/s = megatransfers per second.** It describes how many data transfers the memory can perform per second.

Your screen shows:

```text
IMC: 665MHz (DDR3-1330)
```

The key detail is **DDR** = *Double Data Rate*.

### The math

The actual memory clock is:

```text
665 MHz
```

DDR transfers data on **both** the rising and falling edge of each clock cycle:

```text
665 MHz × 2 = 1330 million transfers/sec
                         ↑
                       1330 MT/s
```

So:

```text
Physical clock:       665 MHz
Effective rate:       1330 MT/s
```

This is why saying "DDR3-1333 runs at 1333 MHz" is technically wrong. **The DRAM clock is ~667 MHz; 1333 MT/s is the effective transfer rate.**

### How much bandwidth is that?

Your system has **64-bit-wide memory channels**. One transfer moves:

```text
64 bits = 8 bytes
```

Therefore:

```text
1330 MT/s × 8 bytes
= 10.64 GB/s
```

That's approximately **10.6 GB/s per memory channel**.

With two DIMMs in **dual-channel** operation:

```text
10.64 × 2 ≈ 21.3 GB/s
```

So your 2×4 GB setup can theoretically provide around **21 GB/s of memory bandwidth** if the motherboard is actually running both sticks in dual-channel mode.

One useful distinction:

> **MHz tells you the clock frequency. MT/s tells you the data-transfer rate.**

DDR doubles the transfers per clock, which is where the apparent 2× number comes from.
