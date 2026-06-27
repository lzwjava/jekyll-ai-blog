---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacBook Air M2 charger and cable
translated: false
type: note
---

Question: For the MacBook Air M2 (model A2681), what charger and cable does it use?

Answer:

The A2681 (13-inch MacBook Air M2, 2022) ships with:

**Charger (power adapter):**

- Base config (8-core GPU, 256GB) → **30W USB-C Power Adapter**
- Higher configs / build-to-order → **35W Dual USB-C Port Power Adapter** (two USB-C ports, charge two devices) or optionally the **67W USB-C Power Adapter** for fast charging
- Fast charge (0→50% in ~30 min) requires the **67W adapter** (or higher, e.g. 70W/96W/100W)

**Cable:**

- **USB-C to MagSafe 3 Cable** (2m, color-matched to the laptop: midnight, starlight, silver, space gray)
- MagSafe 3 is the magnetic port. You can *also* charge via either of the two USB-C / Thunderbolt 3 ports on the left side using a plain USB-C–to–USB-C cable, leaving MagSafe free.

**Practical notes for your setup:**

- The board pulls ~30W max under load, so 30W "works" but won't fast-charge. The 67W gets you the 30-min half-charge.
- MagSafe 3 cable is just a USB-C cable with a MagSafe tip — it negotiates standard USB-C PD, so any decent third-party USB-C PD charger (Anker 65W GaN, etc.) drives MagSafe fine.
- Charging through the USB-C ports is genuinely equivalent electrically; MagSafe's only real advantage is the breakaway connector and freeing a data port.
- The A2681 supports USB-C PD up to ~67–70W input; pushing a 100W charger at it just caps at what the board negotiates — no benefit, no harm.

References:

- [MacBook Air (M2, 2022) - Technical Specifications](https://support.apple.com/en-us/111867)
- [Identify the power adapter for your Mac notebook](https://support.apple.com/en-us/118264)
