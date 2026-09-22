---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Test Point Guide
translated: false
type: note
---

Done. I've marked the test points on `gpu1_marked.jpg` (in `/mnt/data/gpu-diagonalize/`).

## ⚠️ Important caveat

The AI's pixel-level placement isn't perfectly reliable on a busy board photo, so **treat the markers as approximate** and confirm by eye using the descriptions below. The legend on the image numbers them 1–7.

## The 7 marked points & how to recognize them

| # | Test point | How to find it | What to measure |
|---|-----------|----------------|-----------------|
| **1** | **8-pin PCIe power** | Black block socket on the card's edge — the cable plugs here | 12V (already OK ✅) |
| **2** | **BIOS / SPI flash chip** | Tiny 8-pin square chip near the **PCIe gold fingers** (the row of gold contacts that go into the motherboard slot). Often labelled `25Q…` / `MX25…` / `W25…`. **Pin 8** = its VCC | 3.3V |
| **3** | **5V buck output** | Small grey coil (inductor) near the **video output bracket** (where HDMI/DP ports are) | 5V |
| **4** | **3.3V test point** | A pad/via near the BIOS chip | 3.3V |
| **5** | **Fan header** | Small 4-pin white/black connector | 12V or 5V (sanity) |
| **6** | **VCore inductor** | The row of grey coils **closest around the GPU die** (under the thermal paste) | VCore (expect 0.6–1.1V when running) |
| **7** | **Ground** | Any **plated mounting hole** (no component in it) | reference for black probe |

## Your next measurement (after 12V ✅)

1. **Black probe** → point **7** (mounting hole / ground)
2. **Red probe** → point **2** (BIOS chip, pin 8) → expect **3.3 V**
3. **Red probe** → point **3** (5V inductor) → expect **5.0 V**

Report those two numbers and we'll continue to **1.8V → VMEM → VCore**.

If the marked image looks off when you open it, tell me which number is wrong and I'll re-place it — or just send a zoomed/cropped photo of the area and I'll pinpoint it exactly.