---
audio: false
generated: true
image: false
lang: en
layout: post
title: Burned RTX 4060 capacitor diagnosis
translated: false
type: note
---

Question: You have an Inno3D RTX 4060 “dead card” with a burned PCB and shorted VRAM, and you’re asking what to do around the capacitor area.

Answer: If you mean **the capacitors near the GPU/VRAM power section**, don't power the card yet. A burned PCB + multiple shorted VRAM rails makes this primarily a **power-rail/PCB diagnosis and donor-board** problem.

If you send me a clear photo of the capacitor area, I can mark what to measure first and identify the likely rail/components.

For now, I'd do:

```text
1. Visual inspection
   ↓
2. Identify burned components / PCB carbonization
   ↓
3. Multimeter resistance to GND
   ↓
4. Determine which rail is shorted
   ↓
5. Check MLCC capacitors around that rail
   ↓
6. Inject low voltage/current-limited power ONLY if the PCB is still viable
```

### If a capacitor itself is shorted

A very common failure mode is an MLCC becoming shorted:

```text
VRM rail ────────┬──── MLCC ─── GND
                 │
                 └──── GPU/VRAM
```

With power **completely disconnected**, measure resistance/diode mode across the capacitor.

But don't immediately conclude:

```text
0 Ω → capacitor is bad
```

because the **GPU or VRAM can itself be the short**.

A useful technique is to compare:

```text
suspect capacitor → GND
nearby identical capacitor → GND
```

and trace which capacitors are connected to the same rail.

### For this particular 4060

If the seller says **“VRAM 1.8V is all shorted”**, that's a major clue. You want to establish whether:

```text
1.8 V rail
   │
   ├── MLCC short
   ├── VRAM chip short
   ├── GPU-side component short
   └── damaged PCB internal short
```

The **burned/charred PCB is the biggest concern**. Once FR-4 is seriously carbonized, it can become electrically conductive between layers, so replacing a capacitor may not fix the underlying problem.

For a first GPU-repair project, I would treat this card as:

**donor/diagnostic board first → repair candidate second.**

I can also help you build a **4060 capacitor/VRAM rail measurement checklist**, starting with exactly which multimeter measurements to make before applying any power.
