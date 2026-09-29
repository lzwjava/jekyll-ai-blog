---
audio: false
generated: true
image: false
lang: en
layout: post
title: Root filesystem nearly full
translated: false
type: note
---

Here's the disk usage on this system:

| Filesystem | Size | Used | Avail | Use% | Mounted on |
|---|---|---|---|---|---|
| `/dev/nvme0n1p2` | 916G | 814G | **55G** | **94%** | `/` |
| `/dev/sda1` | 1.8T | 1.2T | **590G** | 67% | `/mnt/data` |
| tmpfs | 6.3G | 4.1M | 6.3G | 1% | `/run` |
| tmpfs | 32G | 179M | 32G | 1% | `/dev/shm` |
| `/dev/nvme0n1p1` | 511M | 6.2M | 505M | 2% | `/boot/efi` |

**Summary:**
- Root filesystem (`/`) is at **94%** usage with only **55G** free — getting tight.
- Your working directory `/mnt/data` is a 1.8T volume with **590G** free (67% used).