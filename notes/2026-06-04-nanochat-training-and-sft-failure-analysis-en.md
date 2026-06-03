---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nanochat Training and SFT Failure Analysis
translated: false
type: note
---

Here's the full picture of your training experiments on the RTX 4070 workstation:

============================================================
NANOCHAT (Karpathy's nanochat) — /mnt/data/nanochat
============================================================

Status: COMPLETED (Jun 2, 2026) — but SFT stage produced NaN loss.

What happened:
  1. Downloaded 9 shards (~2B chars) of ClimbMix data to ~/.cache/nanochat/base_data_climbmix/
  2. Trained a BPE tokenizer (32,503 merges, vocab_size=32768)
  3. BASE PRETRAINING (depth=8, ~40M params):
     - 5000 steps, device_batch_size=4, total_batch_size=32768
     - val_bpb: 3.14 -> 0.99 (healthy convergence!)
     - Best val_bpb: 0.9909 at step 5000
     - Model saved: ~/.cache/nanochat/base_checkpoints/d8/model_005000.pt (320MB)
     - Speed: ~103,700 tok/sec, ~26 min total training
  4. BASE EVAL — scores on benchmarks:
     - ARC-Easy: 25.42%  (random = 25%)
     - ARC-Challenge: 24.91%  (random = 25%)
     - MMLU: 25.19%  (random = 25%)
     - GSM8K: 0.00%
     - HumanEval: 0.00%
     -> This is expected for a 40M param model — it's basically random.
  5. SFT (Supervised Fine-Tuning):
     - Loaded identity_conversations.jsonl
     - Loss went NaN at step 6! (lr=1.0, way too high)
     - All 188 SFT steps had loss: nan
     - Final val_bpb: 3.9589 (degraded from base 0.99)
     - ChatCORE: 0.0012 (near zero)
     - All eval benchmarks: 0.00%
     -> SFT FAILED due to learning rate explosion

Key issue: The SFT stage learning rate was too high for the tiny 40M model,
causing NaN loss immediately. The base pretraining was actually fine.

============================================================
NANOGPT (Karpathy's nanoGPT) — /mnt/data/nanoGPT
============================================================

Multiple training runs exist:

Data:
  data/fineweb/         — train.bin (6.9GB) + val.bin (12K) + edu_fineweb100B/
  data/openwebtext/     — train.bin (16GB in old format)
  data/shakespeare_char/
  data/shakespeare/
  data/wikipedia_local/

Output checkpoints:
  out-fineweb/ckpt.pt          — 1.49 GB (Apr 30)
  out-gpt2-200m/ckpt.pt        — 2.63 GB (May 15) — GPT-2 200M params
  out-wikipedia/ckpt.pt         — 362 MB (Nov 2025)
  out-helloworld/ckpt.pt        — 129 MB (Apr 28)
  out-shakespeare-char/ckpt.pt  — 129 MB (Apr 23)
  out-shakespeare/              — empty (no checkpoint)

============================================================
HOW TO USE NANOCCHAT TO TRAIN
============================================================

The pipeline is: data -> tokenizer -> pretrain -> SFT -> eval -> chat

1. Quick smoke test (5 min, fits RTX 4070):

   cd /mnt/data/nanochat
   source .venv/bin/activate
   OMP_NUM_THREADS=1 python -m scripts.base_train --depth=8 \
     --device-batch-size=4 --num-iterations=200 --run=smoke

2. Full run with SFT (fix the NaN):

   Edit run_rtx4070.sh, change SFT lr. The base model is already trained
   so you can skip to SFT:

   python -m scripts.chat_sft --max-seq-len=1024 \
     --device-batch-size=4 --total-batch-size=32768 \
     --num-iterations=1500 --run=rtx4070-d8

   But you need to lower the learning rate. Check what chat_sft.py
   accepts for lr args.

3. Chat with your trained model:

   python -m scripts.chat_cli -p "Why is the sky blue?"
   # or web UI:
   python -m scripts.chat_web

4. Scale up — try depth=12 (GPT-1 sized, ~100M params):

   python -m scripts.base_train --depth=12 \
     --device-batch-size=2 --total-batch-size=32768 \
     --num-iterations=5000 --run=rtx4070-d12

============================================================
WHAT TO DO NEXT
============================================================

The immediate fix: SFT NaN. Want me to SSH in and:
  (a) Check chat_sft.py for lr override flags
  (b) Re-run SFT with a sane lr (e.g. 1e-4 instead of 1.0)
  (c) Test the chat CLI with the fixed model?

Or if you want to experiment differently, you could also:
  - Try depth=12 or depth=16 on RTX 4070 (with smaller batch)
  - Use the nanoGPT fineweb checkpoint (~200M) for actual generation
  - Run the RL training stage (scripts/chat_rl.py) after SFT works
