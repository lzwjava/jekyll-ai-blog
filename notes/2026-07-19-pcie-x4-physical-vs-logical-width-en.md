---
audio: false
generated: true
image: false
lang: en
layout: post
title: PCIe x4 Physical vs Logical Width
translated: false
type: note
---

Question: Is PCIe x4 lane physically 1/4 the width of a PCIe x16 slot?

Answer: **Logically yes, physically not always.**

The `x4` in **PCIe 4.0 x4** means **4 PCIe lanes**, not "4 times smaller width". A PCIe lane is an independent high-speed serial link.

For bandwidth:

* PCIe 4.0 **per lane** ≈ 2 GB/s each direction
* PCIe 4.0 x4 ≈ 8 GB/s each direction
* PCIe 4.0 x16 ≈ 32 GB/s each direction

So:

```
PCIe 4.0 x16
[ lane ][ lane ][ lane ][ lane ]
[ lane ][ lane ][ lane ][ lane ]
[ lane ][ lane ][ lane ][ lane ]
[ lane ][ lane ][ lane ][ lane ]

= 16 lanes


PCIe 4.0 x4

[ lane ][ lane ][ lane ][ lane ]

= 4 lanes
```

Bandwidth-wise:

```
x4 = 4/16 = 25% of x16
```

So your intuition is correct **for electrical lanes**.

However, the **physical slot length** is different:

A motherboard may have:

```
PCIe x16 slot (physical)
==============================

PCIe x4 slot (physical)
=============
```

But manufacturers often put **x4 electrical connections inside an x16-length slot**:

```
Physical x16 slot:

==============================
|                            |
|  GPU inserted here         |
|                            |
==============================

Electrical:
[====]------------------------
 4 lanes connected
```

This is common for motherboard expansion slots.

Examples:

* A GPU slot might look like x16 but actually be **PCIe 4.0 x4**
* A small NVMe adapter slot might be **PCIe 4.0 x4**
* A second GPU slot on cheaper mATX boards is often **x4 electrical**

You can check with Linux:

```bash
lspci -vv | grep -A20 VGA
```

Example:

```
LnkCap: Speed 16GT/s, Width x16
LnkSta: Speed 16GT/s, Width x8
```

Meaning:

* The GPU supports x16
* Currently connected with x8

For your dual RTX 3090 / 4070 type setup, this matters:

* RTX 3090 on PCIe 4.0 x16 → ideal
* RTX 3090 on PCIe 4.0 x8 → usually only a few % slower for training
* RTX 3090 on PCIe 4.0 x4 → can hurt multi-GPU training because GPU-to-GPU data movement becomes limited

A typical consumer motherboard:

```
CPU PCIe lanes:
    GPU1: PCIe 4.0 x16  ✅

Chipset lanes:
    GPU2: PCIe 4.0 x4   ⚠️
```

For 2×3090, you usually want an ATX workstation-style board with:

```
CPU
 |
 +-- PCIe x16 slot 1  (x16)
 |
 +-- PCIe x16 slot 2  (x8/x8)
```

rather than mATX where the second slot is often only x4.
