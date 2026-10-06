---
audio: false
generated: true
image: false
lang: en
layout: post
title: USB Stick Health Test
translated: false
type: note
---

The stick re-enumerated cleanly as `/dev/disk12` (15.7 GB, USB, removable) — it's talking to the bus again, and the kernel even re-read the old GPT (partition 4's Linux region shows as free space since dd had started overwriting it before dying).

Now the health test — this erases whatever's on the stick (which you're about to overwrite with the ISO anyway):

```bash
diskutil eraseDisk FAT32 TEST /dev/disk12
```

Run that and tell me if it completes or hangs. If it completes, we re-flash (different port, `bs=1m`). If it hangs... the drive is done.

I can also run it for you if you want — just say the word.
