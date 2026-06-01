---
audio: false
generated: true
image: false
lang: en
layout: post
title: Set Up ML Data Volume
translated: false
type: note
---

**Quick answers:**

**Storage size:** 200GB

**Configuration:** Automatically Format & Mount

**Filesystem:** Ext4

**Name:** `ml-data`

That's it. Reasoning:

- **Auto format & mount** — saves you the `mkfs` + `fstab` steps, DigitalOcean does it for you
- **Ext4** — battle-tested, widely supported, no reason to use XFS unless you have massive files >16TB or specific throughput needs. Ext4 is fine for model checkpoints and token binaries
- **200GB** — as calculated above, covers tokenized data + 3 checkpoints + headroom

After droplet boots, volume will be ready at `/mnt/ml-data` — just `cd /mnt/ml-data` and start working.