---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fine-tuning Pipeline Build and Debug
translated: false
type: note
---

## What We Did — Full Summary

### 1. Built the Fine-tuning Pipeline (`/mnt/data/zz/finetune/`)

**Dataset extraction** (`build_dataset.py`):

- Parsed 16,107 Jekyll markdown posts from `~/projects/jekyll-ai-blog/_posts/{en,zh}/`
- Extracted `{title, body}` pairs as SFT conversations
- Cleaned Liquid tags, kramdown attributes, image refs, captions
- 10,726 English + 10,708 Chinese = **21,434 examples**
- **25.1M tokens**, avg 1,169 tokens/example
- 200 held out for eval, 21,234 for training
- Shipped as `notes_sft_train.jsonl` (85MB) + `notes_sft_eval.jsonl` (820KB)

**Training script** (`train.py`):

- Started with Unsloth-based QLoRA, hit Triton segfaults on RTX 4070
- Rewrote to **pure transformers + peft** (no Unsloth kernel dependency)
- Qwen3-4B-unsloth-bnb-4bit, 4-bit quantized, LoRA r=32
- 66M trainable params (1.6% of 4B)
- Smoke tested: 10 steps, 1.25s/step, loss decreasing (2.86→2.11)

**Supporting scripts**:

- `eval.py` — compare fine-tuned vs base on held-out titles (vLLM or transformers)
- `export_gguf.py` — export to GGUF for ollama/llama.cpp
- `README.md` + `requirements.txt`

### 2. Model Download Dance

Tried 4 models before finding what works:

| Model | Size | Result |
| --- | --- | --- |
| `unsloth/Qwen3-8B` (4-bit) | 7.5GB | Download too slow (300KB/s), killed |
| `Qwen/Qwen3.5-9B` (cached) | 18GB | VL model, wrong type |
| `Qwen/Qwen3-4B-FP8` (cached) | 4.9GB | Hung during Unsloth load |
| **`unsloth/Qwen3-4B-unsloth-bnb-4bit`** | **3.4GB** | **Downloaded via curl, works** |

Downloaded from `huggingface.co` at ~37MB/s (speed recovered from earlier 300KB/s). Set up HF cache structure manually with symlinks since `hf` CLI / `hf-mirror.com` didn't have the model.

### 3. Unsloth → Pure Transformers Pivot

Unsloth's Triton kernels segfault consistently on this setup:

- torch 2.10+cu128, CUDA 12.8, Triton 3.6.0, RTX 4070 (compute 8.9)
- Crashes at step 0 in both training and inference
- `UNSLOTH_DISABLE_TRITON=1` didn't help

**Fix**: Dropped Unsloth entirely, used:

- `transformers` for model loading
- `peft` for LoRA (`LoraConfig` + `get_peft_model`)
- `trl.SFTTrainer` with `processing_class` (TRL 0.24 API)

### 4. TRL 0.24 API Fixes

The installed TRL 0.24.0 changed APIs from the docs:

- `tokenizer=` → `processing_class=`
- `SFTConfig` has no `max_seq_length` param
- `torch_dtype=` → `dtype=`
- `warmup_ratio` deprecated (but still works)

### 5. Git Commits

```
8292db9  add finetune pipeline for lzwjava notes SFT
9aaa8f3  fix train.py: use pure transformers+peft, fix TRL 0.24 API
```

Pushed to `github.com:lzwjava/zz.git`. JSONL files gitignored.

### 6. Ready to Run

```bash
cd /mnt/data/zz/finetune && python3.11 train.py
```

- ~55 min on RTX 4070 (2,656 steps × 1.25s/step)
- Saves LoRA adapter to `lzw-notes-lora/`
- Then: `python3.11 export_gguf.py` for ollama, `python3.11 eval.py` to test
