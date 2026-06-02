---
audio: false
generated: true
image: false
lang: en
layout: post
title: Common Causes for 0% GPU Utilization
translated: false
type: note
---

That's not right. GPU-Util at **0%** means the GPU is completely idle — not computing anything.

56GB used = model + optimizer states loaded. But 0% GPU-Util = it's just sitting there waiting.

Common causes:

1. **Data loading bottleneck** — the script is bottlenecked on reading from disk/CPU preprocessing, GPU sits idle waiting for batches
2. **`torch.compile` profiling phase** — first few steps are slow while it traces the graph
3. **Disk I/O** — if fineweb data is on slow storage, batch prep can't keep up with GPU

Quick diagnostic — run `nvidia-smi` again while training is active (in another terminal). Is GPU-Util still 0%?

If yes, it's almost certainly the **data loader**. With `streaming=True` in your `download_fineweb.py`, you're reading from the raw text file every epoch — that's slow. For 1.5B model training, you want the data pre-processed into **binary `.bin` files** that `train.py` can memory-map for fast loading.

Did you run `prepare.py` to convert FineWeb to nanoGPT's binary format? That's the step you're likely missing.
