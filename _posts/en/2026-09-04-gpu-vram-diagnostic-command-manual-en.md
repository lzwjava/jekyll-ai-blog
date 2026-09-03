---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU VRAM Diagnostic Command Manual
translated: false
type: note
---

## Question: What is this PDF?

Answer: **`显卡测试命令手册.pdf` is a GPU VRAM diagnostic/testing manual**. It describes a bootable multi-system test environment used by GPU repair technicians to diagnose **NVIDIA and AMD graphics cards**, especially memory (VRAM) faults.

The manual is essentially a **MATS/Tserver repair technician's command reference**.

### What it does

The core idea is:

```text
GPU
 │
 ├── GPU core
 │
 ├── VRAM chips ──┐
 │                 │
 └── VRAM bus ─────┘
        ↓
     MATS / Tserver
        ↓
   memory test
        ↓
   PASS / FAIL
        ↓
 identify bad VRAM channel
        ↓
 locate physical VRAM chip
```

For NVIDIA, the important program is **MATS**:

```bash
./mats -e 10
```

`-e 10` means test **10 MB of VRAM** according to the manual.

For a GPU that **doesn't output display**, the manual shows using the motherboard's iGPU to boot the machine while testing the discrete GPU:

```text
Monitor
   │
   ▼
Motherboard HDMI/DP
   │
   ▼
Intel iGPU
   │
   ├────────── system
   │
   └── PCIe ── broken NVIDIA GPU
                    │
                    ▼
                  MATS
```

The manual explicitly recommends a motherboard capable of Multi-GPU/iGPU operation for this situation.

### The interesting part for GPU repair

It doesn't merely say **"VRAM bad."**

It attempts to tell you **which memory channel / byte lane is failing**, and then maps that result to the physical VRAM chip.

For example:

```text
report.txt

FBI0A0
A0 = 31760 errors
```

The manual's example interprets this as a low-byte VRAM problem and then maps it to a particular physical memory position on the card.

It also gives the physical mapping rules:

```text
NVIDIA — VRAM on both sides

Side A → high byte → bits 32–63
Side B → low byte  → bits 0–31
```

and another arrangement for cards with VRAM on only one side.

That's **very useful for the repair workflow you're learning**:

```text
GPU doesn't work
       ↓
Can MATS initialize?
       ↓
    YES
       ↓
Run VRAM test
       ↓
   PASS / FAIL
       ↓
FAIL → identify channel
       ↓
map channel → physical VRAM
       ↓
inspect VRAM / soldering / power / traces
       ↓
possibly reball / replace VRAM
```

### It covers both NVIDIA and AMD

The document has separate environments:

| Vendor    | Tool                     | Example                      |
| --------- | ------------------------ | ---------------------------- |
| NVIDIA    | `mats` / `mods`          | `./mats -e 10`               |
| AMD older | individual test programs | `./rx580a6`                  |
| AMD newer | `tserver`                | `./tserver -boardtest=memfa` |

For newer AMD cards, the result is stored in `memfa.log`.

### One important limitation

This is **not a universal PCIe diagnostic tool** like plugging a car scanner into a car.

MATS/Tserver works at a much deeper level, but it still needs the GPU to reach a sufficiently functional state.

The manual specifically says that if the test environment itself cannot initialize, possible causes include **abnormal power delivery or GPU-core problems**, meaning you may not even reach the VRAM test stage.

So conceptually you can think of the repair hierarchy as:

```text
             GPU
              │
       ┌──────┴──────┐
       │             │
   Power/VRM      Initialization
       │             │
       └──────┬──────┘
              ↓
          GPU core
              ↓
       MATS initialization
              ↓
          VRAM test
              ↓
       bad channel / chip
```

**For the GPU repair work you've been exploring, this PDF is quite relevant.** The most valuable sections for you are pages **5–18**, because they show the actual `mods`, `mats`, `report.txt`, channel mapping, and the additional test used to distinguish **VRAM fault vs GPU-core fault**.
