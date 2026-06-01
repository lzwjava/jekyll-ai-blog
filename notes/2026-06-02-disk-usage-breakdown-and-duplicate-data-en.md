---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disk Usage Breakdown and Duplicate Data
translated: false
type: note
---

The disk is only 124GB used, not 240GB. Here's the breakdown:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Disk Usage — amd-cloud (MI300X)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total:  124 GB used / 697 GB (18%)

Breakdown:
  /root/                         81 GB
    /root/zz/datasets/fineweb-edu    40 GB  ← duplicate training data
    /root/nanoGPT/data/fineweb       28 GB  ← training data
    /root/nanoGPT/out-fineweb-760m   8.5 GB ← checkpoint (ckpt.pt)
    /root/llama.cpp                  385 MB
    /root/zz/logs                    200 KB
  /usr/                          22 GB
  /opt/                          22 GB
  /var/                          694 MB
  /tmp/                          37 MB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The biggest space hogs:

1. **40 GB** — `/root/zz/datasets/fineweb-edu` — duplicate of training data
2. **28 GB** — `/root/nanoGPT/data/fineweb` — training data (same dataset)
3. **8.5 GB** — `/root/nanoGPT/out-fineweb-760m/ckpt.pt` — the checkpoint

You have **68 GB of duplicate training data** (same FineWeb dataset in two places). If you want to free space:

```bash
# Remove duplicate dataset (keep the one nanoGPT uses)
rm -rf /root/zz/datasets/fineweb-edu    # saves 40 GB

# Or remove both if done training
rm -rf /root/nanoGPT/data/fineweb       # saves 28 GB
```

That would free up 40-68 GB. Where did you see 240GB?