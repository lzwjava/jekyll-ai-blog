---
audio: false
generated: true
image: false
lang: en
layout: post
title: iPhone App Audit and Cleanup Summary
translated: false
type: note
---

Here's what we did in this session:

1. **Checked installed apps** — Listed all ~250+ user apps on your connected iPhone "lzwjava" using `ideviceinstaller`

2. **Identified games** — Found only 6 game-related apps (Chess, NeuralPlay Bridge, Mahjong 4 Friends, Vita Mahjong, Steam, Nintendo Switch App)

3. **Deleted 4 games** — Uninstalled Mahjong 4 Friends, Vita Mahjong, Chess, and NeuralPlay Bridge via `ideviceinstaller uninstall`

4. **Checked app file sizes** — Pulled `StaticDiskUsage` for all apps, sorted largest to smallest. Top space hogs: WeCom (852 MB), TikTok (805 MB), QQ (758 MB), HSBC HK (749 MB), WeChat (744 MB)

5. **Listed smallest apps** — Showed the bottom 50 apps (all under 60 MB each), noted that deleting small apps won't free much space — better to target the big ones

Total space freed from game deletions: ~27 MB (negligible). The real savings would come from deleting large unused apps like HUAWEI AI Life (730 MB), T-Life (570 MB), Amazon Alexa (414 MB), etc.
