---
audio: false
generated: true
image: false
lang: en
layout: post
title: 8GB DDR4 on Skylake
translated: false
type: note
---

**DDR4.** On `.137`:

- **Type: DDR4**
- **1× 8 GB stick** installed (3 empty slots)
- Stick rated **DDR4-2400** (CL16-16-16 timing), currently running at **2133 MT/s** (default JEDEC speed on the Q170/Skylake platform)
- 1.2 V standard DDR4 voltage

Makes sense for that hardware generation — the i5-6500 (Skylake, LGA1151) + Q170 chipset is a DDR4-era board, and it matches the 7.7 GiB `free` shows.

So thinking about the H3 wall: the 8 GB DDR4 stick is a big part of the RAM bottleneck — bumping to 16/32 GB (4×8 up to 64 GB possible on 4 slots) would help with host-side offload, but the 24 GB VRAM and Maxwell-architecture walls on the GPU still remain the hard blockers.

Want me to check the RAM type on `.34` too while we're here?
