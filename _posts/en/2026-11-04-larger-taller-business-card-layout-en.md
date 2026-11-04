---
audio: false
generated: true
image: false
lang: en
layout: post
title: Larger Taller Business Card Layout
translated: false
type: note
---

Both cards regenerated with a taller, larger layout:

- **English card**: `card_output/business_card_en.png` (2300×1680)
- **Chinese card**: `card_output/business_card_zh.png` (2300×1680)

Changes made in `ww/card/card.py`:
- **Bigger canvas**: 2300×1680 (up from 2100×1200) — taller so the About text has plenty of room.
- **Larger text everywhere**: bigger About body font (44/46 vs 38/40), name (92), role (46), contacts (34), watermark (34).
- **More air per line**: increased line-height/spacing and paragraph gaps.
- **Spaced-out left panel**: bigger avatar (480), name/role pushed down, larger QR code, contacts moved lower so the tall panel doesn't look empty.

I verified programmatically that both the EN (bottom of text ~1514) and ZH (~1408) intros sit cleanly above the watermark (~1590) with no clipping or overlap.
