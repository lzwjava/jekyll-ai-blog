---
audio: false
generated: true
image: false
lang: en
layout: post
title: X99-A Motherboard Legacy PCI Check
translated: false
type: note
---

**Question:** Does an X99-A motherboard have PCI?

**Answer:** Usually **no legacy PCI slot**.

Most ASUS X99-A boards have:

* **PCIe x16** slots — for GPUs
* **PCIe x1** slots — for smaller cards
* **No old PCI (32-bit, 33 MHz) slot**

The important distinction is:

```text
Old PCI:
[ PCI ]       ← legacy parallel PCI

PCI Express:
[ PCIe x1 ]
[ PCIe x16 ]  ← GPU
```

So if you're asking because you want to use an **old PCI diagnostic/test card**, X99-A generally isn't a good choice. For GPU repair/testing, an **H81/B85/Z97-era board** is often more useful because some models still have legacy PCI.

If you mean a specific **ASUS X99-A revision**, send me a photo of the motherboard and I can identify every expansion slot.
