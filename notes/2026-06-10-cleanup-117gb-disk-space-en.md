---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cleanup 117GB Disk Space
translated: false
type: note
---

Here's the full breakdown of what's eating 184GB:

```
TOP SPACE CONSUMERS:
====================

1. /root/nanoGPT/data/fineweb        28GB  - old nanoGPT FineWeb dataset
2. /root/nanoGPT/out-fineweb-760m     9GB  - old nanoGPT checkpoint
3. /root/zz/datasets/fineweb-edu     40GB  - FineWeb-Edu dataset
4. /root/.cache/nanochat/base_ckpt   19GB  - nanochat cached checkpoints
5. /root/.cache/nanochat/data        2.7GB - nanochat cached data
6. /root/.cache/uv/archive-v0        31GB  - uv package cache (pip equivalent)
7. /root/.cache/pip                   4.7GB - pip cache
8. /opt/rocm-7.2.0                   22GB  - ROCm (NEEDED - keep)
9. /tmp/flash-attention               1.8GB - flash-attention build dir
10. /tmp/torchinductor_root           1.5GB - torch compile cache
```

RECOMMENDED TO DELETE (saves ~117GB):

```bash
# 1. OLD nanoGPT FineWeb dataset (~28GB)
#    You have nanochat now, this is the old pipeline's data
rm -rf /root/nanoGPT/data/fineweb

# 2. OLD nanoGPT checkpoint (~9GB)
#    Replaced by nanochat checkpoints
rm -rf /root/nanoGPT/out-fineweb-760m

# 3. FineWeb-Edu dataset in zz (~40GB)
#    Check if you still need this - was for earlier experiments
rm -rf /root/zz/datasets/fineweb-edu

# 4. uv package cache (~31GB)
#    Safe to delete - uv will re-download on next install
rm -rf /root/.cache/uv

# 5. pip cache (~4.7GB)
rm -rf /root/.cache/pip

# 6. /tmp build caches (~3.3GB)
rm -rf /tmp/flash-attention /tmp/torchinductor_root
```

KEEP:
- `/opt/rocm-7.2.0` (22GB) - ROCm runtime, required for GPU
- `/root/.cache/nanochat/` - your nanochat checkpoints/data cache
- `/root/nanochat/` - your current working project

Want me to run the cleanup commands?
