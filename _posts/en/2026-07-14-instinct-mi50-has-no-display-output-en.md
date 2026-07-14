---
audio: false
generated: true
image: false
lang: en
layout: post
title: Instinct MI50 Has No Display Output
translated: false
type: note
---

Thanks for the correction—let me address this directly.

The **AMD Radeon Instinct MI50 does not have a Mini‑DisplayPort output** (or any video output). The card you’re probably thinking of is the **AMD Radeon Pro VII**, which looks similar (same Vega 20 GPU, 16 GB HBM2, passively cooled variant) but has **6× Mini‑DisplayPort** connectors and is a professional workstation card. The **Instinct MI50** is strictly a headless datacenter compute accelerator with zero display connectors. That mix-up is very common because they share the same core chip.

You can verify this:

- Official product pages and every teardown/review of the MI50 show no ports on the bracket—just the PCIe power connector and ventilation.
- The MI50 driver stack is compute‑only (ROCm); it isn’t designed to drive a desktop display even if you tried to pass through another GPU’s framebuffer to it.

So the initial **Critical Issue still stands**: with an MI50 (no display) and a Ryzen 5 5600 (no integrated graphics), you will get **no video signal at all**. The system will power on but you’ll never see the BIOS.

**What to check:**

- If you actually intend to buy a **Radeon Pro VII** (which does have Mini‑DP), that would solve the display problem. However, make sure you’re getting that exact model, because the second‑hand market often mixes up the naming. A genuine Pro VII typically costs more than ¥680 (≈¥1500‑2500 used), while the MI50 often goes for ¥500‑700 precisely because it’s headless and harder to use in a desktop PC.
- If you’re set on the MI50 for compute tasks, you’ll need a separate GPU with display outputs (even a cheap used GT 710/1030 or an APU) to drive your monitors. The easiest fix is to swap the CPU to a **Ryzen 5 5600G** (integrated graphics) and use the MI50 purely as a coprocessor, but note that mixing a datacenter card with consumer drivers can be tricky.

The other issues I mentioned (AM4 cooler compatibility, poor cooling for a passive server card, and overpriced RAM/SSD) remain unaffected by this clarification. Let me know if you want help refining the part list based on a display‑capable card or an APU swap.
