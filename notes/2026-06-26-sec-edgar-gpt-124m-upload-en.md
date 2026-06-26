---
audio: false
generated: true
image: false
lang: en
layout: post
title: sec-edgar-gpt 124M Upload
translated: false
type: note
---

Done so far:

- Repo created: https://huggingface.co/lzwjava/sec-edgar-gpt (public)
- Uploaded: config.json, tokenizer.json, tokenizer_config.json, generation_config.json, README.md
- Converted nanoGPT ckpt.pt (from ~/projects/nanoGPT/out-sec-edgar-124m/) to HF safetensors format
- Removed remote .gitignore that was blocking model upload

Remaining:
- model.safetensors (498MB) — you're uploading now, just needs no-proxy to go faster

Model details: GPT-2 124M, trained on SEC-EDGAR filings (1.55B tokens, 47K iters, val_loss 2.28, ~8h on RTX 4070).

After upload completes, verify at: https://huggingface.co/lzwjava/sec-edgar-gpt
