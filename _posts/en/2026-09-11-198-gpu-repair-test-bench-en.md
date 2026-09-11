---
audio: false
generated: true
image: false
lang: en
layout: post
title: ¥198 GPU Repair Test Bench
translated: false
type: note
---

Question: What is this ¥198 used PC, and is it a good deal for your GPU-repair/test bench?

Answer:

This is a **very old but usable AMD FM2+ office/test machine**. At **¥198**, it can actually make sense for your GPU-repair setup.

| Part        | Details                               | Assessment                              |
| ----------- | ------------------------------------- | --------------------------------------- |
| CPU         | AMD **Athlon X4 850**, 4C/4T, 3.2 GHz | Old, but adequate for testing           |
| Motherboard | ASUS **A68HM-E**                      | FM2+/A68 chipset                        |
| RAM         | 8 GB DDR3, 2×4 GB                     | Fine                                    |
| SSD         | WD 120 GB                             | Fine for OS/tools                       |
| HDD         | 500 GB                                | Useful for test software/storage        |
| GPU         | Colorful **GT 210**                   | Very weak, but useful as a display card |
| OS          | Windows 10 Pro                        | Convenient for old GPU tools            |
| Price       | **¥198**                              | Cheap                                   |

### The interesting part: the motherboard

The **ASUS A68HM-E** is an entry-level micro-ATX FM2+ board.

The X4 850 is an **AMD Kaveri-family CPU**, so unlike many Intel CPUs, the system's video output situation depends on the exact CPU/APU configuration. The X4 850 itself is **not an APU with integrated graphics**, so the included GT 210 is important for getting display output.

Conceptually:

```text
PSU
 │
 ├── A68HM-E motherboard
 │     ├── Athlon X4 850
 │     ├── DDR3 4G
 │     ├── DDR3 4G
 │     └── PCIe x16
 │            └── GT 210
 │
 ├── 120G SSD → Windows
 └── 500G HDD → storage
```

### For your GPU-repair bench

I'd actually rate the machine **better as a cheap diagnostic host than as a normal PC**.

The important thing is that you can remove the GT 210 and use the PCIe x16 slot for a GPU under test:

```text
A68HM-E
   │
   └── PCIe x16
          │
          ├── GT 210          ← current display GPU
          │
          └── GPU under test  ← 3060 / 3090 / etc.
```

However, there is one major issue:

**The motherboard only has one PCIe x16 slot.**

So if you want to test a GPU that has no display output, you don't have a second x16 GPU available to provide display.

For **MATS/MODS-style GPU testing**, this machine can still be useful, but I'd prefer a platform with:

* PCIe x16 slot
* another PCIe slot for a display GPU
* cheap CPU
* 8–16 GB RAM
* reliable PSU
* easy CMOS/BIOS access

### ¥198 verdict

**For ¥198: yes, potentially worth buying.**

You're basically paying ¥198 for:

> CPU + motherboard + 8 GB DDR3 + SSD + HDD + case + GT 210

Even if the HDD/SSD is nearly worthless, the **motherboard + CPU + RAM + case + GT 210** can be useful for experimentation.

For your current goal of learning **GPU repair**, I'd rather spend ¥198 on this than ¥500–800 on a modern office PC that you don't care about opening up.

The thing I'd inspect before buying is **the PSU**. The listing doesn't mention it, and a questionable PSU is not what you want when testing expensive 3090/4090-class cards.

I can also evaluate whether this ¥198 machine is a better GPU-repair bench than the B75/X99/B250 machines you've been looking at.
