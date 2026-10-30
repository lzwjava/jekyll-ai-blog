---
audio: false
generated: true
image: false
lang: en
layout: post
title: Passing Photo Composition Analysis
translated: false
type: note
---

Here's the analysis of why **`photo_6126_body_600x600.jpg`** (the version currently on disk) passes:

## What's actually in the file

| Metric | Value |
| --- | --- |
| **Dimensions** | **600 × 727 px** (aspect 0.825 ≈ 5:6) — *note: not actually 1:1; the file was modified after my script output a 600×600* |
| **Face box** | x=123, y=167, 364×364 px |
| **Face center** | (305, 349) → **50.9%** across, **47.9%** down |

## Why it reads as "OK"

1. **Horizontal centering** — face center at 50.9% of width (off-center by only 0.9%) and side margins nearly symmetric (L 20.6% / R 18.8%). Subject is centered-looking.
2. **Head in upper half** — face center at 47.9% of height → head sits in the upper part of the frame (rule-of-thirds friendly), not floating low.
3. **Head size is large but not cropped** — head spans **50% of frame height**, 61% of width. This is exactly what fixes your earlier "人像区域尺寸不足": the portrait/person region now fills a sufficient, dominant area.
4. **Clear breathing room** — 167 px (23%) above the head and **197 px (27%) from chin to bottom** → shoulders/torso are visible below the chin, so nothing is cut off and the composition doesn't feel cramped.
5. **Symmetric, tight-but-safe framing** — the subject is big enough to read as a proper portrait while margins and chin-bottom space keep it inside the frame boundaries.

**In short:** it's OK because the head is large (fixing the "人像区域尺寸不足" issue), horizontally centered (±1%), placed in the upper half, with balanced side margins and clear chin-to-bottom space.

One heads-up: this differs from what my script generated (600×600 square) — the passing file is 600×727. Let me know if you want me to re-align the script to reproduce **this exact framing** (600×727, head ~50% of height) so future runs match the accepted version.
