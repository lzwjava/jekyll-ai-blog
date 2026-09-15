---
audio: false
generated: true
image: false
lang: en
layout: post
title: Finding True Dual x16 AM4 Boards
translated: false
type: note
---

Question: How do I find an AM4 motherboard with **two physically x16 slots that are also electrically x16**?

Answer: Search for the spec **“2 × PCIe x16, x16/x16”** or, more commonly, **“2 × PCIe x16 (x16/x16)”**. But there is a catch: on consumer AM4 platforms, **CPU lane availability** determines whether true x16/x16 is possible.

### The key thing

For Ryzen desktop CPUs on AM4, you normally have:

```text
CPU
 ├── PCIe x16  ──> GPU 1
 └── PCIe x4   ──> NVMe / chipset
```

To get:

```text
GPU 1 = x16
GPU 2 = x16
```

the motherboard needs a **PCIe lane switch / PLX-style switch**, or a platform/CPU with more lanes.

Most AM4 boards instead do:

```text
GPU 1 = x16
GPU 2 = x4
```

or:

```text
GPU 1 = x8
GPU 2 = x8
```

The latter is what you want if you're okay with **x8/x8**.

### What to search for

For AM4:

```text
"AM4 PCIe x8 x8 motherboard"
"X570 PCIe x8 x8"
"X570S PCIe x8 x8"
"AM4 2 x PCIe x16 x8 x8"
```

Look specifically at the motherboard manual/specification and find something like:

```text
1 x PCI Express x16 slot, running at x16
1 x PCI Express x16 slot, running at x8
```

and CPU support:

```text
PCIe x16/x8
```

When both GPUs are installed, the CPU lanes are bifurcated:

```text
CPU
       16 lanes
    ┌────────────┐
    │            │
  x8 GPU 1     x8 GPU 2
```

That's **much better than x16 + x4** for two-GPU workloads.

### If you literally require x16 + x16

I'd **not target AM4**. Look at platforms with more CPU PCIe lanes, e.g.:

* **Threadripper / sTRX4 / sTRX40**
* **Threadripper Pro**
* **EPYC**
* Modern workstation/server platforms

Those CPUs have enough lanes to do:

```text
GPU 1: x16
GPU 2: x16
GPU 3: x16
...
```

without stealing lanes from each other.

If you tell me **which two GPUs you're trying to put in the machine**, I can tell you whether **x16+x4, x8+x8, or true x16+x16** actually matters for your workload.
