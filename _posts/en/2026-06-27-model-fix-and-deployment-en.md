---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model fix and deployment
translated: false
type: note
---

Done. Here's what happened:

**Root cause**: The old model on RunPod had degenerate output because it was from the original nanoGPT checkpoint (same weights that loop). The new HF model (`lzwjava/sec-edgar-gpt-124m-hf`) has different, properly trained weights — but was saved in raw nanoGPT layout (transposed weights, no biases).

**What was done**:

1. **Local server.py** — removed the 18-line embedding trimming hack
2. **RunPod** — downloaded new model from HF, converted it:
   - Transposed linear weights `[out, in]` → `[in, out]` (GPT2Conv1D layout)
   - Added zero biases (original training used `bias=False`)
   - Vocab stays at 50257 (no padding)
3. **Server restarted** on port 8888, generating real SEC-EDGAR financial text

**Files on RunPod** (`/workspace/model/`):

- `hf-model/` — converted model (622MB, proper transformers layout)
- `hf-model-new/` — raw HF download (backup)
- `hf-model-old/` — original model with degenerate weights (backup)
- `hf-model-trimmed/` — old model trimmed to 50257 (backup)
- `server.py` — updated, no trimming hack

The model gets repetitive on long outputs (typical for 124M), but no more "ivableivable" garbage.
