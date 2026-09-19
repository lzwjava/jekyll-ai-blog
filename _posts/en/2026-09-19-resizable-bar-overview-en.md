---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resizable BAR Overview
translated: false
type: note
---

## BAR = Base Address Register

Every PCIe device (GPU, NIC, NVMe, etc.) has up to six **BARs** (BAR0–BAR5). Each BAR is a request that says to the firmware/OS: *"I have a chunk of memory you need to map into the CPU's physical address space, and here is how big it is."*

For a GPU, the big one is **BAR1** — the window the CPU uses to reach the graphics card's **VRAM (framebuffer)**.

### The old model: small fixed window

Historically a GPU's VRAM BAR was capped at a small size — classically **256 MB** — and it was **fixed**; neither the BIOS nor the OS could change it. VRAM itself was much bigger (8, 16, 24 GB). So the CPU could only "see" a 256 MB slice of VRAM at a time:

```
CPU address space
 ┌───────────────┐
 │   ...         │
 │ ┌───────────┐ │      GPU VRAM (16 GB)
 │ │ BAR1      │ │      ┌──────────────────────────┐
 │ │ 256 MB    │─┼─────►│ only a 256 MB slice is   │
 │ │ (window)  │ │      │ reachable at once        │
 │ └───────────┘ │      └──────────────────────────┘
 └───────────────┘
```

To move data, the driver had to bounce buffers through that 256 MB window: copy into the window, tell the GPU to read, copy the next chunk, etc. Extra copies, extra driver work, lower throughput.

**Analogy:** VRAM is a huge warehouse. BAR1 is the loading-dock door. Without ReBAR the door is a mail slot — you can still get everything in and out, but only a bit at a time.

### Resizable BAR (ReBAR)

**Resizable BAR** is a PCIe specification feature (a capability the device advertises) that lets the firmware/OS **change the size of the BAR** at boot — typically from a small value up to the **full VRAM size**. Now the CPU can address the entire framebuffer directly:

```
 ┌───────────────────────────────┐
 │ BAR1 = 16 GB                  │─────► entire 16 GB VRAM
 │ (whole framebuffer mapped)    │       directly addressable
 └───────────────────────────────┘
```

**Analogy:** the loading-dock door is widened to the full size of the warehouse, so the CPU can reach any box without shuttling.

**What it buys you:** the driver can write straight into the VRAM region it wants (e.g., upload a texture directly to its final location) instead of staging it through a small window. Real-world gain is usually modest — single-digit percent in games, sometimes more in specific workloads. AMD markets it as **Smart Access Memory (SAM)**; NVIDIA as **Resizable BAR**. Same thing.

### It needs all three layers to cooperate

| Layer | Requirement |
|---|---|
| **GPU** | Must advertise the Resizable BAR capability (Pascal and newer on the NVIDIA side) |
| **Platform/firmware** | BIOS/UEFI + root complex + chipset must support resizing and allocate the address space |
| **OS/driver** | Driver must actually request the larger size |

Miss any one and you get the old fixed small BAR.

### The related-but-different piece: *Above 4G Decoding*

This is a **prerequisite, not the same thing**. A large BAR (say 16 GB) doesn't fit in the low MMIO region below the 4 GB address boundary, which is crowded with RAM and other device windows. **Above 4G Decoding** tells the BIOS: *"it's fine to place PCIe MMIO address ranges **above** the 4 GB line, using the CPU's 64-bit physical address space."* Without it, a big BAR has nowhere to go.

That's exactly your P100 situation:

```
P100 BAR1 = 0x4_0000_0000 = 16 GB, 64-bit prefetchable
BIOS: "can't assign; no space"   ← no Above 4G window exists
```

So for the P100, **Above 4G Decoding is the thing you need** — it's what would let that 16 GB BAR1 be placed. Resizable BAR is a *different* mechanism for dynamically resizing a BAR up and down; the Tesla P100 exposes a large **fixed** 16 GB BAR rather than a resizable one, and in any case your B85 platform supports neither.

### One-line summary

> **A BAR is the address window the CPU uses to talk to a device's memory. Resizable BAR lets that window grow to cover the whole GPU memory instead of a fixed small slice, so the CPU/GPU can exchange data with fewer copies. It requires GPU + motherboard + driver support — and a big BAR also needs "Above 4G Decoding" to have somewhere to live.**