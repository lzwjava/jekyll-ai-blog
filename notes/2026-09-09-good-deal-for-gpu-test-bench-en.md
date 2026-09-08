---
audio: false
generated: true
image: false
lang: en
layout: post
title: Good Deal for GPU Test Bench
translated: false
type: note
---

Question: How good is the **MSI B150M PRO-VH + i5-6500 for ¥200**?

Answer: **Good deal. I'd take it for a GPU test bench.**

The **MSI B150M PRO-VH** is a basic but perfectly suitable LGA1151 board:

* **CPU:** i5-6500 — 4C/4T, 3.2–3.6 GHz
* **Socket:** LGA1151
* **Chipset:** B150
* **RAM:** DDR4, typically 2 DIMM slots, up to 32 GB
* **GPU:** PCIe 3.0 x16
* **CPU iGPU:** Intel HD Graphics 530
* **Form factor:** Micro-ATX
* **No CPU overclocking** — irrelevant for your use

For **GPU repair/testing**, I'd rank it:

**B150M PRO-VH + i5-6500 @ ¥200 → 8.5/10**

The important thing is that you get a **known-working CPU + motherboard platform for only ¥200**, rather than buying a random motherboard and CPU separately.

For your use case:

```text
B150M PRO-VH
      │
 i5-6500 + HD 530
      │
   PCIe x16
      │
 ┌────┴─────┐
 │ GPU DUT  │  ← 4090 / 5090 / etc.
 └──────────┘
```

One limitation: **only one x16-length PCIe slot** is useful for GPU testing, so this isn't a good multi-GPU platform. But for **testing one GPU at a time**, that's actually ideal.

I'd choose this over an old B85/i5-4xxx setup if the prices are similar because **DDR4 + newer Skylake platform** gives you a bit more flexibility.

If you have the listing photo, send it and I can check the **exact PCB revision, socket pins, PCIe slot condition, and whether anything looks repaired**.
