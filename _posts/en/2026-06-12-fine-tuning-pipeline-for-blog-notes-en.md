---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fine-Tuning Pipeline for Blog Notes
translated: false
type: note
---

## Comprehensive Summary — Fine-tuning Pipeline for lzwjava's Notes

### Goal

Fine-tune an LLM on lzwjava's ~16k blog notes (en + zh) from `jekyll-ai-blog` to learn his writing voice and answer style.

---

### 1. Created `/mnt/data/zz/finetune/` Pipeline

**Dataset extraction** (`build_dataset.py`):

- Parsed Jekyll markdown with YAML front matter from `_posts/en/` and `_posts/zh/`
- Cleaned Liquid tags `{% %}`, kramdown `{: .class}`, image refs, captions
- No filtering — included AI-generated posts as requested
- Output: `{question: title, answer: body}` conversation format

| Stat | Value |
|---|---|
| English posts | 10,726 |
| Chinese posts | 10,708 |
| Total examples | 21,434 |
| Total tokens | 25.1M |
| Avg tokens/example | 1,169 |
| Train split | 21,234 |
| Eval split | 200 |
| Skipped (too short) | 30 |

**Training script** (`train.py`):

- Went through 3 iterations before working:
  1. **Unsloth-based** — Triton kernels segfaulted on RTX 4070 (torch 2.10+cu128, Triton 3.6.0)
  2. **Unsloth with `UNSLOTH_DISABLE_TRITON=1`** — still segfaulted
  3. **Pure transformers + peft** — works perfectly
- Final stack: `transformers` loader + `peft` LoRA + `trl.SFTTrainer`
- Config: Qwen3-4B, 4-bit, LoRA r=32, 66M trainable params (1.6%)
- Fixed TRL 0.24 API: `processing_class` instead of `tokenizer`, no `max_seq_length` in SFTConfig
- Disabled eval during training (OOM on full-vocab logits computation)
- Save LoRA adapter only (4-bit can't merge to 16-bit in-memory)

**Supporting scripts**:

- `eval.py` — compare fine-tuned vs base on held-out titles
- `export_gguf.py` — GGUF export for ollama/llama.cpp
- `README.md` — full usage guide
- `requirements.txt` — pip dependencies

---

### 2. Model Download Saga

| Model | Size | Attempt | Result |
|---|---|---|---|
| `unsloth/Qwen3-8B` (4-bit) | 7.5GB | Direct + hf-mirror | Too slow (300-470KB/s), killed |
| `Qwen/Qwen3.5-9B` (cached) | 18GB | Direct load | VL model, wrong type |
| `Qwen/Qwen3-4B-FP8` (cached) | 4.9GB | Direct load | Hung with Unsloth, incompatible |
| **`unsloth/Qwen3-4B-unsloth-bnb-4bit`** | **3.4GB** | **curl direct** | **Works** |

Final download: Direct from `huggingface.co` at ~37MB/s (network recovered). Manually set up HF cache structure with symlinks since `hf` CLI and `hf-mirror.com` didn't have this model.

---

### 3. Unsloth Triton Investigation

Segfault pattern:

- Crashes at step 0 in both training and inference
- Exit code 139 (SIGSEGV)
- Happens with full LoRA (7 target modules) and minimal LoRA (2 modules)
- `UNSLOTH_DISABLE_TRITON=1` doesn't help
- Environment: torch 2.10+cu128, CUDA 12.8, Triton 3.6.0, RTX 4070 (compute 8.9)

Resolution: Abandoned Unsloth entirely. Pure transformers + peft works at ~1.25s/step.

---

### 4. Git History

```
8292db9  add finetune pipeline for lzwjava notes SFT
9aaa8f3  fix train.py: use pure transformers+peft, fix TRL 0.24 API
```

Pushed to `github.com:lzwjava/zz.git`. JSONL files + output dirs gitignored.

---

### 5. Current Training Status

Started at ~17:18 in a tmux session:

```
Model:      Qwen3-4B-unsloth-bnb-4bit (4-bit, 3.4GB cached)
LoRA:       r=32, 66M params, all projection layers
Dataset:    21,234 examples, 25.1M tokens
Config:     batch 16 (2×8), cosine LR 2e-4, 2 epochs
Steps:      400 / 2,656 (15%)
Loss:       2.86 → 1.70
GPU:        11.5GB, 100% utilization
Checkpoints: step 10, 200, 400 saved
ETA:        ~9 more hours (~04:00 tomorrow)
Output:     /mnt/data/zz/finetune/lzw-notes-lora/
```

---

### 6. Post-Training Plan

```bash
# Test the adapter
python3.11 eval.py

# Export to GGUF for ollama
python3.11 export_gguf.py

# Or serve with vLLM
vllm serve ./lzw-notes-lora --max-model-len 4096
```
