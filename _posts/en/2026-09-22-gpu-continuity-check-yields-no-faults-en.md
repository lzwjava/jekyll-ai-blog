---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Continuity Check Yields No Faults
translated: false
type: note
---

Here's the analysis of `IMG_2506.MOV` (no more scripting — just reading the report the analysis already produced):

## Video profile
- **39.6 s**, 4K (3840×2160) HEVC + AAC audio, 125 MB
- Board is **disassembled** (cooler off, thermal paste on the die)
- The AI identified the die as **GA104** → this is an **RTX 3060 Ti / 3070 / 3070 Ti** class card

## What the meter actually showed (in sequence)

| Frame | Reading | Mode | Where |
|-------|---------|------|-------|
| 1 | **1.800** on 200 kΩ range → **1.8 kΩ** | Resistance | Near-core VRM area, lower-left of GPU package |
| 2 | **00.0 Ω** | Resistance | Bottom PCB edge, small component near GPU |
| 3 | **0.0** | Continuity/diode | Core/memory VRM area near PCIe edge |
| 4 | **0.000 Ω** | Continuity | Near 4-pin fan header |
| 5 | **0.00 V** | DC voltage | Fan-header area |
| 6 | **"1" (out-of-range / OL)** | Resistance | Test pad/via near fan/power header |
| 7–9 | display unreadable | DC/diode | Near 8-pin PCIe input |

## Visual inspection
Across all frames the model reported:
- ✅ **No burn marks, bulged/leaking caps, cracked MOSFETs/ICs, broken traces, lifted pads, or corrosion**
- ⚠️ Heavy **dried thermal paste residue** on the die and substrate — flagged as disassembly residue, not damage
- ⚠️ Yellow patches near display outputs — judged as tape/label adhesive, not burn

## Audio
- Dominant signal ~220 Hz, classification: **speech/noise (narration)** — your voice talking through the process
- **0 beep codes / 0 continuity beeps detected** — the meter never beeped during the recording

## Honest interpretation

**1. This is a continuity/resistance probing session, not a powered rail check.** Only one DC-voltage reading appeared (0.00 V), which is expected on an unpowered, disassembled board.

**2. The 0.0 Ω readings are ground-connected points.** On continuity mode, 0.0 Ω means the probe point is tied to the ground plane — *normal for ground pads/vias*. It would only be a fault if you were probing a rail that's *supposed* to be isolated from ground (i.e., a dead short on 12V/VCore/VMEM). To judge that, I'd need to know which exact point each 0.0 Ω reading was on.

**3. The 1.8 kΩ reading is not a short.** It's a low-ish resistance to ground (could be a cap/resistor path) but nothing alarming on its own.

**4. The "1" (OL) reading = open circuit.** Expected for some nodes; a fault only if that node should have continuity.

**5. No visible physical damage.** Nothing looks burned or blown in any frame.

## Bottom line
From this video alone, there's **no evidence of a board-level fault** — no shorts to ground on rails (that we can confirm), no visible damage, no POST beep codes. The video is mostly continuity checks on a clean-looking board. The main limitation is that **the multimeter display was unreadable in the last 3 frames**, and the probe points weren't labeled.

**To get a real diagnosis, I'd need you to tell me:** which specific points each reading was on, and the symptom (no display? artifacts? no power?) — plus ideally repeat the probe with the display fully in frame. If you want, send those point labels/symptom and I'll cross-reference the readings against the GA104 power rails (12V, 5V, 1.8V, VDDCI, VDDC, VMEM).