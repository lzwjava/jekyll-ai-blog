---
audio: false
generated: true
image: false
lang: en
layout: post
title: nanoGPT Limited to GPT-2 Models
translated: false
type: note
---

Short answer: **GPT-2 family yes, everything else no — at least not for loading existing weights.** Here's the breakdown.

## What `sample.py --init_from=...` supports

`model.py:230` hard-codes this assertion:
```python
assert model_type in {'gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'}
```

| Model                                 | Params  | Works? | Size to download                                                                                                            |
| ------------------------------------- | ------- | ------ | --------------------------------------------------------------------------------------------------------------------------- |
| `gpt2`                                | 124M    | ✅     | ~500 MB                                                                                                                     |
| `gpt2-medium`                         | 350M    | ✅     | ~1.5 GB                                                                                                                     |
| `gpt2-large`                          | 774M    | ✅     | ~3.2 GB                                                                                                                     |
| `gpt2-xl`                             | 1.5B    | ✅     | ~6.5 GB                                                                                                                     |
| **GPT-3**                             | 175B    | ❌     | OpenAI never released weights. The "gpt3-style" configs in this repo just *train from scratch* using GPT-3 hyperparameters. |
| **Qwen / DeepSeek / Llama / Mistral** | various | ❌     | Different architecture — nanoGPT can't load them as-is.                                                                     |

## Why nanoGPT can't load Qwen/DeepSeek/Llama

nanoGPT's `model.py` implements the original GPT-2 transformer block. Modern open models diverged significantly:

| Component          | GPT-2 (nanoGPT)        | Qwen / DeepSeek / Llama        |
| ------------------ | ---------------------- | ------------------------------ |
| Position embedding | Learned absolute       | **RoPE** (rotary)              |
| Normalization      | LayerNorm              | **RMSNorm**                    |
| Activation         | GELU                   | **SwiGLU**                     |
| Attention          | Standard MHA           | **GQA** (grouped-query)        |
| Tokenizer          | GPT-2 BPE, 50257 vocab | Different BPE, 100K–150K vocab |
| Attention bias     | Yes                    | No                             |

The weight tensor names *and* shapes are different — `from_pretrained` would fail on the first layer.

## Your realistic options

**If you want bigger pretrained text-gen on this box:**
- Stick with `gpt2-xl` (1.5B) — still useful and fits on most GPUs.
- For anything beyond that, use `transformers` directly, not nanoGPT:
  ```python
  from transformers import AutoModelForCausalLM, AutoTokenizer
  tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B")
  m   = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-3B", torch_dtype="auto", device_map="auto")
  ```
  (With `HF_ENDPOINT=https://hf-mirror.com` set — same mirror works for Qwen, DeepSeek, etc.)

**If you want to *train* GPT-3-class models from scratch:**
- That's exactly what the `config/train_gpt2_*.py` and your `out-gpt2-200m` configs are for. nanoGPT is built for this; loading pretrained weights is a side feature.

**If you really want nanoGPT-style code for Llama/Qwen:**
- Karpathy's `llm.c` or `nanollama` / `nano-llama31` (community ports) are the modern equivalents — same minimalist spirit, RoPE + RMSNorm + SwiGLU built in.

TL;DR: for *inference* on big modern models, just use `transformers` with the mirror env vars. nanoGPT shines for training small/medium GPT-2-style models from scratch.
