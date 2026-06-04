---
audio: false
generated: true
image: false
lang: en
layout: post
title: Excess Data, Undertrained Model
translated: false
type: note
---

Here's the situation:

```
DATA ALREADY ON DISK (nanochat cache)
  Location: ~/.cache/nanochat/base_data_climbmix/
  Files:    176 parquet shards (fineweb-edu format)
  Size:     374 GB
  Docs:     ~138M documents
  Tokens:   ~164B tokens (estimated, ~4 chars/BPE token)

TRAINING vs DATA
  Used in training:    0.655B tokens  (10k steps x 65,536 batch)
  Chinchilla optimal:  5.7B tokens   (20x params for 286M model)
  Already on disk:     164B tokens   (28x Chinchilla, 250x what was used)

VERDICT: You don't need more data. You have 164B tokens sitting on disk
and only used 0.655B of them (0.4%).
```

The fix is to train longer, not download more. For Chinchilla-optimal training:

```
Target:     5.7B tokens
Batch size: 65,536 tokens/step
Steps needed: 5.7B / 65,536 = ~87,000 steps
Time:       87,000 * 1.18s = ~28.5 hours
```

Or if you want to go aggressive and use more of the data:

```
10B tokens:  ~153k steps  (~50 hours)
20B tokens:  ~305k steps  (~100 hours)
```

Want me to check the nanochat dataset.py to confirm it'll correctly loop through all 176 shards with more iterations, or do you want to set up a longer training run?
