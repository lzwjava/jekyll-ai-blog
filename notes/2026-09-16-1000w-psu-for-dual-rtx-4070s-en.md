---
audio: false
generated: true
image: false
lang: en
layout: post
title: 1000W PSU for Dual RTX 4070s
translated: false
type: note
---

Question: For **two RTX 4070s** in the X370 Gaming K3, what PSU should I use?

Answer: **I'd buy a good 1000W PSU.**

The math is roughly:

```text
RTX 4070 #1       ~200 W
RTX 4070 #2       ~200 W
CPU               ~65–150 W
Motherboard/RAM   ~50–80 W
SSD/fans/etc.     ~30–50 W
--------------------------------
Typical total     ~545–680 W
```

NVIDIA rates the RTX 4070 at **200 W TGP** and recommends **650 W for a single 4070**. ([NVIDIA][1])

For **2 × 4070**, I'd choose:

| PSU        | Verdict                     |
| ---------- | --------------------------- |
| 650 W      | ❌ No                        |
| 750 W      | ⚠️ Too little headroom      |
| 850 W      | ✅ Can work                  |
| **1000 W** | **✅ My choice**             |
| 1200 W     | Overkill unless future GPUs |

### More important: PSU connectors

Don't just look at the wattage. For two 4070s, get a PSU with **enough independent PCIe GPU power cables**.

For example:

```text
PSU
 ├── PCIe cable #1 → RTX 4070 #1
 ├── PCIe cable #2 → RTX 4070 #2
 └── CPU EPS 8-pin → X370 motherboard
```

Ideally use a modern **ATX 3.x / PCIe 5.x 1000W PSU** with native GPU connectors, rather than relying on a pile of adapters.

### But there's a bigger problem with this motherboard

The X370 Gaming K3 has:

```text
PCIEX16 → PCIe 3.0 x16
PCIEX4  → PCIe 2.0 x4
```

and the second slot can fall to **x2** depending on the other PCIe slots. ([GIGABYTE][2])

So:

```text
RTX 4070 #1 → PCIe 3.0 x16
RTX 4070 #2 → PCIe 2.0 x4   ← very limited
```

This is **not an ideal 2×4070 AI machine**. The PSU isn't the bottleneck; **the motherboard's PCIe topology is**.

If your goal is specifically **two 4070s for LLM inference/training**, I'd actually reconsider the motherboard before buying the PSU.

[1]: https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4070-family/?utm_source=chatgpt.com "GeForce RTX 4070 Family Graphics Cards | NVIDIA"
[2]: https://www.gigabyte.com/Motherboard/GA-AX370-Gaming-K3-rev-10/sp?utm_source=chatgpt.com "GA-AX370-Gaming K3 (Rev. 1.0) Motherboard - GIGABYTE Global"
