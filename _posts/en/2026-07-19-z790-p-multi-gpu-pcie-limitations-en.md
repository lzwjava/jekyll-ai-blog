---
audio: false
generated: true
image: false
lang: en
layout: post
title: Z790-P Multi-GPU PCIe Limitations
translated: false
type: note
---

Question: **How good is the PCIe layout of MSI PRO Z790-P for multi-GPU / AI workloads?**

Answer:

The MSI PRO Z790-P has a **consumer desktop PCIe layout**, not a workstation/server multi-GPU layout. It is good for **one powerful GPU + expansion cards**, but not ideal for **2× RTX 3090 / AI training rigs**.

The slots:

```
CPU PCIe lanes:
PCI_E1:
    PCIe 5.0 x16
    ↑ directly connected to Intel CPU

Z790 chipset lanes:
PCI_E3:
    PCIe 4.0 x4

PCI_E4:
    PCIe 3.0 x1

PCI_E2:
    PCIe 3.0 x1
```

Physical layout:

```
CPU
 |
 |  PCIe 5.0 x16
 |
[ GPU slot ]  <- RTX 4070 / 3090 here

(blank space)

[ PCIe x4 slot ] <- second GPU possible but only x4

[ PCIe x1 ]

[ PCIe x1 ]
```

## For RTX 3090 + RTX 3090

Example:

### GPU1

RTX 3090:

```
PCIe 4.0 x16
```

Actually runs:

```
PCIe 4.0 x16
```

Good.

### GPU2

RTX 3090:

```
PCI_E3:
PCIe 4.0 x4
```

Bandwidth:

```
PCIe 4.0:
1 lane ≈ 2 GB/s each direction

x4:
≈ 8 GB/s
```

Compared with x16:

```
x16:
≈ 32 GB/s
```

So second GPU has only 25% bandwidth.

For inference:

```
GPU1 -> model layers
GPU2 -> model layers
```

PCIe x4 is usually OK.

For training:

```
GPU1 gradients
       |
       | PCIe
       |
GPU2 gradients
```

x4 becomes painful.

---

## The bigger issue: Intel desktop CPU lanes

Your i9-13900KF:

```
CPU PCIe lanes:
16 lanes GPU
4 lanes NVMe
```

Only:

```
GPU:
x16
```

There is no:

```
x16/x16
```

support.

The motherboard cannot create lanes.

A Z790 board does not magically give more GPU bandwidth.

---

## Compare better boards

For your AI use case (3090, 4070, ROCm experiments), look for:

### MSI MPG Z790 Carbon WiFi

Better:

```
GPU1:
PCIe 5.0 x16

GPU2:
PCIe 5.0 x8
```

because it uses CPU bifurcation.

Both GPUs get CPU lanes:

```
x8 + x8
```

Much better.

---

### ASUS ProArt Z790 Creator WiFi

More workstation-like:

```
PCIe 5.0 x16
PCIe 5.0 x8
Thunderbolt
10Gb Ethernet
```

Good for creators / AI.

---

### Real multi-GPU platform

If your goal becomes:

```
2× RTX 3090
4× RTX 3090
```

then consumer Intel is the wrong platform.

Need:

* AMD Threadripper
* Intel Xeon W
* EPYC

Example:

Threadripper:

```
CPU PCIe lanes:
64-128 lanes
```

Then:

```
GPU1 x16
GPU2 x16
GPU3 x16
GPU4 x16
```

---

## For your current situation

You have:

* i9-13900KF
* RTX 4070
* AI training interest
* considering RTX 3090 second hand

I would rank options:

### Option A — cheapest

Keep PRO Z790-P:

```
RTX 4070:
PCIe x16

RTX 3090:
PCIe x4
```

Good for:

* LLM inference
* QLoRA
* vLLM experiments
* running 40B+ models

Not optimal for:

* distributed training

---

### Option B — change motherboard

Buy Z790 with x8/x8:

```
RTX 3090
+
RTX 3090

both x8
```

Much cleaner.

---

### Option C — workstation

Later:

```
Threadripper + 4 GPUs
```

when you really need multi-GPU training.

---

For your use case (training GPT-2 class models, experimenting with 24GB VRAM), **the PRO Z790-P is acceptable. The second RTX 3090 at PCIe 4.0 x4 will hurt training throughput, but it will not stop you from running larger models.** For inference, VRAM matters far more than PCIe bandwidth.
