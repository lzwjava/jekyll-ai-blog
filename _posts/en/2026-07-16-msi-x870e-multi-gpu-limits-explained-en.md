---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI X870E Multi-GPU Limits Explained
translated: false
type: note
---

**Question: MSI X870E board — how many RTX 4070-class GPUs can I plug in?**

**Answer:**

MSI X870E is a very high-end AM5 motherboard platform (Ryzen 7000/8000/9000). It is good, but it is **not a multi-GPU AI workstation board** like server boards. ([MSI USA][1])

Typical MSI X870E layout:

```
CPU (Ryzen 9000)
 |
 +-- PCIe 5.0 x16  ---> GPU #1 (RTX 4070)
 |
 +-- PCIe 5.0 x4/x8 ---> GPU #2 (depends on model)
 |
 +-- PCIe 4.0 x4 ---> GPU #3 (possible, but slower)
```

For example, MSI MPG X870E Carbon has:

* PCIe 5.0 x16 primary slot
* PCIe 5.0 secondary slot (bandwidth sharing)
* PCIe 4.0 x4 third slot ([MSI USA][1])

So physically:

* **1 × RTX 4070** → perfect
* **2 × RTX 4070** → possible
* **3 × RTX 4070** → possible on some models, but not ideal
* **4 × RTX 4070** → practically no (slot space + PCIe lanes + power limitations)

([MSI][2])

For AI workloads:

### 1 GPU

```
RTX 4070 12GB
PCIe 5.0 x16
```

Excellent.

### 2 GPUs

Example:

```
RTX 4070 12GB
RTX 4070 12GB

Total VRAM:
24GB
```

But no NVLink, so PyTorch distributed training uses PCIe communication.

### 3 GPUs

```
RTX 4070
RTX 4070
RTX 4070
=
36GB VRAM
```

Possible, but:

* third card only PCIe x4
* physical cooling becomes difficult
* motherboard lanes become bottleneck

### Better AI build

For LLM experiments, I would not choose X870E. I would choose:

```
Used workstation/server board:

Threadripper Pro
EPYC
Xeon W
```

because you get:

```
PCIe lanes:

CPU
 |
 +-- GPU x16
 +-- GPU x16
 +-- GPU x16
 +-- GPU x16
```

Example:

```
4 × RTX 3090 24GB

= 96GB VRAM
```

which is much more interesting for local LLM.

X870E is more like:

```
Ryzen 9950X
+
RTX 5090 / RTX 4090
+
fast NVMe
+
gaming + AI workstation
```

not:

```
4 GPU training machine
```

For your use case (GPT training, ROCm experiments, local LLM), I would rank:

```
EPYC / Threadripper Pro  >>>  X870E  >>>  normal B650/B760
```

X870E is a great enthusiast board, but the AM5 platform simply does not have enough PCIe lanes for a serious multi-GPU lab. ([MSI][2])

References:

* MSI PCIe lane sharing explanation ([MSI][2])
* MSI MPG X870E Carbon specifications ([MSI USA][1])
* MSI PRO X870E-P specifications ([MSI USA][3])

[1]: https://us.msi.com/Motherboard/MPG-X870E-CARBON-WIFI/Specification?utm_source=chatgpt.com "MPG X870E CARBON WIFI | Gaming Motherboards｜Best Motherboard for AI PC｜MSI"
[2]: https://www.msi.com/blog/pcie-lane-bifurcation-and-bandwidth-sharing-on-msi-x870e-x870-motherboards?utm_source=chatgpt.com "PCIe Lane Bifurcation and Bandwidth Sharing on MSI X870E / X870 Motherboards"
[3]: https://us.msi.com/Motherboard/PRO-X870E-P-WIFI/Specification?utm_source=chatgpt.com "PRO X870E-P WIFI | PRO Series Motherboards｜Best Motherboard for AI PC｜MSI"
