---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS Chip Pin 8 Voltage Check
translated: false
type: note
---

Marked it. The image is saved at:

```
/mnt/data/gpu-diagonalize/keyframes/t_31.25s_bios_marked.jpg
```

## What's drawn on it

- 🟩 **Green box** = the BIOS/SPI flash chip (small 8-pin SOIC, near the PCIe gold fingers)
- 🟨 **Yellow dot** = **Pin 1** (the dot corner — pins count counter-clockwise from here)
- 🟥 **Red dot** = **Pin 8** = **VCC** ← *this is where you measure 3.3V*
- 🔍 **Zoomed inset** in the top-right corner so you can verify it's the right chip

## How to measure

1. Multimeter → **20V DC**
2. **Black probe** → ground (mounting hole / metal bracket)
3. **Red probe** → **Pin 8** (red dot)
4. Expect **3.3 V**

## ⚠️ One thing to verify

The AI placed the chip near the top of the PCIe gold fingers (the key notch area) at roughly `x=480, y=1000`. Please check the **zoom inset** — the BIOS chip should be a small square IC with **8 legs** and usually a label like `25Q…`, `MX25…`, or `W25…`.

- If the green box is on the right chip ✅ → probe the red dot and tell me the voltage.
- If it's off → tell me what's actually in the inset (or point me to roughly where the chip is: "closer to the gold fingers", "further left/right", etc.) and I'll re-place it.

What does Pin 8 read?