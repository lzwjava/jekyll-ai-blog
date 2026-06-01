---
audio: false
generated: true
image: false
lang: en
layout: post
title: Stop Rsync Corrupting Containerd Data
translated: false
type: note
---

Here's the situation:

```
containerd:     stopped (dead since 6 min ago)
rsync:          ACTIVE, copying 59G containerd data to volume
Root disk:      697G, 88G used (610G free) — plenty of space
Volume:         100G, 60G used (35G free) — WON'T FIT!
```

**Stop the rsync immediately.** Two problems:

1. **Volume has only 35G free, containerd data is 59G** — it'll fill the volume and crash partway through.
2. **`rsync -a` breaks hardlinks** — containerd snapshots use hardlinks internally. After rsync, the data would be corrupted.

```bash
# Kill the rsync
kill 6595 6602 6603

# Clean up partial copy
rm -rf /mnt/volume_atl1_1780280110689/containerd-data/

# Restart containerd so Docker works again
systemctl start containerd
```

**The real answer: you don't need to move it at all.** Your root disk has **610G free**. The 59G containerd data is fine where it is. The volume is smaller (100G) and already 60% full — it's the wrong target for this.

If you actually need the space later, just `docker system prune -af` to nuke unused images. Want me to kill that rsync and restart containerd?