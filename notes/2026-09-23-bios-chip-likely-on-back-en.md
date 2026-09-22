---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS chip likely on back
translated: false
type: note
---

I tried GLM, Qwen, and Gemini via OpenRouter on this frame. They all agree on one thing: **the BIOS chip is not clearly visible in this particular frame.** Here's the honest summary:

## Multi-vendor result

| Vendor | Model | What it said |
| -------- | ------- | -------------- |
| **Zhipu GLM** | `glm-4.6v` | PCIe gold fingers on **left edge**; BIOS chip "just above the gold fingers" — but when I cropped that spot, it said **no chip there** |
| **Alibaba Qwen** | `qwen3.8-flash` | Crop shows blurry surface, **no BIOS chip** |
| **Zhipu GLM** | `glm-5v-turbo` | Same — **no 8-pin SOIC in the crop** |
| **Google Gemini** | `gemini-3.8-flash` | Blocked (provider ToS 403) |

The models keep contradicting themselves on exact location because this frame is **too blurry / the chip is either hidden by the hand or on the back of the board**.

## Where the BIOS chip actually is

On NVIDIA cards the BIOS/flash chip is **almost always on the back of the PCB**, near the **PCIe gold fingers**, next to the **key notch** (the gap in the gold fingers). This frame shows the **front** of the card — so it may simply not be visible.

## What to do

1. **Flip the card over** (back side), look near the gold finger notch for a tiny 8-pin square chip labelled `25Q…` / `MX25…` / `W25…` / `Pm25…`.
2. On that chip: **pin 1 = dot corner**, count counter-clockwise → **pin 8 = opposite corner = VCC**.
3. Measure pin 8 to ground → expect **3.3 V**.

## Easier alternative — skip the BIOS chip

You can check 3.3V and 5V at easier points:

- **3.3V / 12V from the PCIe slot itself:**
  - Pin **B1/B2/B3** (12V), Pin **A9/A10** (3.3V) — on the gold fingers
- **5V** → the small **grey inductor** near the **video output bracket** (top edge of the card)

---

If you want me to mark these instead, just say which and I'll mark them on the image — or send a photo of the **back** of the card and I'll pinpoint the BIOS chip exactly.
