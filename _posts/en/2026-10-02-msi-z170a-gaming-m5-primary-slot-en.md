---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI Z170A Gaming M5 Primary Slot
translated: false
type: note
---

Question: Which of the three PCIe x16-length slots on the MSI Z170A Gaming M5 is the primary GPU slot?

Answer: On the **MSI Z170A Gaming M5**, the primary GPU slot is **PCI_E1** — the **top PCIe x16-length slot, physically closest to the CPU socket**.

Typical layout:

```text
CPU
┌─────────────────────────┐
│                         │
└─────────────────────────┘

PCI_E1  █████████████████  ← PRIMARY GPU, CPU-connected x16
PCI_E2  █████████████████  ← secondary
PCI_E3  █████████████████  ← lower slot
```

For your **M40/P100 troubleshooting**, put the card in **PCI_E1 first**.

Also, don't judge by physical length alone. The board has three x16-length slots, but their electrical lane configurations differ. On Z170, the top slot is the one you want for a single GPU.

If you're getting **“Insufficient PCI Resources Detected” even with the M40 in PCI_E1**, the next thing I'd investigate is the exact **lane/resource configuration of PCI_E1/E2/E3 + Above 4G + CSM**.