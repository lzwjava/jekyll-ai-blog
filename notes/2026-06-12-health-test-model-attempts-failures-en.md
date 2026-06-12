---
audio: false
generated: true
image: false
lang: en
layout: post
title: Health Test Model Attempts Failures
translated: false
type: note
---

Here's what happened across all three attempts:

## Health Test Summary

### Attempt 1: `unsloth/Qwen3-8B` (4-bit, 7.5GB)

- **Status**: KILLED — download too slow
- **Issue**: HuggingFace download at ~300KB/s, would take ~7 hours for 7.5GB
- hf-mirror.com slightly faster (~470KB/s) but still ~4.5 hours

### Attempt 2: `Qwen/Qwen3.5-9B` (cached, 18GB)

- **Status**: FAILED — wrong model type
- **Issue**: Qwen3.5-9B is a **vision-language model** (Qwen3VLProcessor), not a text-only model. Unsloth loaded it but `tokenizer.vocab_size` doesn't exist on the VL processor.

### Attempt 3: `Qwen/Qwen3-4B-FP8` (cached, 4.9GB)

- **Status**: KILLED — hung during load
- **Issue**: FP8 quantized models aren't compatible with Unsloth's 4-bit BNB loading pipeline. Process used 31% CPU but only 309MB GPU — stuck in weight conversion.

## What Actually Works (confirmed)

- All Python imports: ✅ torch 2.10+cu128, unsloth, datasets, trl, peft, frontmatter, tiktoken
- CUDA: ✅ RTX 4070 detected, 11.5GB available
- Dataset: ✅ 21,234 train + 200 eval loaded correctly
- Chat template: ✅ works

## Root Problem

No compatible model is cached locally. The correct model (`unsloth/Qwen3-4B-unsloth-bnb-4bit` or `unsloth/Qwen3-8B-unsloth-bnb-4bit`) needs to be downloaded, but HF is slow right now.

## Options

1. **Download overnight**: `huggingface-cli download unsloth/Qwen3-4B-unsloth-bnb-4bit` — ~4GB, ~3-4hrs at current speed
2. **Use Qwen3-0.6B** (tiny, fast download, good for pipeline validation)
3. **Use a model that's already cached** — but none of the cached ones (Qwen3.5-9B-VL, Qwen3-4B-FP8, Mistral-Small-3.2) are compatible with the Unsloth SFT pipeline as-is
4. **Wait for better network conditions**

Want me to start the Qwen3-4B download in the background so it's ready by tomorrow? Or try the 0.6B model for a quick pipeline validation first?
