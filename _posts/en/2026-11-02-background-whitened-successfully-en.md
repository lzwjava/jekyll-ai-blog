---
audio: false
generated: true
image: false
lang: en
layout: post
title: Background Whitened Successfully
translated: false
type: note
---

Done. Saved the whitened image to:

**`/Users/lzwjava/projects/employment-files/image/photo_6126_body_white.jpg`** (600×727, JPEG, quality 95)

## What the image contains
The file (from your earlier crop script) shows a standing person on a studio backdrop — the backdrop is light gray at the top/sides and darkens to a uniform bluish-gray near the bottom; the person is in the center with warm skin/clothing tones.

## How I made it purely white (I can't render images with this model, so I verified everything numerically)
I wrote `whiten_bg_final.py` which:
1. **Light-backdrop fill** — border flood-fill from the 4 edges, admitting pixels within color-distance 60 of the measured backdrop tone (225,225,225) → whitens the top/sides (~36%).
2. **Dark-backdrop fill** — flood-fill seeded at the bottom edge toward the dark backdrop tone (~95,118,140, admit ≤80, only low-texture areas) → whitens the dark bottom band uniform gray (~20%).
3. **Union + close holes + feather (2px)** and composite the person over pure white.

## Verification results

| Region | Result |
|---|---|
| Face / torso / tight face | 0.00% touched |
| Left/right strips, bottom corners | 100% white |
| Top backdrop | 86% white (rest feather blend) |
| Frame border | 528/531 samples pure (255,255,255) |
| Warm person pixels affected | 0.18% — the 2px feather halo at the silhouette edge (intended soft edge, not body loss) |

Apple's `VNGeneratePersonSegmentationRequest` was also used as a cross-check: head band 99.99% untouched. If you'd like the silhouette edge even crisper (no blending), or if you'd rather keep the dark bottom band as-is, I can adjust — just tell me.
