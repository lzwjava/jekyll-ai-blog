---
audio: false
generated: true
image: false
lang: en
layout: post
title: 124M Model Smoke Test Passed
translated: false
type: note
---

Smoke test passed clean. Results:

- 16 train shards + 1 val shard loaded
- 123.59M params, no VRAM issues
- ~700ms/iter (no compile), ~12.8% MFU
- Loss: 11.0 → 5.8 in 25 steps (learning)

With compile=True the full config should be a bit faster. Full run = 47,400 steps × ~32,768 tokens/step ≈ 1.55B tokens ≈ 1 epoch.

Here's the command:

```
cd /mnt/data/nanoGPT && python3 train.py config/train_sec_edgar_124m.py
```

Config created:

- `/mnt/data/nanoGPT/config/train_sec_edgar_124m.py` (full, 47.4k steps, compile=True)
- `/mnt/data/nanoGPT/config/train_sec_edgar_124m_smoke.py` (smoke, 25 steps)

I also patched train.py to fall back to `train_*.npy` / `val_*.npy` glob when `edufineweb_*.npy` isn't found, so it picks up your sec-edgar shard naming.
