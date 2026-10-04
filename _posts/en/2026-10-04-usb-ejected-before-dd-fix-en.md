---
audio: false
generated: true
image: false
lang: en
layout: post
title: "USB Ejected Before dd: Fix"
translated: false
type: note
---

Found the root cause. The logs reveal what happened:

```
20:51:30  storagekitd: ejected disk, id = /dev/disk12, success.      ← disk EJECTED
20:51:46  kernel: dd(84861) deny(1) file-write-create /dev/rdisk12   ← your dd ran AFTER the eject
```

**Your USB stick was ejected at 20:51:30 — before your `dd` even ran** (via Finder's eject button / Disk Utility, or the cable came loose). `dd` then tried to write to a device that no longer existed → `Operation not permitted`.

### Fix: re-plug and flash it in one go

**1. Physically pull the USB out and plug it back in** (wait ~3 seconds).

**2. Confirm it's back** — run this and tell me the number it gets:

```bash
diskutil list
```

**3. As soon as it appears, run these back-to-back** (don't eject anything in between, don't click the eject icon in Finder, don't let anything auto-mount):

```bash
diskutil unmountDisk /dev/diskNN     # NN = number from step 2
sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdiskNN bs=4m status=progress conv=fsync
```

It'll take ~2–5 minutes. Wait for `xxxx+0 records out` and the prompt to come back before unplugging.

---

⚠️ Two tips to avoid this again:
- Don't use Disk Utility / Finder eject before `dd` — only `diskutil unmountDisk` (unmount ≠ eject).
- If macOS auto-mounts after replugging, that's fine — unmount right before `dd`.

Plug it in and paste `diskutil list` output — I'll verify the device number with you before you run `dd`.
