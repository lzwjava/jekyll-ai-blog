---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training checkpoint saved and data copied
translated: false
type: note
---

Done.

**Training confirmed alive through the eval + checkpoint:**
- `iter 500: train 6.3077 | val 6.2557` — checkpoint saved: `out-wikipedia/ckpt.pt` (344 MiB)
- Process 670206 still running (etime 02:55), GPU 11,662 MiB used / 178 MiB free
- Step time 323 ms steady (`~1339ms` on the eval iter only)

**Data copied to `/mnt/data/igpt/data/wikipedia/`** — the dir is now self-contained:

| file | size | status |
|---|---|---|
| `train.bin` | 171,940,466 B | already present, md5 `abd9f26f…` matches nanoGPT source |
| `val.bin` | 118,116 B | already present, md5 `cc47f9dc…` matches |
| `meta.pkl` | 73 B | already present (gpt2 BPE, vocab 50257) |
| `train_wikipedia.txt` | 435,797,227 B | **copied** from `/mnt/data/nanoGPT/data/wikipedia_local/`, md5 `9fe89b7e…` matches |
| `prepare.py` | 4,797 B | **copied** (provenance/recipe) |
| `readme.md` | 489 B | **copied** |

`data/` is git-ignored, so none of this shows up in `git status` (only `.gitignore` + `train.py` are modified there).

One thing worth flagging: the `mfu` numbers (~1800%) are impossible — `train.py` computes `params*6*tokens_per_iter/(dt*1e12)`, which yields achieved TFLOP/s, not MFU. The real figure is roughly 18 TFLOP/s out of the card's peak (so ~1–2% MFU); the missing divisor is the GPU's peak FLOP/s. Harmless for training, just a mislabeled metric.