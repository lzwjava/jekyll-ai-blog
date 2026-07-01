---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disable Power Saving Settings
translated: false
type: note
---

Done on `lzwjava@192.168.1.57` (Fedora 44 / GNOME):

| Setting | Before | After |
|---|---|---|
| Screensaver idle activation | `true` | **`false`** |
| Lock screen | `true` | **`false`** |
| Suspend on AC timeout | 900s (15 min) | **0 (never)** |
| Screen dimming | `true` | **`false`** |
| Session idle delay | 300s | **0 (never)** |

Same behaviour as xiaoxin's machine — screen stays on, never locks, never dims, never suspends when plugged into power.
