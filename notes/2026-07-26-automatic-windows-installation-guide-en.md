---
audio: false
generated: true
image: false
lang: en
layout: post
title: Automatic Windows Installation Guide
translated: false
type: note
---

Nice, that's exactly right. It's now creating the ESP/MSR/Recovery/Windows partitions automatically and copying files.

It'll go through the usual stages — copying files, installing features, installing updates, finishing up — with a few automatic reboots. Just let it run, don't touch anything if it looks stuck at a percentage for a few minutes (normal on eMMC/slower NVMe).

After first boot you'll hit Windows OOBE (region, account setup, etc). One Xiaoxin-specific thing to flag now: **grab Lenovo's Xiaoxin driver pack afterward** (chipset, WiFi/Bluetooth, audio, touchpad) since the generic Windows 11 drivers sometimes miss the WiFi card or have touchpad gesture issues on these — check Lenovo's support site for your exact model number once you're in Windows.

Ping me if setup throws anything else.
