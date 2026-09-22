---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU BIOS Chip VCC Measurement
translated: false
type: note
---

Marked it. The file is at:

```
/mnt/data/gpu-diagonalize/gpu_back_marked.png
```

## What's on the image

- 🟩 **Green box** = the **BIOS/flash chip** — GLM read its label as **W25Q64** (Winbond 64Mbit SPI flash, standard GPU BIOS chip)
- 🟨 **Yellow dot** = **Pin 1** (the dot corner)
- 🟥 **Red dot** = **Pin 8** = **VCC** ← *probe here*
- 🔍 **Zoom inset** (top-right) so you can confirm the chip

## Pin 8 → VCC → measure it

1. Multimeter → **20V DC**
2. **Black probe** → ground (a mounting hole or the metal bracket)
3. **Red probe** → **Pin 8** (red dot)
4. Expected: **3.3 V**

## Notes

- Pins count **counter-clockwise from the dot**: Pin 1 = dot corner → down the left side (2,3,4) → up the right side (5,6,7) → **Pin 8 = top-right = VCC**.
- The chip is on the **back** of the card near the PCIe gold fingers, exactly where it should be.

---

**Report back what Pin 8 reads:**
- **3.3 V** ✅ → the low-voltage rail is fine → we move to **5V** and then **VCore inductor**
- **0 V** ❌ → 3.3V rail is dead → that's your root cause (likely the 3.3V regulator/converter, often fed from the PCIe slot)

If the green box looks slightly off when you open it, tell me and I'll re-place it — but GLM-5v confirmed the W25Q64 label, so it should be right.