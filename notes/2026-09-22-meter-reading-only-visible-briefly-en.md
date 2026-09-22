---
audio: false
generated: true
image: false
lang: en
layout: post
title: Meter reading only visible briefly
translated: false
type: note
---

Done. Here's what I found and extracted.

## Key finding: the meter only shows a reading at ~30–31.5 s

The whole 39.6 s video was scanned densely (4 fps in the 29–36 s window). The display is **blank for almost the entire video** and only settles a few times:

| Time | Display | Meaning |
| ------ | --------- | --------- |
| **30.00 s** | `00.0` Ω | Stable — near-zero resistance (short/ground) |
| **31.25 s** | `006 V` (0.06 V) | Stable DC voltage — essentially dead rail / no power |
| 31.50 s | `1` | Over-range / **open circuit** (OL) |
| 33.75 s | `888` → `988` | **Self-test pattern** (all LCD segments lit), not a real reading |
| everywhere else | blank | Display not visible / off |

## Audio

No beeps or tones. Two ~0.2 s voice snippets at **13.75 s** and **14.39 s** — your narration. The rest is silence.

## Saved keyframes (full-res, 1920 px)

```
keyframes/
├── t_13.75s.jpg    ← audio (voice) event
├── t_14.39s.jpg    ← audio (voice) event
├── t_30.00s.jpg    ← meter: 00.0 Ω  (stable)
├── t_31.25s.jpg    ← meter: 006 V   (stable)  ← the best reading in the video
├── t_31.50s.jpg    ← meter: OL / open circuit
└── t_33.75s.jpg    ← meter: LCD self-test pattern
```

## What this means for your workflow

Your instinct was right: **the useful reading is only on-screen for ~1.5 seconds (30–31.5 s)**. Fixed-interval extraction (every 3 s) mostly caught blank display — that's why earlier frames looked "unreadable."

**Practical fix:** probe and *hold the probe still until the reading settles*, then either:

- keep the display in frame for 2+ seconds, or
- snap a still photo the moment it's stable.

That guarantees the vision model can read the value. If you want, I can also make the tool **hold the last good frame** (keep displaying the last stable reading until a new one appears) — but honestly, holding the probe steady on-screen is the simpler fix.
