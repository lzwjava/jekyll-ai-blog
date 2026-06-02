---
audio: false
generated: true
image: false
lang: en
layout: post
title: Containerd Space Recovery Status
translated: false
type: note
---

Containerd rsync killed, partial data cleaned up. Models move is done and working. Status:

```
Root disk:  697G  88G used (610G free)  — was 124G, freed 36G
Volume:     100G  37G used (58G free)
```

What worked:
- ✓ llama.cpp/models (37G) → volume, symlinked back

What didn't:
- ✗ containerd (59G) — 39,000+ tiny files in overlayfs snapshots (ROCm container layers). rsync would take forever.

**containerd options:**
1. `systemctl stop containerd && mv /var/lib/containerd /mnt/volume_.../containerd && ln -s /mnt/volume_.../containerd /var/lib/containerd && systemctl start containerd` — mv is instant on same filesystem... but these are different filesystems so it'd copy too.
2. **Prune unused container images** instead — `crictl rmi --prune` could reclaim significant space without moving anything.
3. Change containerd's `root` in `/etc/containerd/config.toml` to point at the volume (requires restart, might break running containers).

Want me to try pruning container images first? That's the safest way to free space on root without risking the containerd setup.
