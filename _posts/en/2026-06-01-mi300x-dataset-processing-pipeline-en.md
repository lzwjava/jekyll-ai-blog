---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X Dataset Processing Pipeline
translated: false
type: note
---

All done. Here's the summary:

Server: root@129.212.187.36 (MI300X, Ubuntu)
Installed: huggingface_hub 1.17.0 (with `hf` CLI)
Downloaded: lzwjava/zz → /root/zz (424K, 37 files)

Contents:
  scripts/download/   — FineWeb/Wikimedia download scripts (incl. hf-mirror for China)
  scripts/extract/    — Parquet extraction, GPT-2 BPE tokenization
  scripts/analysis/   — Training duration, metric evaluation
  scripts/deepseek/   — DeepSeek-V2-Lite inference (4-bit, 12GB VRAM)
  logs/               — Training logs (fineweb, openweb, do_fineweb, gen1/2)
  datasets/           — Dataset storage placeholder
  requirements.txt    — Python deps

The HF token was used for the download. The repo is your dataset processing + training pipeline toolkit — ready to use on that MI300X box.
