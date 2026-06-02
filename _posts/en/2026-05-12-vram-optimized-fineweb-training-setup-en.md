---
audio: false
generated: true
image: false
lang: en
layout: post
title: VRAM-Optimized FineWeb Training Setup
translated: false
type: note
---

It's OK — you can run for hours. Summary of what the smoke run showed and what I changed:

  Findings
  - batch_size=8 OOM'd (needed 1.54 GiB more than your 12 GB had). Fixed to batch_size=4 +
  gradient_accumulation_steps=128 — same 524k tokens/step.
  - At batch_size=4, eager mode: ~88 ms/microbatch, ~6.6 GB VRAM (≈5.6 GB headroom).
  - Loss went 11.04 → 10.94 → 10.85 → 10.75 → 10.56 across 4 iters → training is wired up correctly, shards
  load, vocab is right.
  - Extrapolated per-iter at the real grad_accum=128: ~11 seconds/iter.

  Time budget for the real run (max_iters=19073, ~10B tokens seen)
  - Eager (compile=False): ~59 hours (~2.5 days)
  - With compile=True: roughly 20–30% faster after a 1–3 min compile, so ~40–50 hours
  - If you want a shorter run, set --max_iters=5000 --lr_decay_iters=5000 → ~15 hours, ~2.6B tokens seen.

  Run this in another terminal

  cd /mnt/data/nanoGPT
  tmux new -s nano                 # so it survives disconnects
  source venv/bin/activate

  PYTORCH_ALLOC_CONF=expandable_segments:True \
  python -u train.py config/train_fineweb_gpt3.py 2>&1 \
    | tee -a out-fineweb-gpt3/train.log
  # detach: Ctrl-b d        reattach: tmux attach -t nano

  If compile=True errors on your torch/CUDA combo, just re-launch with --compile=False appended.

  Resume after interruption: add --init_from=resume.
