---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinchilla Training Script Commands
translated: false
type: note
---

Checkpoint at step 10,000 already exists. Script is ready:

```
/mnt/data/nanochat/run_rtx4070_chinchilla.sh
```

To run fresh from step 0:

```
bash /mnt/data/nanochat/run_rtx4070_chinchilla.sh
```

To resume from the existing step 10k checkpoint:

```
bash /mnt/data/nanochat/run_rtx4070_chinchilla.sh --resume-from-step=10000
```

What it does:

```
  87,000 steps x 65,536 batch = 5.7B tokens (Chinchilla optimal)
  Checkpoints every 10k steps (crash-safe)
  Eval every 2k steps, samples every 5k steps
  ~28.5 hours on RTX 4070
  Data: 142.6B tokens on disk, only needs 5.7B
```

Run it? Or want to tweak anything first (eval frequency, save frequency, etc.)?
