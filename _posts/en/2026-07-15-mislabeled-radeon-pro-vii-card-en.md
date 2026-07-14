---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mislabeled Radeon Pro VII Card
translated: false
type: note
---

You're right to push back with the listing's description. Let me re‑examine this carefully.

The advertisement claims:

> “AMD MI50显卡，16G显存，带ECC芯片……鲁大师跑分40W左右……**插上即用**” (implying display out) and you say it explicitly mentions **Mini‑DP**.

Officially, the **AMD Radeon Instinct MI50** is a **headless compute accelerator** (no display outputs). The card with the same Vega 20 GPU, 16 GB HBM2, ECC, and **multiple Mini‑DisplayPort outputs** is the **AMD Radeon Pro VII**. The two are often confused in the second‑hand market because they share the same die, but the Pro VII has a blower fan and 6× Mini‑DP, while the MI50 is a passive server card with zero video connectors.

**So what’s actually being sold here?**
It’s almost certainly a **mislabeled Radeon Pro VII** (or a card that was converted, but that’s far less likely). The mention of “插上即用” and Mini‑DP, combined with “鲁大师跑分40W” (a typical Pro VII score), makes it clear: **this is a display‑capable workstation card.**

---

### If the card is indeed a Radeon Pro VII (or equivalent with Mini‑DP), the previous “critical – no display” issue **disappears**.
You’ll get a video signal normally. However, other potential problems remain, and some new ones need attention:

1. **Driver & Software Compatibility (minor but real)**
   - A real MI50 requires **ROCm** (Linux) and has no Windows display driver.
   - A Pro VII uses standard **Radeon Pro / Adrenalin drivers** (Windows & Linux) and works as a normal GPU for displays, gaming, and compute.
   - If the seller flashed a Pro VII with an MI50 vBIOS to sell it as a compute card, you might face driver confusion. *Check GPU‑Z:* it should report “Radeon Pro VII” and show 6 Mini‑DP ports under the Graphics Card tab. If it says “MI50” but has ports, the vBIOS has been cross‑flashed—you may need to flash it back to a Pro VII BIOS for reliable Windows operation.

2. **Cooling & Temperature (the 90°C stress test)**
   - The official Pro VII has a **blower‑style cooler**; 90°C after 10 minutes of stress is high but within its thermal limit (max ~110°C hotspot). Still, it suggests the card may be dusty, have dried paste, or run in a low‑airflow case.
   - The DeepCool CH270 is a vertical case with decent airflow, but if the card is a *passive* MI50 (no fan) that was modded with a Mini‑DP, 90°C is disastrous—you’d need to strap a fan directly to it.
   - Since the ad says “插上即用” and gives a temperature, it’s likely active‑cooled. 90°C is borderline; I’d expect throttling or loud fan noise.

3. **The CPU cooler still may not support AM4**
   The BUBALUS Frost 360A listing emphasizes AM5, not AM4. You **must** confirm the box includes an AM4 bracket and backplate. Without it, the cooler is useless. Simply ask the seller or check the package contents.

4. **RAM & SSD are very overpriced**
   - 32 GB DDR4‑3200 for **¥979** is ~double the normal price. You can get the same spec for ¥400–450. This eats budget that could go toward a better power supply or a CPU upgrade.
   - A 1 TB PCIe 4.0 NVMe SSD for **¥899** is also high; good 1 TB drives (e.g., Solidigm P44 Pro, WD SN770) often cost ¥500–600.

5. **PSU quality concern**
   The Thermalright TR‑KG750 is a budget Gold unit. It’s *probably* fine, but for a Vega‑based 16 GB card (which can spike >300 W) and a Ryzen 5 5600, I’d prefer a slightly better known unit from a tier‑list regular (e.g., DeepCool, Cooler Master). However, this is not a deal‑breaker if budget is tight.

---

### Verdict: Is this setup usable?
**Yes, if:**
- You verify the GPU is a Radeon Pro VII (or at least has working Mini‑DP outputs and a fan) and you can install normal drivers.
- You source an AM4 mounting kit for the cooler.
- You consider swapping the RAM and SSD to sensibly priced alternatives, saving ~¥500+.

**No, if:**
- The card turns out to be a real MI50 with no video out (despite the ad), and you’re left with no display.
- The card is a cross‑flashed Pro VII with driver issues you can’t resolve easily.

My recommendation: **Before buying, ask the seller for a clear photo of the I/O bracket** (showing the Mini‑DP ports) and a **GPU‑Z screenshot**. If they match a Radeon Pro VII, you’re good to go—just fix the cooler and memory pricing. If they refuse or the card looks passive with no fan and only a single suspicious Mini‑DP, walk away.
