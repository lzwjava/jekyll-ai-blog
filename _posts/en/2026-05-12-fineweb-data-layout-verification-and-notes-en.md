---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb Data Layout Verification and Notes
translated: false
type: note
---

Layout is correct: `edufineweb_val_000000.npy` (val) + train 1..1407, which matches nanoGPT's expected format.

Two minor things to be aware of:

1. **You have ~140.7B tokens, not 100B.** 176 input parquets is more than the `sample-100BT` subset alone (typically ~150). Check if the input dir mixes the 100BT sample with another snapshot — extra data won't hurt training, just means the dir name is now a misnomer.

2. **The last shard is partial (36.3M tokens).** Fine for nanoGPT's loader, but if you ever resume tokenization, the script overwrites shard 0 (line 75-76 just warns), so a re-run from scratch would clobber `val_000000`.

Otherwise, good to go — point your training config at `/mnt/data/nanoGPT/data/fineweb/edu_fineweb100B`.