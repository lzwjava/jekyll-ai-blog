---
audio: false
generated: true
image: false
lang: en
layout: post
title: SPGISpeech Training Status Update
translated: false
type: note
---

Here's the full status of the SPGISpeech financial audio model training:

## Latest Commit

**`a503fb5`** — just a `.gitignore` update (added `spgispeech/checkpoints/` to ignored list). The actual training code lives in commit `2167e5c`.

## What Was Built

**Scripts** (both committed):

- `spgispeech/train_whisper.py` — 336 lines, Whisper fine-tuning pipeline
- `spgispeech/train_cmd.sh` — launcher with `--model small --batch-size 16 --grad-accum 2 --lr 1e-5 --epochs 3`

**Architecture** — Custom pyarrow-backed `SPGISpeechDataset` (no HF `datasets` Audio, avoids torchcodec dep hell):

- Builds an index `[(shard_idx, row_group, offset)]` over 12 parquet files (42 GB)
- Caches row groups in memory (~1000 samples each), cycles through ~78 row groups per epoch
- soundfile for WAV decoding from embedded bytes
- `dataloader_num_workers=0` (shared state in Dataset cache)

**Training config**: whisper-small (244M params), effective batch 32, fp16, gradient checkpointing, eval+save every 500 steps, WER metric, TensorBoard logging.

## Where Training Actually Stands

**The training was started but killed after 10 steps.** From the TensorBoard log:

| Step | Loss | Grad Norm | LR | Epoch |
|------|------|-----------|----|-------|
| 5 | 2.1592 | 46.0 | 0.0 | 0.0005 |
| 10 | 2.3147 | 76.0 | 0.0 | 0.0010 |

- Still in warmup phase (LR = 0)
- Loss hadn't converged yet
- No model checkpoints saved (save-steps=500, so first save at step 500 was never reached)
- No `train_log.json` was written
- Only checkpoint artifact: a single TensorBoard events file

**What you have vs what you need to run:**

```
spgispeech/
├── train_whisper.py       # committed
├── train_cmd.sh           # committed
├── explore.py             # committed
├── data/S/                # 12 parquet, 42 GB — fully present
├── .venv/                 # exists, deps installed
└── checkpoints/runs/      # 1 aborted tensorboard run (10 steps)
```

## To Resume

```bash
cd /mnt/data/zz/spgispeech && source .venv/bin/activate

# In tmux:
tmux new-session -s whisper \; send-keys 'cd /mnt/data/zz/spgispeech && source .venv/bin/activate && python3 train_whisper.py --model small --batch-size 16 --grad-accum 2 --lr 1e-5 --epochs 3 --save-steps 500 --eval-steps 500 --logging-steps 50 --eval-samples 500 --test-samples 2000' Enter
```

The dataset, venv, and code are all ready — just needs to actually be launched and left running (~24-30h for 3 epochs). Want me to kick it off?
