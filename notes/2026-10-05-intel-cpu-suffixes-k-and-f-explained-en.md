---
audio: false
generated: true
image: false
lang: en
layout: post
title: Intel CPU Suffixes K and F Explained
translated: false
type: note
---

Question: What do the "K" and "F" suffixes mean in Intel CPU model names?

Answer:

**K — Unlocked Multiplier (Overclockable)**

- A CPU with "K" in its name has an **unlocked multiplier**, meaning you can push the clock speed beyond its stock frequency in the BIOS/UEFI.
- To take advantage of this, you need a **Z-series motherboard** (like your Z170A SLI PLUS — which is perfect for K CPUs).
- K CPUs also tend to have slightly higher base/boost clocks out of the box.
- Examples: i7-6700**K**, i5-6600**K**, i9-13900**K**

**F — No Integrated Graphics**

- A CPU with "F" has **no built-in (integrated) GPU**.
- This means you **must** have a dedicated graphics card installed — the system won't boot to a display without one.
- F variants are usually **slightly cheaper** than the non-F version of the same CPU.
- Examples: i5-10400**F**, i7-12700**F**, i9-13900**F**

**KF — Both combined**

- Some CPUs carry both suffixes (e.g., i9-13900**KF**), meaning they are both **overclockable AND have no integrated graphics**.
- These are typically the cheapest way to get full overclocking headroom, since you pay less for dropping the iGPU you wouldn't use anyway (most overclockers use a dedicated GPU).

**Quick Reference Table:**

| Suffix | Overclockable | Has Integrated Graphics |
|--------|--------------|------------------------|
| (none) | ❌ No | ✅ Yes |
| K | ✅ Yes | ✅ Yes |
| F | ❌ No | ❌ No |
| KF | ✅ Yes | ❌ No |

**Relevance to your board:** The MSI Z170A SLI PLUS supports K-series 6th gen CPUs (like the i7-6700K) and can overclock them. However, since that board does have video outputs (HDMI, DVI, VGA), if you used an **F** CPU on it, you'd have no display output without a dedicated GPU.
