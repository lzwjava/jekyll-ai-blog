---
audio: false
generated: true
image: false
lang: en
layout: post
title: Download and Tokenize 100GB Code
translated: false
type: note
---

Wget works: 273MB in 28s (~10 MB/s). 100GB will take ~3 hours.

Both scripts are ready and tested. Here's the summary:

================================================================
FILES CREATED IN /mnt/data/zz/
================================================================

/mnt/data/zz/scripts/download/download_github_code.py

- Downloads ~100GB of code parquet shards from HuggingFace
- Resumable (skips already-downloaded files)
- Output: /mnt/data/zz/datasets/github-code/*.parquet

/mnt/data/zz/scripts/extract/tokenize_github_code.py

- Tokenizes parquet -> nanoGPT binary shards (.npy)
- GPT-2 BPE, 100M tokens per shard
- Output: /mnt/data/zz/datasets/github-code-tok/

================================================================
RUN THESE IN TMUX (one at a time)
================================================================

Step 1 — Download (~3 hours):

  python3.11 /mnt/data/zz/scripts/download/download_github_code.py

Step 2 — Tokenize (~1 hour):

  python3.11 /mnt/data/zz/scripts/extract/tokenize_github_code.py

================================================================
NOTES
================================================================

- The dataset has 1126 shards, each ~285MB with ~100K code files
- 100GB = ~350 shards = ~129B tokens (way more than needed for 760M)
- Columns: content, repo_name, path, license, size (30 languages)
- One test shard already downloaded and verified working
