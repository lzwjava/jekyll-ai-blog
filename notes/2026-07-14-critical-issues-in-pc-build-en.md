---
audio: false
generated: true
image: false
lang: en
layout: post
title: Critical Issues in PC Build
translated: false
type: note
---

This build has several issues, ranging from a critical showstopper to less severe compatibility and practical concerns. Below is a breakdown:

### 1. 🚨 Critical: No display output possible

- **GPU (AMD Instinct MI50)** – This is a **datacenter compute accelerator**, not a consumer graphics card. It has **no video outputs** (no HDMI, DisplayPort, etc.).
- **CPU (Ryzen 5 5600)** – This model **does not have integrated graphics** (no “G” suffix).
- **Result:** The system will **never produce a display signal**. You won’t even see the BIOS.
  - *Fix:* Replace the MI50 with a consumer graphics card that has video outputs, or swap the CPU for a **Ryzen 5 5600G** (if you only need light graphics and compute, but note the MI50 would still be headless). For a general-purpose PC, the MI50 is simply the wrong component.

### 2. 🔧 Probable: CPU cooler may not support AM4

- The cooler (BUBALUS Frost 360A) is listed as supporting **AM5 / LGA2011** only. AM5 coolers often use the same mounting-hole spacing as AM4, but they typically rely on the **integrated AM5 backplate** and do not include the necessary **AM4 backplate + mounting screws**.
- Your motherboard is **AM4**. Without the correct hardware, you cannot mount the cooler.
  - *Fix:* Verify if the cooler box includes an AM4 kit. If not, pick a cooler that explicitly states **AM4 compatibility**.

### 3. ⚠️ Practical: GPU cooling concerns

- The MI50 is a **passively cooled dual-slot card** designed for high‑airflow server chassis (front‑to‑back wind tunnel).
- In a vertical desktop case (DeepCool CH270), the card may **overheat** unless you add very strong dedicated airflow directly over its heatsink. Normal case fans alone often aren’t enough. This can lead to thermal throttling or instability under load.

### 4. 💰 Value/price anomaly

- **32 GB DDR4‑3200 for ¥979** is **far above market price** (typical kit costs ~¥400–500). You’re overpaying by roughly 100% for standard non‑ECC memory. This isn’t a compatibility issue, but it’s a big budget waste.
- The **1 TB PCIe 4.0 SSD for ¥899** is also on the higher side (good 1 TB Gen4 drives are often ¥400–600). Not a problem, but you could reallocate the saved money.

### Summary of required actions

1. Replace the GPU with a **display‑capable card** or add a separate display adapter (plus change the CPU to one with integrated graphics if no dGPU is used).
2. Ensure the cooler has an **AM4 mounting kit** or swap it for an AM4‑compatible model.
3. Improve case airflow if you keep the passive MI50 (still doesn’t solve the no‑output problem).
4. (Optional) Choose a reasonably priced memory kit to free up budget for the above fixes.
