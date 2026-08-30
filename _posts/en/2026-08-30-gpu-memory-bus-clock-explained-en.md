---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Memory Bus & Clock Explained
translated: false
type: note
---

Question: What do "memory", "memory bus", and "memory clock" mean in a GPU?

Answer:

**Memory (VRAM)**
The GPU's dedicated video RAM — a pool of high-speed memory used to store everything the GPU is actively working with: textures, frame buffers, render targets, shaders, and geometry data. More VRAM lets you run higher resolutions, larger textures, and more complex scenes without stuttering. Common types are GDDR6, GDDR6X, and HBM3.

**Memory Bus (Memory Bus Width)**
The physical "highway" connecting the GPU chip to its VRAM. Measured in bits (e.g., 128-bit, 256-bit, 384-bit). A wider bus means more data can travel in parallel per clock cycle — so a 256-bit bus moves twice as much data at once as a 128-bit bus, all else being equal. It directly determines how much raw bandwidth is possible.

**Memory Clock (Memory Frequency)**
How fast the VRAM operates, measured in MHz or Gbps (effective). A higher clock means the bus transfers data more times per second. Manufacturers usually advertise the *effective* speed (e.g., "18 Gbps"), which already accounts for the double/quad-pumped nature of GDDR memory.

---

**How they combine — Memory Bandwidth:**
These three factors work together to produce the most important derived metric:

> **Bandwidth (GB/s) = (Bus Width ÷ 8) × Effective Clock Speed**

Example — RTX 4090:

- Bus: 384-bit → 48 bytes wide
- Clock: ~21 Gbps effective
- Bandwidth: 48 × 21 = **~1,008 GB/s**

A GPU bottlenecked on bandwidth (not enough for its shader throughput) will underperform no matter how powerful its compute cores are.

---

References:

- [GPU Memory Bandwidth Explained — TechPowerUp](https://www.techpowerup.com/gpu-specs/)
- [VRAM: How Much Do You Need? — Digital Foundry / Eurogamer](https://www.eurogamer.net/digitalfoundry-2023-how-much-vram-do-you-need)
- [GDDR6 vs GDDR6X vs HBM — AnandTech](https://www.anandtech.com)
