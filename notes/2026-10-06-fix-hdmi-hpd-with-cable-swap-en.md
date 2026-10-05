---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix HDMI HPD with Cable Swap
translated: false
type: note
---

### Notes

- **Script:** `/home/lzw/fix-hdmi-hpd.sh` (idempotent; re-runnable).
- **Backup:** `/etc/default/grub.bak.20261006020242` — to revert: `sudo cp /etc/default/grub.bak.* /etc/default/grub && sudo update-grub` then reboot.
- **Trade-off:** with polling off, plugging in a *different* monitor while running won't be auto-detected (intended for a fixed desktop).
- **Stale config:** `~/.config/monitors.xml` still lists a non-existent `DVI-I-1` 1024x768 monitor. Not the cause, but you may want it cleared — say the word.

### Still recommended

These are software band-aids. The root cause is a bouncing HDMI **HPD** line — **swap the HDMI cable** (or try `HDMI-A-2`/DP). If the storm returns after rebooting with a good cable, the GPU port or monitor input is the culprit.
