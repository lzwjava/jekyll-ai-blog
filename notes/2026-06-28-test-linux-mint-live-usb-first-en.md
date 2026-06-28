---
audio: false
generated: true
image: false
lang: en
layout: post
title: Test Linux Mint Live USB First
translated: false
type: note
---

Here's the summary — save this for when you're ready:

**Recommendation: Start with a live USB test first.**

Steps:
1. Download Linux Mint Cinnamon ISO (22.x) from linuxmint.com on any machine
2. Flash to a USB drive (16 GB+): `sudo dd if=linuxmint.iso of=/dev/rdiskN bs=4m` on macOS
3. Plug into the MacBook Pro, hold Option key at boot, select the USB
4. Boot into live session — test Wi-Fi, trackpad, keyboard, audio, display
5. If everything works (or you can fix Wi-Fi with a dongle/driver), then decide on install method

**Why test first:** The Broadcom Wi-Fi is the main risk. If you can't get online after install, you're stuck. A live session lets you confirm hardware support before committing.

If the live session works well, I'd recommend **external USB SSD install** — it's non-destructive, gives you a portable Linux system, and you keep macOS intact for recovery. A 128 GB USB 3.0 SSD costs ~$15-20.
