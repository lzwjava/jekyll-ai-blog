---
audio: false
generated: true
image: false
lang: en
layout: post
title: Lenovo L-IG41M3 PCIe Slot
translated: false
type: note
---

Question: What PCIe slot does the Lenovo L-IG41M3 have — PCIe 3/4, and x16?

Answer: **PCIe 2.0 x16**, most likely.

The distinction is:

```text
PCIe 2.0 = generation / speed
x16       = number of PCIe lanes / physical slot
```

So for the GPU slot on the G41 platform:

```text
PCIe 2.0
└── x16 physical slot
```

### What that means for GPU repair

A modern GPU such as an RTX 4070 can physically plug into it:

```text
RTX 4070
   │
   ▼
PCIe x16 slot
   │
   ▼
G41 / L-IG41M3
PCIe 2.0 x16
```

But the link will negotiate down to **PCIe 2.0**.

Approximate one-way bandwidth:

| PCIe         | x16 bandwidth |
| ------------ | ------------: |
| PCIe 1.0     |       ~4 GB/s |
| **PCIe 2.0** |   **~8 GB/s** |
| PCIe 3.0     |      ~16 GB/s |
| PCIe 4.0     |      ~32 GB/s |

For **GPU repair**, however, this isn't necessarily a problem. You're usually interested in:

```bash
lspci
lspci -vv
dmesg
```

and whether the card:

```text
PCIe device detected?
       ↓
GPU initialized?
       ↓
VRAM detected?
       ↓
driver loads?
       ↓
GPU works?
```

rather than maximum gaming bandwidth.

**One thing I'd verify before buying:** Lenovo sometimes used different configurations under similar board names. If you send me a **photo of the L-IG41M3 board**, especially the PCIe area, I can identify the slots directly.
