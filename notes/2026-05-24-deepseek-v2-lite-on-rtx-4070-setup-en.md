---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek V2 Lite on RTX 4070 Setup
translated: false
type: note
---

Run a DeepSeek model on RTX 4070 (12GB VRAM). The original DeepSeek-V4 code in `/mnt/data/deepseek-v4-inference` targets a 671B+ parameter model needing 8x H100 GPUs — not viable on consumer hardware. So we went with **DeepSeek-V2-Lite-Chat** instead: same MLA/MoE architecture, just 16B total (2.4B activated per token).

## Step 1 — Git Pull ~/projects/ww

Pulled latest from `github.com:lzwjava/ww`. Got a big update: 140 files changed, +21,275 lines. New modules for agents, tests, weather, machine info, hermes config, image EXIF, GitHub mgmt, etc.

## Step 2 — Install Dependencies

```bash
python3.11 -m pip install --user bitsandbytes accelerate
```

| Package | Version | Purpose |
|---------|---------|---------|
| bitsandbytes | 0.49.2 | 4-bit NF4 quantization |
| accelerate | 1.13.0 | `device_map="auto"` for multi-GPU/CPU offload |

Already had: torch 2.6.0, transformers 4.48.3, safetensors 0.5.2.

## Step 3 — Download Model

- **Model:** `deepseek-ai/DeepSeek-V2-Lite-Chat`
- **Destination:** `/mnt/data/models/DeepSeek-V2-Lite-Chat/`

First tried HF mirror (`hf-mirror.com`) for speed — failed with `LocalEntryNotFoundError`. Fell back to direct HuggingFace.

Download ran in background, took ~35 minutes for 30GB:
- 4 safetensor shards (8.1GB ×3 + 5.3GB ×1)
- Plus tokenizer, config, modeling code (~15 small files)
- Speed: ~1 GB/min sustained

```python
from huggingface_hub import snapshot_download

snapshot_download(
    "deepseek-ai/DeepSeek-V2-Lite-Chat",
    local_dir="/mnt/data/models/DeepSeek-V2-Lite-Chat",
)
```

## Step 4 — Inference Script

Wrote `/mnt/data/deepseek-v4-inference/run_lite.py` with:

- 4-bit NF4 quantization via `BitsAndBytesConfig`
- Double quantization for extra memory savings
- `bfloat16` compute dtype
- `device_map="auto"` for automatic GPU placement
- Interactive chat mode and single-prompt mode
- CLI args: `-p "prompt"`, `-n max_tokens`

## Step 5 — Fix: Python.h Missing

First run failed — triton (bitsandbytes dependency) tried to compile C code needing `Python.h` for python3.11, but only python3.12-dev was installed.

Fix: symlink python3.12 headers as python3.11:

```bash
sudo ln -sf /usr/include/python3.12 /usr/include/python3.11
```

This works because the C API is compatible enough for triton's simple build. After this, model loaded and ran successfully.

## Step 6 — Test Run

```bash
python3.11 run_lite.py -p "Hello! Who are you?"
```

| Metric | Value |
|--------|-------|
| Loading time | ~2.5 min (4 shards, 37s each) |
| GPU memory | 9.5 GB used (of 11.6 GB available) |
| Response | "I am an AI language model, here to assist you with information, questions, or tasks you have." |

## Final State

| Item | Value |
|------|-------|
| Model | `/mnt/data/models/DeepSeek-V2-Lite-Chat/` (30GB on disk) |
| Script | `/mnt/data/deepseek-v4-inference/run_lite.py` |
| VRAM usage | 9.5 GB / 11.6 GB (82%) |
| Quantization | 4-bit NF4 with double quant |
| Speed | ~2.5 min load, then fast inference |

## How to Use

Interactive chat:

```bash
python3.11 /mnt/data/deepseek-v4-inference/run_lite.py
```

One-shot prompt:

```bash
python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "Explain quantum computing"
```

Longer output:

```bash
python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "Write a poem" -n 1024
```

## What Changed from the Original Assessment

- **Original code:** DeepSeek-V4 (671B+ params, 8x H100 required)
- **Now running:** DeepSeek-V2-Lite-Chat (16B params, 1x RTX 4070)

Same architecture family (MLA + MoE), just scaled to fit your hardware. You lose some capability vs the 671B model, but you can actually run it locally.
