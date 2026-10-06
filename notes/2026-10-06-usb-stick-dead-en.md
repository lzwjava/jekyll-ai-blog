---
audio: false
generated: true
image: false
lang: en
layout: post
title: USB Stick Dead
translated: false
type: note
---

That's the decisive failure. The sequence in the kernel log:

```
22:55:30  removed disk12                    ← fell off the disk tree
22:55:35  unable to probe /dev/disk12s1/2/3 ← DiskArbitration couldn't even read the media
22:56:24  removed disk12s1 / s2 / s3
22:56:26  removed disk12                    ← whole disk node gone
```

The USB device is still physically on the bus (`OnlyDisk@00130000` present in IORegistry, idle), but **the media no longer responds** — same "medium not present" behavior that hung `dd`. The kernel gave up on it entirely: `Could not find disk for disk12`.

**Verdict: this USB stick is dead.** Timeline of evidence:
1. `dd` wrote fine to **5.04 GB** then hit bad media at a fixed LBA — pipe stalled, retried dozens of times, hung for 18+ min.
2. After replug, `diskutil eraseDisk` **couldn't even open the device**.
3. DiskArbitration couldn't probe a single partition — the flash isn't responding at all now.

It's a white-label "OnlyDisk" stick (generic, no brand), which matches — these use the cheapest flash and controllers, and once they start throwing "medium not present" errors, they don't recover.

**Recommendation: stop trying to revive it.** You'd be gambling an OS install on a drive that's already failed twice. A name-brand 16 GB+ USB 3.0 stick costs a few dollars and will reliably flash:

```bash
sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdiskX bs=4m status=progress
```

(verify `X` with `diskutil list` first). If you *must* try the old stick one last time, unplug/replug and check `diskutil list` — but I'd expect it to stay gone or fail again.
