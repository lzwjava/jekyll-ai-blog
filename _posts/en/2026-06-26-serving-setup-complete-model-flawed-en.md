---
audio: false
generated: true
image: false
lang: en
layout: post
title: Serving Setup Complete, Model Flawed
translated: false
type: note
---

## Summary

### ✅ HuggingFace Upload — DONE
All files uploaded to https://huggingface.co/lzwjava/sec-edgar-gpt-124m. Used Aliyun HK relay for the 475MB model.safetensors (Mac→HK 30min SCP, HK→HF 12min upload). MD5 verified identical.

### ✅ RunPod Serving Infrastructure — DONE
- RunPod: `ssh -p 28484 -i ~/.ssh/id_ed25519 root@213.173.110.200`
- RTX 2000 Ada (16GB), 48 CPU cores, 251GB RAM
- FastAPI server running at `/workspace/model/server.py` on port 8080
- OpenAI-compatible API (`/v1/completions`, `/v1/chat/completions`, `/v1/models`)
- GGUF also converted to `/workspace/model/sec-edgar-gpt-124m.gguf` (624MB) + llama-server at `/workspace/llama-b9811/`

### ⚠️ GGUF Conversion — Solved (but not needed now)
Major learnings about `gguf` Python library's shape convention:
- **Writer reverses shapes**: `ti.shape[n_dims - 1 - j]` — numpy (a,b) → file [b,a]
- `token_embd.weight`: pass numpy as-is (auto-handled by gguf)
- Linear weights: need manual `.T` transpose (HF [out,in] → [in,out])
- `output.weight`: pass as-is (same as token_embd)
- `tokenizer.ggml.merges`: must be space-separated ("Ġ t"), NOT concatenated ("Ġt")
- `tokenizer.ggml.model` key is required
- Vocab must match actual tokens (50257, not padded 50304)
- `tokenizer.ggml.pre = "default"` (b9811 binary doesn't support "gpt2" pre-tokenizer)

### ❌ Model Quality Issue — NOT a serving problem
The model produces degenerate output ("ivableivable..." loops) regardless of:
- Serving method (transformers direct, llama.cpp, FastAPI)
- Sampling strategy (greedy, top-k, temperature)
- Prompt used

Top-1 next-token probabilities are flat (~0.01-0.002) with no clear winner, and the top tokens are suffix fragments ("em", "ivable", "igned"). This indicates the model didn't converge properly during training despite the reported 2.28 validation loss. The 1-epoch, 124M-parameter training on RTX 4070 may have had issues (learning rate, data preprocessing, etc.).

### What to do next
The serving infrastructure is ready — once you have a better-trained model checkpoint, just:
```bash
# On RunPod:
cd /workspace/model
# Replace hf-model/ with new checkpoint, then:
python3 server.py  # OpenAI-compatible API on :8080
```
