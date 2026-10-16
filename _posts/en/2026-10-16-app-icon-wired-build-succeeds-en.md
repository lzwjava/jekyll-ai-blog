---
audio: false
generated: true
image: false
lang: en
layout: post
title: App Icon Wired, Build Succeeds
translated: false
type: note
---

Done. The build succeeds with the icon wired in.

**What I did:**

1. **Picked the right size:** the iOS `AppIcon.appiconset` uses the modern single-size format requiring exactly **1024×1024** — so `fun-live-icon-1024.png` is the correct source (verified with `sips`, confirmed 1024×1024). The smaller sizes (32/48/64/128/160/256/512) are for web favicons and aren't used by iOS.

2. **Copied it into the asset catalog:** `fun-live-icon-1024.png` → `LiveIos/Assets.xcassets/AppIcon.appiconset/AppIcon.png`

3. **Updated `Contents.json`** to reference `AppIcon.png` in the `ios universal 1024x1024` slot.

4. **Verified:** `ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon` already points to the catalog, and a simulator build succeeded.
