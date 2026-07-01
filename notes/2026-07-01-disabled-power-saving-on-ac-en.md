---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disabled Power Saving on AC
translated: false
type: note
---

Done. All settings applied and verified on `xiaoxin@192.168.1.28` (Linux Mint 22.3 Cinnamon):

| Setting | Before | After |
|---|---|---|
| Screensaver idle activation | `true` | **`false`** |
| Lock screen on suspend | `true` | **`false`** |
| Display sleep on AC power | 1800s (30 min) | **0 (never)** |
| Dim screen on AC | `true` | **`false`** |
| Suspend on AC timeout | 0 (already off) | 0 (unchanged) |
| Session idle delay | 300s | **0 (never)** |

Screen stays on and doesn't lock when plugged into power. If they want battery-side too, say the word.
