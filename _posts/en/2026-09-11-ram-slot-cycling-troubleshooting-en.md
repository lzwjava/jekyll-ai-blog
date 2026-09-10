---
audio: false
generated: true
image: false
lang: en
layout: post
title: RAM Slot Cycling Troubleshooting
translated: false
type: note
---

Question: One RAM slot causes CPU↔DRAM cycling, while another slot stays on DRAM. What should you do next?

Answer: Based on the diagnostic pattern you've described, here is a structured approach to isolate whether the fault lies in the RAM stick, the slot, or the CPU socket.

---

## Step 1 — Systematic Slot × Stick Matrix

Run every combination and log the result:

| Stick | Slot A | Slot B |
|---|---|---|
| Current stick (GAMER II) | CPU↔DRAM cycle | DRAM stays lit |
| Known-good DDR4 stick | ? | ? |

This is the single most important experiment. If a second DDR4 stick reproduces the exact same pattern (same slot behaves differently), the fault points strongly away from the RAM and toward the **slot, trace, or CPU memory controller**.

---

## Step 2 — Inspect the LGA1151 Socket

The i5-6500's memory controller lives inside the CPU. A bent or tilted pin in the LGA1151 socket can cause DRAM initialization to fail or stall at different phases depending on which channel is active.

```
LGA1151 socket pins
        ↓
CPU integrated memory controller (IMC)
        ↓
DDR4 Channel A / Channel B
```

**How to check:**
- Power off, unplug PSU, ground yourself
- Remove cooler and CPU
- Inspect socket under bright light or magnification (a phone macro lens works)
- Look for any pin that sits at a different angle than its neighbors — even 1 pin can kill a channel

---

## Step 3 — Rule Out CMOS / Overclock Residue

Before anything else (costs nothing):

```
1. Power off + unplug PSU
2. Remove CMOS battery for ~60 seconds
3. Reinstall battery, plug in, attempt POST with one stick
```

A stale XMP profile or a previous overclock saved in BIOS can cause the memory controller to attempt out-of-spec timings and stall.

---

## Step 4 — Interpret the LED Behavior Carefully

| Observation | What it likely means |
|---|---|
| CPU↔DRAM cycling | POST is reaching memory init, failing, and retrying |
| DRAM LED stays lit | POST is stalling during memory training — potentially a harder failure |

The slot where the LED **stays on DRAM is not necessarily the "good" slot** — it may simply be failing at a different (later or harder) stage of memory initialization.

---

## Summary Decision Tree

```
Both sticks fail identically in both slots?
    → Suspect CPU socket pins or IMC damage

One stick passes in one slot?
    → Suspect the failing stick or a slot trace fault

CMOS clear fixes it?
    → Was a BIOS/XMP config issue all along
```

A photo of the RAM slots and LGA1151 socket (with CPU removed) would allow visual inspection of pin condition if you want to continue narrowing this down.