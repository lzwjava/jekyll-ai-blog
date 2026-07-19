---
audio: false
generated: true
image: false
lang: en
layout: post
title: PCIe 4.0 x4 Explained
translated: false
type: note
---

Question: What does PCIe 4.0 x4 mean on a motherboard? Does the "x4" mean four PCIe 4.0 ports?

Answer:

No. **"x4" does not mean four PCIe ports.** It means **four PCIe lanes**.

PCIe naming has two parts:

```
PCIe 4.0 x4
│       │
│       └── number of lanes
└────────── generation / speed
```

* **PCIe 4.0** = generation 4, each lane is about **2 GB/s per direction**
* **x4** = the device uses **4 lanes**

So:

```
PCIe 4.0 x4
= 4 PCIe 4.0 lanes
= ~8 GB/s bandwidth each direction
```

A physical PCIe slot can have different lane sizes:

```
Physical slot size:

[x1]       one lane
[x4]       four lanes
[x8]       eight lanes
[x16]      sixteen lanes
```

A motherboard may look like this:

```
CPU PCIe lanes:

PCIe x16 slot
====================  GPU
████████████████

PCIe x4 slot
========          NVMe adapter / network card

M.2 slot
========          NVMe SSD (PCIe 4.0 x4)
```

The important point:

**The connector size and electrical lanes are different.**

Example:

A long GPU slot:

```
PCIe x16 physical slot
████████████████████
```

may actually run as:

```
PCIe 4.0 x16
or
PCIe 4.0 x8
or
PCIe 4.0 x4
```

depending on motherboard wiring.

---

For M.2 SSDs, you often see:

```
M.2 NVMe:
PCIe 4.0 x4
```

This means:

* SSD connects through PCIe generation 4
* SSD gets 4 lanes
* not four separate connectors

Typical speed:

```
PCIe 4.0 x1  ≈ 2 GB/s
PCIe 4.0 x4  ≈ 8 GB/s

Samsung 990 Pro:
~7.4 GB/s
```

---

For your GPU use case (multiple RTX 3090/4070):

A motherboard spec might say:

```
2 × PCIe x16 slots

Slot 1:
PCIe 5.0 x16

Slot 2:
PCIe 4.0 x4
```

It means:

```
GPU #1:
16 lanes

GPU #2:
only 4 lanes
```

The second GPU will work, but bandwidth is much lower.

For AI inference/training, this matters:

* LLM inference with model split across GPUs → PCIe bandwidth matters
* independent jobs on each GPU → less important
* NVLink (3090 only) can bypass some PCIe limitations

For dual RTX 3090, ideally look for:

```
PCIe x16 slot 1: x16
PCIe x16 slot 2: x16 or x8
```

not:

```
x16 + x4
```

because the second 3090 becomes bandwidth constrained.
