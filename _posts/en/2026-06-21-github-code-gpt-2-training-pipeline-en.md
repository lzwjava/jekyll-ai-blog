---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Code GPT-2 Training Pipeline
translated: false
type: note
---

Here's the full pipeline summary:

=== /mnt/data/zz — GitHub Code Training Pipeline ===

STEP 1: DOWNLOAD (codeparrot/github-code from HuggingFace)
- Script: scripts/download/download_github_code.py
- Uses wget to pull parquet shards from HF
- Downloaded 38 shards so far (~11 GB), target was 100 GB
- Output: datasets/github-code/train-00000-of-01126.parquet ...

STEP 2: TOKENIZE (GPT-2 BPE via tiktoken)
- Script: scripts/extract/tokenize_github_code.py
- Reads parquet 'content' column, encodes with tiktoken gpt2
- Writes 100M-token .npy shards (uint16)
- First shard = val, rest = train
- Creates symlinks with edufineweb_ prefix so nanoGPT finds them
- Output: datasets/github-code-tok/
  - 140 train shards + 1 val shard
  - 13.97B train tokens, 100M val tokens
  - 27 GB total

STEP 3: TRAIN (nanoGPT, running now in tmux "train")
- Config: nanoGPT/config/train_github_code_124m.py
- GPT-2 124M (12 layers, 12 heads, 768 embd)
- Batch 4 × 1024, grad_accum 8 = 32,768 tokens/step
- 427,000 steps × 32,768 = ~14B tokens (covers all data)
- Currently at iter 14,000 / 427,000 (~3.3%)
- Best val loss: 5.87
- ~5 days estimated to finish
- Checkpoint: out-github-code-124m/ckpt.pt (1.49 GB)

LATEST COMMITS:
  79273b9 feat(training): add GPT-2 124M config for github-code on RTX 4070
  c0672b7 refactor(extract): simplify tokenization logic
  0f9416d chore(finetune): add merge script, gitignore *.gguf
  336bcef Add github-code download and tokenize scripts

NOTE: Only 38 of 1126 parquet shards were downloaded (11 GB of 100 GB target). But the tokenization produced ~14B tokens already, which is exactly what the training config targets. So the pipeline is complete for this run — download more shards later if you want more data.
