---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Repair Test Bench Build Guide
translated: false
type: note
---

## Question

The manual recommends ASUS B85/H170/B150, but it was revised around 2021. What would I recommend **today for a dedicated GPU repair/testing bench**?

## Answer

Yes — I would **not blindly build around B85 today**.

The important thing in the manual is not really "B85." The real requirements are:

1. **Legacy/CSM boot**
2. **Integrated graphics**
3. **iGPU + dGPU simultaneously**
4. **Enough RAM**
5. **Reliable PCIe slot**
6. Cheap, replaceable hardware

The manual explicitly says the purpose of the iGPU is to let you test a dGPU that produces **no display output**, by connecting the monitor to the motherboard and selecting CPU Graphics in BIOS.

### What I'd build in 2026

I'd go for **two generations**, rather than trying to find the "perfect" old ASUS board.

| Platform                | My rating | Why                                                         |
| ----------------------- | --------: | ----------------------------------------------------------- |
| **B85 + i5-4460**       |      ⭐⭐⭐⭐ | Extremely cheap, proven by your manual                      |
| **B150/H170 + i5-6500** |     ⭐⭐⭐⭐⭐ | Probably my favorite cheap legacy test bench                |
| **B250 + i5-7500**      |     ⭐⭐⭐⭐⭐ | Newer, cheap, good compatibility                            |
| **H310/B360 + i5-8500** |      ⭐⭐⭐⭐ | Newer, but legacy/CSM behavior becomes more board-dependent |
| **B550 + Ryzen APU**    |       ⭐⭐⭐ | Modern, but not ideal for old DOS/MATS workflows            |
| **X99 + Xeon E5**       |       ⭐⭐⭐ | Powerful, but lacks the iGPU workflow                       |

**My first choice: B150/H170 + i5-6500/6600 + 16 GB DDR4.**

Why?

The manual itself groups **B85, B150 and H170** together as boards it verified as stable.

But B150/H170 gives you a much nicer middle ground than B85:

* DDR4
* Skylake
* i5-6500 is extremely cheap used
* Intel HD 530
* PCIe x16
* SATA
* UEFI + legacy compatibility
* much newer than Haswell
* still old/simple enough for weird GPU repair software

### The architecture I would use

Something like:

```text
             ┌─────────────────────┐
             │   i5-6500           │
             │   Intel HD 530      │
             └──────────┬──────────┘
                        │
                   motherboard
                        │
              ┌─────────┴─────────┐
              │                   │
          iGPU output          PCIe x16
              │                   │
           Monitor             GPU under test
                                  │
                            RTX 3090 / 4090
                            RX 580 / 6800
                            etc.
```

This is much more useful for repair than simply having a powerful CPU.

If the GPU is completely dead:

```text
GPU under test
      │
      ├── PCIe power
      ├── PCIe slot
      │
      X── no video output

Motherboard iGPU
      │
      └── Monitor
```

You can still boot Linux and run the diagnostic program against the PCIe GPU.

That's exactly the workflow described in the manual.

---

## One thing I would change from the manual

I **wouldn't bother with a 250 GB SSD specifically**.

The manual says 250 GB+ and recommends SATA SSDs, largely because its image is partitioned into multiple MBR partitions.

Today I'd simply use:

```text
120 GB / 240 GB SATA SSD
        +
USB flash drive
        +
separate modern Linux SSD if needed
```

Storage isn't the bottleneck.

The **real bottleneck is compatibility with the old MATS/MODS environment**.

---

# More importantly: don't make this your only test machine

For your GPU-repair work, I'd actually build a **two-machine lab**.

### Bench A — legacy diagnostic machine

```text
B150/H170
i5-6500
16 GB DDR4
120/240 GB SATA SSD
Intel iGPU
PCIe x16
```

Purpose:

```text
MATS/MODS
old NVIDIA
old AMD
dead-display GPUs
VRAM diagnosis
BIOS/firmware work
```

The manual's MATS workflow is specifically oriented toward identifying VRAM failures and even mapping error channels to physical memory chips.

### Bench B — modern GPU machine

Your newer machine:

```text
modern CPU
RTX 4070 / whatever modern GPU
64 GB+ RAM
NVMe
modern UEFI
```

Purpose:

```text
RTX 30
RTX 40
RTX 50
modern AMD
GPU-Z
CUDA
Linux
Windows
stress testing
vBIOS tools
driver testing
```

This distinction matters because **the old MATS/MODS environment is not the same thing as a modern GPU validation environment**.

---

# And there's a bigger problem with this manual

The manual itself says:

> N cards: RTX 3090 and below

and its AMD documentation goes through RX 6000/RX 5000-era hardware.

So I would treat it as a **legacy repair manual**, not a complete 2026 GPU-testing methodology.

For example:

```text
GTX 1080
RTX 2080
RTX 3090
RX 580
RX 5700
RX 6900
        ↓
excellent use case for this manual
```

but:

```text
RTX 4090
RTX 4080
RTX 5090
RTX PRO 6000 Blackwell
RX 7900 XTX
newer Blackwell GPUs
        ↓
don't assume MATS/MODS from this image is sufficient
```

You need a modern diagnostic stack as well.

---

## My actual recommendation for you

Given that you're buying cheap second-hand hardware specifically for **GPU repair**, I would hunt Xianyu for:

```text
ASUS B150 / H170
        +
i5-6500 / i5-6600
        +
16 GB DDR4
```

Don't pay a premium for ASUS specifically if another reputable B150/H170 board has:

```text
Intel iGPU
PCIe x16
CSM/Legacy support
```

But **ASUS is still a very good choice for this particular manual**, because the author explicitly validated ASUS B85/B150/H170 rather than merely recommending the chipset in theory.

### Target used-market price

I'd roughly think:

```text
B150/H170 motherboard     ¥80–150
i5-6500                   ¥30–60
16 GB DDR4                ¥50–80
240 GB SATA SSD           ¥30–50
cheap PSU                 ¥50–100
case                      optional

Total                    ~¥240–440
```

At that price, **I'd absolutely build it**.

And keep your X99 machine. Don't replace it.

The ideal repair bench becomes:

```text
                 GPU REPAIR LAB
                       │
             ┌─────────┴─────────┐
             │                   │
       Legacy bench         Modern bench
       B150/H170            X99 / newer
       i5-6500              powerful CPU
       Intel iGPU           modern GPU
             │                   │
       MATS/MODS              modern tests
       dead GPU              stress/driver
       VRAM diagnosis        CUDA/GPU-Z
```

**That's considerably more robust than buying a B85 simply because the manual says B85.**
