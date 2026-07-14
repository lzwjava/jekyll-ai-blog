---
audio: false
generated: true
image: false
lang: en
layout: post
title: PSU for R5 5600 + MI50 Build
translated: false
type: note
---

Question: What PSU fits this build (R5 5600 + MI50 16GB + B550M + 32GB DDR4 + 1TB NVMe)?

Answer:

Power sizing here is GPU-driven, and the load profile matters more than peak wattage because this isn't a gaming rig with bursty draw — if you're doing inference/training, the MI50 sits near its power ceiling for sustained periods, which stresses connectors and VRMs differently than gaming spikes.

**Load estimate:**
- MI50: ~300W board power (confirmed via its 2x 8-pin PCIe power inputs, each spec'd for 150W + 75W from the slot = 375W headroom, real draw ~300W under load)
- R5 5600: 65W TDP, up to ~88W boost
- Motherboard + RAM + fans: ~30-40W
- 1TB NVMe: ~5-8W under load
- Total sustained: ~400-440W

**PSU target: 650-750W, 80+ Gold, sustained-rated (not just peak-rated marketing wattage).**

PSUs are most efficient and stable at 40-60% load, so a 650-750W unit keeps you in that band with headroom for boost spikes and future upgrades (second GPU, bigger CPU). Going bigger (850W+) buys nothing here — you're not running dual GPUs.

**Non-negotiable requirement: two native PCIe 8-pin cables, not one cable daisy-chained with a splitter.**

The MI50 needs 2x 8-pin. Under sustained near-TDP load (unlike bursty gaming), running both connectors off one PSU cable via a Y-splitter or using cheap Molex-to-8pin adapters is a real risk — that's exactly the failure mode people report with used mining/compute GPUs on undersized or adapter-heavy PSUs. Check the PSU's cable spec sheet for "2x native PCIe 8-pin (or 6+2)" before buying, not just "supports up to 2 GPUs via included cables."

**Brand/tier:** stick to units with real 80+ Gold certification from known OEMs — Seasonic Focus GX, Corsair RM750/850, FSP Hydro PTM, be quiet! Pure Power 12M. Avoid unbranded/no-name units at this wattage; a 400W sustained sustained draw for hours daily (training/inference) is exactly the workload that exposes cheap PSU quality (voltage ripple, thermal throttling, capacitor failure) faster than gaming does.

**Concrete pick:** 650W-750W 80+ Gold, semi-modular or fully modular (easier cable management for the mATX case), 2 native PCIe 8-pin minimum — e.g. Seasonic Focus GX-650/750, Corsair RM750e.

References:
- [MI50 dual 8-pin power spec confirmation](http://wtarreau.blogspot.com/2025/12/amd-radeon-instinct-mi50-32gb-best-ai.html)
- [PSU efficiency curve and 80+ certification tiers](https://www.clickpowersystems.com/blog/80-plus-certification-guide)
