---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Degenerate GPT-2 Model Output
translated: false
type: note
---

## Comprehensive Summary

### The Problem

The SEC-EDGAR GPT-2 124M model on RunPod was producing **degenerate output** — repetitive loops like "ivableivable..." regardless of serving method, sampling strategy, or prompt. This was a **model quality issue**, not a serving bug.

### Root Cause Analysis

There were **two separate issues** stacked on top of each other:

**1. Old model on RunPod** (`/workspace/model/hf-model/` with vocab_size=50304):

- Properly converted to HF format (correct weight shapes `[768, 2304]`, all biases present)
- But had **padded vocab** from nanoGPT: `vocab_size=50304` (50257 real + 47 padding to nearest 64)
- server.py had a runtime hack to trim embeddings 50304→50257
- **This model produced degenerate output** — the trimming hack was a band-aid, but the underlying trained weights were likely corrupted or from a bad checkpoint

**2. New model from HF** (`lzwjava/sec-edgar-gpt-124m-hf`):

- Has `vocab_size=50257` (correct, no padding) — this is the fix
- But the **safetensors was saved directly from nanoGPT** without proper conversion:
  - Linear weight shapes are **transposed**: `[2304, 768]` instead of `[768, 2304]`
  - **All biases are missing** (ln_1, ln_2, c_attn, c_proj, c_fc, c_proj)
- transformers 5.5.0 on RunPod rejects this with `RuntimeError: shape mismatch`

### What We've Done So Far

1. **Updated local server.py** — removed the 18-line embedding trimming hack, simplified to direct load
2. **Backed up old model** on RunPod → `hf-model-old/`
3. **Downloaded new model** from HF to RunPod → `hf-model/` (7 files, 650MB safetensors)
4. **Server crashed** — transformers refuses to load due to weight shape mismatches
5. **Wrote conversion script** (`scripts/convert_nanogpt_to_hf.py`) that:
   - Transposes linear weights from `[out, in]` to `[in, out]`
   - Adds zero biases for all missing params
   - Saves proper config.json with transformers metadata
   - Copies tokenizer files

### What Still Needs To Be Done

1. **Run the conversion script on RunPod** to produce `hf-model-converted/`
2. **Replace `hf-model/`** with the converted version
3. **Restart the server** with the new model
4. **Test generation** — verify no more degenerate loops
5. **Optionally** re-upload the corrected model to HF so it's properly formatted for anyone

### Key Architecture Notes

| Component | Details |
| ----------- | --------- |
| RunPod GPU | RTX 2000 Ada 16GB (EU-RO-1) |
| Server | FastAPI + transformers on port 8888 |
| Nginx | 8081→8888 reverse proxy |
| Model | GPT-2 124M, 12L, 768d, 12 heads, 1024 context |
| Vocab | 50257 (standard GPT-2, no padding) |
| API | OpenAI-compatible `/v1/completions` + `/v1/chat/completions` |

Want me to run the conversion on RunPod and bring the server up?
