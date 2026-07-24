---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running nano-vllm on RTX 4070
translated: false
type: note
---

Alright, here's the full picture of your laptop and how to run **nano-vllm**:

---

## Hardware Specs

| Component | Spec |
|-----------|------|
| **GPU** | NVIDIA GeForce RTX 4070 (12GB VRAM) |
| **CUDA Driver** | 13.0 |
| **RAM** | 62 GB |
| **Python** | 3.12.3 ✅ (project requires 3.10–3.13) |

---

## Prerequisites Already Satisfied

- **torch** 2.11.0+cu130 ✅
- **transformers** 5.12.1 ✅
- **triton** 3.6.0 ✅
- **huggingface-cli** ✅

---

## Steps to Run

### 1. Install missing dependencies

Flash Attention and xxhash aren't installed yet. Install them with Python 3.12:

```bash
python3.12 -m pip install flash-attn xxhash
```

### 2. Install nano-vllm (from local source)

```bash
cd /mnt/data/nano-vllm
python3.12 -m pip install -e .
```

### 3. Download a model

The example uses **Qwen3-0.6B** (~1.2GB):

```bash
huggingface-cli download --resume-download Qwen/Qwen3-0.6B \
  --local-dir ~/huggingface/Qwen3-0.6B/ \
  --local-dir-use-symlinks False
```

> **Optional**: You can use any HuggingFace model instead — just update the `path` in `example.py`.

### 4. Run inference

```bash
cd /mnt/data/nano-vllm
python3.12 example.py
```

Or run the benchmark:

```bash
python3.12 bench.py
```

---

## Quick One-Liner

```bash
python3.12 -m pip install flash-attn xxhash && \
cd /mnt/data/nano-vllm && \
python3.12 -m pip install -e . && \
huggingface-cli download --resume-download Qwen/Qwen3-0.6B \
  --local-dir ~/huggingface/Qwen3-0.6B/ \
  --local-dir-use-symlinks False && \
python3.12 example.py
```

---

**Important**: Always use `python3.12` explicitly — the default `python3` is 3.14 which is outside this project's supported range. With 12GB VRAM on the RTX 4070 and only ~2.6GB currently used, you have plenty of room to run even larger models like Qwen3-4B or Qwen3-8B.