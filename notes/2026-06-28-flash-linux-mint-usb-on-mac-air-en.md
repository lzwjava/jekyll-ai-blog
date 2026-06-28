---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash Linux Mint USB on Mac Air
translated: false
type: note
---

Got it. Here's what to do on your Air:

**1. Unplug the USB drive from the MacBook Pro, plug it into your Air.**

**2. Then run these commands:**

```bash
# Download Linux Mint ISO (~2.8 GB)
curl -L -o /tmp/linuxmint.iso \
  "https://mirrors.gigenet.com/linuxmint/iso/stable/22.1/linuxmint-22.1-cinnamon-64bit.iso"

# Find the USB drive identifier (look for the ~16 GB external disk)
diskutil list

# Unmount it (replace diskN with the actual identifier)
diskutil unmountDisk /dev/diskN

# Flash the ISO (replace rdiskN — use rdisk, not disk, it's 10x faster)
sudo dd if=/tmp/linuxmint.iso of=/dev/rdiskN bs=4m status=progress

# Eject
diskutil eject /dev/diskN
```

**3. Move the USB back to the MacBook Pro, reboot, hold Option (⌥) key, select the USB.**

Want me to start the download on your Air right now?
