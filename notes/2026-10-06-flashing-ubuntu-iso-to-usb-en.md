---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flashing Ubuntu ISO to USB
translated: false
type: note
---

The ISO is 6.1 GB, fits on your 15.7 GB USB. Here's the command:

```bash
diskutil unmountDisk /dev/disk12   # unmount any mounted volumes first
sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=4m status=progress
sync                                # flush writes before unplugging
```

Notes:
- **`/dev/rdisk12`** (raw device) is used on macOS for faster writes — but make *absolutely sure* `disk12` is the right disk. One typo (`disk1`, `disk3`) and you'll wipe your system/Data volume. Verify with `diskutil list` before running.
- Running `dd` on the whole disk replaces the existing GPT/partition table, so all 4 current partitions get erased — that's expected and fine.
- Wait for `sync` to finish before unplugging. The USB is 15.7 GB, so it'll take a few minutes at USB 2.0 speeds.
- The `--clear` equivalent isn't needed; `dd` writes the raw ISO image (hybrid ISO) which boots directly.

After it's done, verify with `diskutil list disk12` — you should see a single partition that looks like the Ubuntu installer.
