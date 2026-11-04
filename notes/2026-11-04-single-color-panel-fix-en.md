---
audio: false
generated: true
image: false
lang: en
layout: post
title: Single-Color Panel Fix
translated: false
type: note
---

Both cards regenerated with a clean single-color left panel:

- `card_output/business_card_en.png` (2300×1680)
- `card_output/business_card_zh.png` (2300×1680)

The problem: a scaling bug I'd introduced made the accent divider span the entire left panel (giant gold block) instead of a thin line — that's what created the "two colors" look. I removed the accent divider line entirely, so the left panel is now one solid warm-brown color, with just the black background on the right. Confirmed via pixel sampling that the panel is uniform.
