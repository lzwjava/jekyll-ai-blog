---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decoding Quadro 410 Memory Chip Labels
translated: false
type: note
---

Good — I now have enough information to give a thorough and accurate answer. Let me compile everything.

---

**Question:** What are the 4 SK Hynix chips on the Quadro 410 labeled M1, M2, M3, M4 — and what do "11C" and "314" mean?

**Answer:**

---

**What the chips are — M1, M2, M3, M4**

The Quadro 410 uses **512 MB of DDR3 SDRAM** across a **64-bit memory bus**. The 4 chips labeled **M1, M2, M3, M4** are the **four individual DDR3 DRAM chips** that together make up that 512 MB of video memory. Each chip contributes **128 MB (1 Gb)**, and together they form the card's full VRAM.

The Quadro 410 has 512 MB DDR3 memory running at 891 MHz.

The PCB reference designators **M1 through M4** are simply the board silk-screen labels for each memory chip's physical location — M standing for "Memory." This is standard GPU PCB naming convention.

The actual part number on these chips is most likely **H5TQ1G83** or **H5TQ2G83** series — SK Hynix chips beginning with H5GC or H5AN typically denote DDR SDRAM (DDR3, DDR4, DDR5), with the letters following "H5" indicating the generation.

---

**What "11C" means**

In SK Hynix's DDR3 part number scheme, the speed/latency suffix encodes the memory's CAS latency and speed grade. The code "PB" maps to DDR3-1600 at CL11 (11-11-11 timings), and "H9" maps to DDR3-1333 at CL9 (9-9-9 timings).

The **"11C"** printed on the chip label refers to the **speed suffix** of the full part number — specifically the **"-PBC"** or **"-11C"** style suffix used in SK Hynix's laser-marked chip top:

- **11** = **CAS Latency 11** (CL11), meaning DDR3-1600 speed grade
- **C** = **Commercial temperature range & normal power** (standard operating conditions)

So "11C" tells you: this chip is rated for **DDR3-1600, CL11, commercial grade**.

---

**What "314" means**

**"314"** is a **date/lot code** printed on the chip, meaning:

- **3** = Year **2013**
- **14** = **Week 14** of that year (approximately April 2013)

This is the standard YYWW (Year + Work Week) manufacturing date code used by SK Hynix and most semiconductor manufacturers. So **314 = manufactured in week 14 of 2013**, which aligns perfectly with the Quadro 410's launch in Q4 2012 and early production run.

---

**Summary table:**

| Item | Meaning |
|---|---|
| **M1, M2, M3, M4** | PCB location names for the 4 DDR3 DRAM chips |
| **4 chips total** | Together = 512 MB VRAM on a 64-bit bus (128 MB each) |
| **Manufacturer** | SK Hynix |
| **11** in "11C" | CAS Latency 11 → DDR3-1600 speed grade |
| **C** in "11C" | Commercial temperature, normal power |
| **314** | Date code: Year 2013, Week 14 (≈ April 2013) |

**References:**
- [SK Hynix DDR3 Part Number Guide — Scribd](https://www.scribd.com/doc/131570956/DDR-memory-list-from-hynix)
- [SK Hynix Graphics Memory Part Number Decoder — Scribd](https://www.scribd.com/document/371607382/Hynix-Graphics-Part-Numbering)
- [Cracking Hynix Chip Labels — SilverPC Blog](https://blog.silverpc.hu/2025/10/20/cracking-the-code-a-guide-to-understanding-hynix-chip-labeling/)
