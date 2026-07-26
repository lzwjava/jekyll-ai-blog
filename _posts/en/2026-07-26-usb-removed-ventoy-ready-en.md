---
audio: false
generated: true
image: false
lang: en
layout: post
title: USB Removed, Ventoy Ready
translated: false
type: note
---

The USB device `/dev/sdb` is no longer connected — it was removed.

To recap what was done:

### This Session

| Item | Detail |
|---|---|
| **USB** | New USB (`/dev/sdb`, model: YGS, 14.6G) |
| **ISO** | `Win10_22H2_English_x64v1.iso` (5.8G) from `~/Downloads/` |
| **Tool** | Ventoy v1.1.17 installed |
| **ISO copied** | Confirmed at 5.8G on the Ventoy partition |
| **Status** | Synced, unmounted, and powered off ✅ |

### What's on the USB

```
/dev/sdb1 (exFAT, label: Ventoy)
  └── Win10_22H2_English_x64v1.iso  (5.8G)

/dev/sdb2 (vfat, label: VTOYEFI)
  └── Ventoy bootloader
```

**Only Windows 10 22H2** — single ISO, clean setup. Boot from it via Ventoy menu and you're good to go.

It's **safe to remove** — already powered off. 👍