---
audio: false
generated: true
image: false
lang: en
layout: post
title: No-Display GPU Diagnostic Workflow
translated: false
type: note
---

Yes — partially. This manual is mainly a **VRAM (显存) testing manual** (MODS/MATS for NVIDIA, AMD test programs), but it *does* have a specific workflow for a GPU that won't display (点不亮). Here's what it offers and where it stops helping:

## ✅ What the manual covers for a "no display" GPU

**Use the motherboard's integrated graphics (iGPU) to test the dead discrete GPU** — Section 6, N-card steps 11–21:

1. Connect your monitor to the **motherboard's video output** instead of the GPU.
2. Enter BIOS (e.g., ASUS H170 PRO: F7 → Advanced → System Agent → Graphics Configuration → **Primary Display = CPU Graphics**), F10 to save.
3. Boot into the test environment and pick the right version directory, e.g. `cd 400.250`.
4. **Set up the test environment first** (mandatory for a card with no display):
   ```
   ./mods gputest.js -skip_rm_state_init -notest
   ```
5. **Key diagnostic point:** if you see a **PASS screen**, the card can at least run the test program → continue with:
   ```
   ./mats -n 1 -e 5
   ```
   then check results with `less report.txt` (FBI0A0 = VRAM; `0.0.0` = OK, nonzero numbers = failing memory chip).
6. If **no PASS screen** appears → the manual states this means a **hardware fault (power delivery or GPU core problem)**, and the software **cannot test it at all**.
7. It even gives a follow-up command to distinguish **core vs. VRAM failure**: `./mods gputest.js -oqa -test 118 -matsinfo` (fault code 690 = VRAM fault).

## ⚠️ Requirements / limitations for this scenario

- **CPU must have integrated graphics**, and the motherboard must support **Multi-GPU** (manual recommends ASUS B85/B150/H170).
- **RAM ≥ VRAM** of the card being tested (e.g., 8 GB RAM for an 8 GB card).
- Must boot in **legacy mode** ideally (UEFI only works for NVIDIA cards).
- If the card's core/power circuitry is completely dead (step 4 never shows PASS), the manual explicitly says **the software is useless** — that becomes a hands-on repair job (check power rails, core) beyond the scope of this document.
- The manual targets **VRAM faults** primarily — a card that's 点不亮 due to core damage can only be *detected* (no PASS), not diagnosed further by this toolset.

**Bottom line:** Yes, the manual directly addresses 点不亮 cards — via iGPU-based testing, it helps you determine whether the card is testable, whether the fault is VRAM vs. core, and which memory chip is bad. But if the GPU core or power stage is dead, it can only tell you that much.
