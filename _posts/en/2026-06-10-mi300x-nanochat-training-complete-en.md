---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X NanoChat Training Complete
translated: false
type: note
---

Everything is up and running. Here's the summary:

============================================================
  NANOCCHAT 760M TRAINING - MI300X SETUP COMPLETE
============================================================

WHAT WAS DONE:

  1. Cloned nanochat (Karpathy's LLM training harness)
  2. Set up Python venv with ROCm PyTorch 2.9.1+rocm6.4
  3. Downloaded 31 ClimbMix-400B dataset shards (~25B tokens)
  4. Trained BPE tokenizer (32,768 vocab)
  5. Verified model builds and trains on MI300X
  6. Launched full training run in background

MODEL CONFIG:
  Architecture:  depth=24, dim=1536, heads=12, head_dim=128
  Parameters:    760M (transformer) + 604M (value embeddings) = 1.38B total
  Dataset:       ClimbMix-400B (successor to FineWeb)
  Training:      29,000 steps, batch=524,288 tokens/step
  Tokens:        ~15.2B (Chinchilla-optimal: 20x params)

PERFORMANCE (MI300X):
  Throughput:    ~68,000 tokens/sec
  Step time:     ~7.7 seconds
  MFU:           ~27.5% (SDPA fallback, no FA3 on AMD)
  Peak VRAM:     ~105 GB / 192 GB
  Est. total:    ~62 hours

FILES CREATED:
  /root/nanochat/run_mi300x_d24.sh           # Full pipeline (pretrain + SFT + eval)
  /root/nanochat/run_mi300x_d24_pretrain.sh  # Pretrain only
  /root/nanochat/run_mi300x_d24.log          # Training log (live)

BACKGROUND PROCESS:
  Session: proc_c4c8f9ccdff7
  PID:     272714
  Status:  Running (loss dropping: 10.4 → 9.6 in first 8 steps)

MONITORING:
  tail -f /root/nanochat/run_mi300x_d24.log

CHECKPOINTS:
  ~/.cache/nanochat/base_checkpoints/d24/
  (saved every 5000 steps)

RESUME (if crash):
  ./run_mi300x_d24_pretrain.sh --resume-from-step=<last_step>

AFTER TRAINING:
  python -m scripts.chat_cli -p 'Why is the sky blue?'
  python -m scripts.chat_web
