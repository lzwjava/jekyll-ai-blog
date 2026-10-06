---
audio: false
generated: true
image: false
lang: en
layout: post
title: Failing USB Stick
translated: false
type: note
---

dd is now in the process of exiting (its state shows as exiting after the hung I/O gave up) — it'll return to your shell with an I/O error any moment now. Give it a few seconds.

So the summary of the situation:

**Your USB stick (`OnlyDisk`, 15.7 GB) is defective/failing.** At ~5.04 GB it hit a broken region, returned "medium not present" and stalled its USB pipe, hanging the write. This isn't a command problem — the flash media or controller gave up.

**Next steps once dd exits:**

1. **Don't try to boot the stick** — the image is truncated and the tail sectors are bad.
2. **Test the drive itself**: `diskutil eraseDisk FAT32 TEST /dev/disk12` — if this hangs or errors, the stick is dead and you need a different one.
3. If the erase works, it was possibly a flaky port — **try a different USB port** and re-flash with a smaller block size: `sudo dd if=~/Downloads/ubuntu-26.04-desktop-amd64.iso of=/dev/rdisk12 bs=1m status=progress`.
4. After any flash, always `sync` and verify with `diskutil list disk12` (`--` If that still shows trouble, the drive is unreliable and not worth trusting with an OS install).

Want me to wait and check whether dd actually exits cleanly, or watch the erase test if you run it?
