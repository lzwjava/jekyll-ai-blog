---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decoding MODS Memory Training Status
translated: false
type: note
---

Question: **What do `NV_PFB_FBPA_*_TRAINING_STATUS = 0x00`, `0x02`, etc. mean in a MODS log?**

Answer:

Yes — these are **memory PHY training results**. They are extremely useful for diagnosing VRAM faults.

A typical MODS section looks like:

```text
NV_PFB_FBPA_0_TRAINING_STATUS = 0x00000000
NV_PFB_FBPA_1_TRAINING_STATUS = 0x00000002
NV_PFB_FBPA_2_TRAINING_STATUS = 0x00000000
NV_PFB_FBPA_3_TRAINING_STATUS = 0x00000008
```

Think of it as:

```text
GPU
 └── FBPA
      ├── FBPA 0 → memory channel A
      ├── FBPA 1 → memory channel B
      ├── FBPA 2 → memory channel C
      ...
```

The training is essentially the GPU trying to establish reliable electrical timing between the GPU memory controller and GDDR memory. MODS exposes the result through `NV_PFB_FBPA_*_TRAINING_STATUS`. A public MODS example shows `FBPA_3 = 0x08` followed by `Memory DQ write training failed`. ([VLab][1])

### The useful values

For the common GDDR MODS logs:

| Training status | Meaning                          |
| --------------- | -------------------------------- |
| `0x00`          | **PASS / training completed**    |
| `0x02`          | **Bank 0 failure**               |
| `0x08`          | **Bank 1 failure**               |
| `0x0A`          | **Both bank 0 + bank 1 failure** |

So:

```text
FBPA_0 = 0x00
```

means that channel trained successfully.

Whereas:

```text
FBPA_0 = 0x02
```

means approximately:

```text
Channel A
└── Bank 0  ← failure
```

and:

```text
FBPA_0 = 0x08
```

means:

```text
Channel A
└── Bank 1  ← failure
```

and:

```text
FBPA_0 = 0x0A
```

means both:

```text
Channel A
├── Bank 0  ← failure
└── Bank 1  ← failure
```

This mapping is also documented in practical MODS/MATS repair work. ([GPU Solutions][2])

### Important: `FBPA_0` ≠ necessarily "VRAM chip 0"

This is where people often get confused.

`FBPA_0` is a **memory-controller/channel topology identifier**, not simply "the first physical VRAM chip."

For example, on a card with channels A–H:

```text
FBPA_0 → A
FBPA_1 → B
FBPA_2 → C
FBPA_3 → D
...
```

Then:

```text
FBPA_3 = 0x08
```

would indicate:

```text
D1
```

under the common mapping.

But **which physical memory package is D1 on the PCB depends on the GPU/card's memory topology**. The training status tells you the failing logical memory location; it doesn't by itself tell you whether the physical problem is the DRAM package, solder/pads, traces, or GPU-side connection. ([GPU Solutions][2])

### And this is different from your previous `Error 220`

This distinction matters for your card.

Your screenshot showed:

```text
Error 220
Gpu.Initialize pci device not found
```

That means MODS **didn't get far enough to initialize the GPU**.

A log such as:

```text
NV_PFB_FBPA_0_TRAINING_STATUS = 0x00000000
...
NV_PFB_FBPA_3_TRAINING_STATUS = 0x00000008

Error 00000507:
Memory DQ write training failed
```

is a completely different situation: **the GPU was found and initialized far enough to perform memory training, but a memory channel failed.** The public MODS example shows exactly this sequence. ([VLab][1])

So if you're repairing a GPU, **the full `NV_PFB_FBPA_*_TRAINING_STATUS` block is much more interesting than the final error code alone.**

If you paste your actual block, e.g.

```text
NV_PFB_FBPA_0_TRAINING_STATUS = ...
NV_PFB_FBPA_1_TRAINING_STATUS = ...
...
```

I can decode it into **A0/A1/B0/B1/etc. and tell you which VRAM channel(s) are likely bad**.

References:

* [MODS/MATS memory training examples](https://vlab.su/viewtopic.php?f=48&p=1010828&t=124090) ([VLab][1])
* [MODS FBPA training-status decoding](https://gpusolutions.net/tag/memory-testing/) ([GPU Solutions][2])

[1]: https://vlab.su/viewtopic.php?f=48&p=1010828&t=124090&utm_source=chatgpt.com "MATS/MODS 400/455/520/570 Тест видеопамяти nVidia для флешки • VLab"
[2]: https://gpusolutions.net/tag/memory-testing/?utm_source=chatgpt.com "Memory Testing Archives - GPU Solutions"
