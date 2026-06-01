---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fast Snapshot to Droplet via Lazy Hydration
translated: false
type: note
---

**Question:** Why is creating a droplet from a 130GB GPU snapshot so fast, even though creating the snapshot itself takes 20+ minutes?

**Answer:**

## Why Snapshot Creation is Slow

When you **create** a snapshot, DigitalOcean has to:

1. Quiesce/freeze the disk state
2. **Read every used block** from your droplet's disk (130GB of actual data)
3. Compress and deduplicate it
4. Transfer and store it in their object storage (like S3-equivalent)

That's a full disk read + network transfer + compression pipeline. 20+ mins for 130GB is reasonable.

## Why Droplet-from-Snapshot is Fast

This is the key insight — **DigitalOcean uses Copy-on-Write (CoW) lazy hydration**, not a full restore:

```
Snapshot (stored in object storage)
         │
         ▼
New Droplet boots ──► Only metadata + boot blocks copied immediately
                      Remaining blocks fetched on-demand as accessed
```

The droplet **starts immediately** from a thin clone. Blocks are pulled from the snapshot store lazily as your workload touches them. This is the same technique used by:

- AWS EBS fast snapshot restore
- VMware linked clones
- Docker layers (overlay2)
- ZFS/btrfs CoW clones

## What This Means Practically for You

```
t=0s    Droplet created, gets IP, SSH accessible  ← instant
t=30s   You SSH in, run nvidia-smi / rocm-smi     ← works
t=60s   You start loading a 70B model             ← first access, blocks fetched
t=??    Blocks fully hydrated in background       ← transparent to you
```

The **first time** you access data that hasn't been hydrated yet (loading a big model, reading a dataset), you may notice slightly slower disk reads — that's the lazy fetch happening. After that, it's cached locally on the droplet's SSD.

## Analogy

Think of it like:

- **Snapshot creation** = photocopying an entire book (slow, must read every page)
- **Droplet from snapshot** = getting a library card that points to the book (instant), pages physically moved to your desk only when you open them

## Practical Implication for Your Workflow

Since you're working with MI300X and likely loading large models:

```bash
# After droplet creation, you can optionally pre-warm the disk
# to avoid lazy-fetch latency during actual work
dd if=/dev/vda of=/dev/null bs=4M status=progress
```

Or just let it hydrate naturally — DigitalOcean does it in the background anyway. By the time you `apt update`, set up `tmux`, and get your environment ready, most critical blocks are already local.

This is why **snapshot → droplet** is the right workflow for your ~$2/hr GPU sessions: destroy when done, restore in seconds, pay only for active compute.