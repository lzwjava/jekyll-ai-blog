---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setting Up NanoGPT on AMD MI300X
translated: false
type: note
---

Here's what we did:

1. SSH'd into root@129.212.187.36 (AMD MI300X, Ubuntu)

2. Installed HF CLI
   - `pip3 install -U --break-system-packages 'huggingface_hub[cli]'`
   - huggingface_hub 1.17.0

3. Downloaded lzwjava/zz from HuggingFace
   - `hf download lzwjava/zz --local-dir /root/zz`
   - 37 files, 424K (non-git download)

4. Generated SSH key for GitHub
   - ed25519, label `lzwjava-amd-devcloud`
   - Added to GitHub

5. Cloned nanoGPT with full history
   - `git clone git@github.com:lzwjava/nanoGPT.git`
   - 255 commits at /root/nanoGPT

6. Recloned zz as proper git repo from HF
   - Deleted non-git `hf download` version
   - `git clone https://huggingface.co/lzwjava/zz`
   - Set up remotes: origin → GitHub (archived), hf → HuggingFace (active)
   - 18 commits, full history

7. Opened Zed via `zed ssh://root@129.212.187.36//root/zz`

8. Smoke tested download script
   - `plan_and_download_fineweb_gpt3_amd.py` — works, 267 MB/s

9. User ran full download in tmux
   - 18 shards, 39 GB, ~10.4B tokens of FineWeb-Edu
   - Done

10. Installed tokenize deps
    - tiktoken, numpy, pyarrow, tqdm

11. Smoke tested tokenize script
    - `tokenize_fineweb_gpt3.py` — works, ~30-50M tok/s
    - Output: uint16, GPT-2 BPE, EOT prefix ✓

Current state:
  /root/nanoGPT   — nanoGPT repo (255 commits)
  /root/zz        — dataset repo (18 commits, 39GB parquet data)
  Next:           — tokenize into .npy shards, then train