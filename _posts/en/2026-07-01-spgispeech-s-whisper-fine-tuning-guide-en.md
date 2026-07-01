---
audio: false
generated: true
image: false
lang: en
layout: post
title: SPGISpeech S Whisper Fine-Tuning Guide
translated: false
type: note
---

All tested and working. Here's the summary:

**SPGISpeech S — ready for Whisper fine-tuning**

| Item | Value |
| --- | --- |
| Train | 77,073 samples |
| Validation | 39,304 (eval on 500) |
| Test | 39,341 (eval on 2,000) |
| Audio | 16kHz mono WAV, embedded in parquet |
| Model | whisper-small (244M params) |
| VRAM | ~7-8 GB (batch 16, grad_accum 2, fp16) |
| Est time | ~24-36h for 3 epochs |

The script is at `/mnt/data/zz/spgispeech/train_whisper.py`. Run with:

```bash
cd /mnt/data/zz/spgispeech && source .venv/bin/activate

# --- in tmux (recommended) ---
tmux new-session -s whisper \; send-keys 'cd /mnt/data/zz/spgispeech && source .venv/bin/activate && python3 train_whisper.py --model small --batch-size 16 --grad-accum 2 --lr 1e-5 --epochs 3 --save-steps 500 --eval-steps 500 --logging-steps 50 --eval-samples 500 --test-samples 2000' Enter

# --- or using the shell script ---
# tmux new-session -s whisper \; send-keys 'cd /mnt/data/zz/spgispeech && source .venv/bin/activate && bash train_cmd.sh' Enter
```

**Options you may want to tweak:**

- `--model medium` — if you want better accuracy (might need `--batch-size 8`)
- `--freeze-encoder` — faster training, only trains the decoder
- `--epochs 1` — quick run first to validate WER improvement
- `--resume` — resume from last checkpoint if interrupted

Monitor with `tensorboard --logdir /mnt/data/zz/spgispeech/checkpoints` or tail the log.
