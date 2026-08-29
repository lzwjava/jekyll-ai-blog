---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cheap GPU Repair Test Platform
translated: false
type: note
---

Question: What does your friend mean by “避开 X99，用核显，H81 + 4代U” when repairing GPUs?

Answer:

He is basically recommending a **cheap, simple test platform** for GPU repair.

### 1. “避开 X99”

**X99** is an Intel enthusiast/server-ish platform, mainly using LGA2011-3 CPUs such as Xeon E5 v3/v4.

Your friend means:

> Don't use an X99 motherboard as your GPU repair test bench.

Why? For GPU repair, you want the **simplest possible system**, because you're debugging the GPU—not the motherboard/platform.

X99 can introduce extra variables:

```text
GPU
 ↓
PCIe
 ↓
X99 motherboard
 ↓
CPU / chipset / BIOS / PCIe configuration
```

If something doesn't work, you have more possible causes.

---

### 2. “用核显就行”

This is the important part.

Use a CPU with an **integrated GPU (iGPU)** as your display adapter.

For example:

```text
H81 motherboard
+
Intel 4th-gen Core i3/i5/i7 with iGPU
+
broken GPU under test
```

The monitor connects to:

```text
H81 HDMI/DVI/VGA
       ↑
      iGPU
```

while the broken GPU is plugged into:

```text
PCIe x16
    ↑
GPU under repair
```

So the system can boot and display video **even if the discrete GPU is completely dead**.

This is very useful when repairing GPUs.

---

### 3. “H81主板，4代U”

He recommends an extremely cheap platform:

**H81 motherboard + 4th-gen Intel CPU**

For example:

```text
H81
LGA1150
    │
    └── i5-4570 / i5-4590
             │
             └── Intel HD Graphics 4600
```

You can buy this kind of used hardware very cheaply.

The ideal repair bench is something like:

```text
             ┌──────────────────┐
             │   H81 motherboard│
             │                  │
Monitor ────►│ iGPU             │
             │                  │
             │ PCIe x16         │
             └──────┬───────────┘
                    │
                    ▼
             GPU under repair
```

Then you can test:

```bash
lspci
nvidia-smi
dmesg
```

etc., without needing the repaired GPU to produce the initial display output.

### Why this is good for GPU repair

Suppose you're repairing a dead RTX 3090.

Without iGPU:

```text
GPU dead
  ↓
No display
  ↓
Harder to know whether motherboard actually booted
```

With iGPU:

```text
PC boots
  ↓
iGPU produces display
  ↓
broken RTX 3090 is detected / not detected
  ↓
you can inspect PCIe enumeration
  ↓
check power rails / VRAM / GPU core / BIOS / driver
```

So your friend's recommendation is essentially:

> **Don't waste money on a powerful test PC. Build a dirt-cheap LGA1150 test bench with an Intel CPU that has integrated graphics, and use the PCIe slot exclusively for the GPU you're repairing.**

For GPU repair, that's actually a pretty sensible setup.
