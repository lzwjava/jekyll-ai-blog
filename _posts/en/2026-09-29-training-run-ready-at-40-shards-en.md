---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training run ready at 40 shards
translated: false
type: note
---

Download is at 40/171 shards (~30 min to finish). Here's where things stand:

## ✅ Everything works — here's the plan

**1. Tokenizer** — trained on ClimbMix (32k vocab, 37s), compression on-par with GPT-4, better than GPT-2 on code/math.

**2. Model verified: `d18` (702M params) is the max that fits** on this 4070:

| Config | Peak VRAM | Throughput | MFU |
|---|---|---|---|
| bs=1, seq=1024 | 8.87 GB | 7,100 tok/s | 50% |
| **bs=2, seq=1024** ✅ | **9.01 GB** | **8,100 tok/s** | **57%** |
| bs=4 | OOM ❌ | — | — |

**3. Recommended run** (auto-scaling defaults):
- `--depth=18 --max-seq-len=1024 --device-batch-size=2`
- data:params ratio = 12 → **~3.9B tokens** → **~5.6 days** at 8,100 tok/s
- auto batch ≈ 1M tokens/step, ~3,890 steps

## Command (ready once download finishes)

```bash
cd /mnt/data/nanochat && export NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache
./.venv/bin/python -m scripts.base_train \
  --depth=18 --max-seq-len=1024 --device-batch-size=2 \
  --tracker=none --run=d18-climbmix
```

## One decision for you — training budget

| Budget | Tokens | Time | Notes |
|---|---|---|---|
| Quick validation | ~0.5B | ~17 h | sanity-check loss curve |
| Half-Chinchilla | ~2B | ~2.9 days | reasonable |
| **Full (recommended)** | **~3.9B** | **~5.6 days** | default ratio=12 |

The full run is ~5.6 days on this single GPU — that's the honest cost of a 700M model. 

Do you want me to **launch the full ~3.9B run** once the download completes (I'll set it up with checkpoint saving + a `nohup` log), or start with a **shorter validation run** first to confirm the loss is dropping cleanly?