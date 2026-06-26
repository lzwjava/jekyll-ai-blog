---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix model by removing trimming hack
translated: false
type: note
---

Here's my analysis:

## Current State (on RunPod)

The model at `/workspace/model/hf-model/` has **vocab_size: 50304** — that's the raw nanoGPT padded vocab (50257 + padding to nearest 64 boundary for CUDA efficiency). The server.py has a runtime hack to trim embeddings 50304→50257 at load time. This was the root cause of the degenerate output — the weight mapping was corrupted by that trimming.

## New Model (HF: lzwjava/sec-edgar-gpt-124m-hf)

**vocab_size: 50257** — properly converted, standard GPT-2 vocab. Same architecture (124M, 12 layers, 768 hidden, 1024 context). No padding, no trimming needed. This is why it works.

## What Changes in server.py

1. **Remove the entire embedding trimming block** (lines 19-31) — no longer needed, new model has correct vocab
2. **Keep everything else the same** — MODEL_DIR, API endpoints, sampling params all stay
3. **Download the new model** to RunPod — replace `/workspace/model/hf-model/` contents

The server.py becomes simpler: load model, serve. No hacks.

Want me to proceed with:

1. Update the local `server.py` to remove the trimming hack
2. SSH into RunPod, download the new model from HF, and restart the server?

Or do you want to do it step by step?
