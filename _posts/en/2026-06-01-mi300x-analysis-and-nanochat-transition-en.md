---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X Analysis and nanochat Transition
translated: false
type: note
---

Now I have real data. Here's the updated analysis:

---

**MI300X specs (confirmed from Wikipedia):**

- 304 CUs, CDNA 3
- **192 GB HBM3, 5.3 TB/s bandwidth**
- **1307.4 TFLOPS FP16** (2614.9 with sparsity) — faster than H100 (989.4 TFLOPS bf16)
- Supports PCIe 5.0, CXL 2.0

**nanoGPT status: DEPRECATED (Nov 2025)**
Karpathy's README says:

> nanoGPT has a new and improved cousin called nanochat. nanoGPT (this repo) is now very old and deprecated.

**nanochat** (Oct 2025+) is the successor. Key differences:

- Uses `--depth` as single dial — auto-calculates width, heads, LR, weight decay, training horizon
- `model_dim = depth * 64` (aspect ratio), head_dim=128
- GQA (Grouped Query Attention), RoPE, RMSNorm, ReLU², Flash Attention 3, value residual
- GPT-2 capability = depth 24-26, costs ~$48 on 8×H100 in 2 hours
- Uses Muon optimizer + AdamW, not just AdamW
- DCLM CORE benchmark for evaluation

**Scaling law update (Sardana et al., ICML 2024 — "Beyond Chinchilla-Optimal"):**

- When accounting for **inference cost**, you should train **smaller models longer** (more tokens/param)
- Quality **continues to improve** even at extreme token/param ratios (up to 10,000 tokens/param!)
- At 14.6B tokens:
  - 760M model → 19,700 tokens/param (extreme over-training, still improving)
  - 1.5B model → 9,700 tokens/param (extreme over-training)
  - 3B model → 4,870 tokens/param (very high, still improving)
  - 7B model → 2,086 tokens/param (moderate)

**Revised recommendation:**

Given that the paper shows quality keeps improving at extreme token/param ratios, and MI300X has 192 GB VRAM:

| Model | Params | tok/param | VRAM (train) | Fits? | Quality |
|-------|--------|-----------|-------------|-------|---------|
| 760M | 760M | 19,700 | ~22 GB | ✅ | Good, but small capacity |
| 1.5B | 1.5B | 9,700 | ~44 GB | ✅ | Better — good balance |
| 3B | 3B | 4,870 | ~88 GB | ✅ | Best capacity, still improving |
| 7B | 7B | 2,086 | ~172 GB | ✅ tight | Largest, but may under-train |

**The "Beyond Chinchilla" paper changes my recommendation**: since quality keeps improving at extreme ratios, **3B is clearly the sweet spot** — it has the largest capacity that still gets meaningful over-training (4,870 tok/param), fits comfortably in 192 GB, and leaves room for large batch sizes.

**However**, if you want to use nanochat's modern architecture (GQA, RoPE, Muon optimizer, etc.), you'd need to port your data to nanochat's format. The nanoGPT codebase is 3 years old.

**Two paths forward:**

1. **Stay with nanoGPT** — write a new `train_fineweb_3b.py` config, use your existing data as-is. Faster to start, older architecture.

2. **Switch to nanochat** — better architecture, auto-tuned hyperparams, but need to reformat data and adapt the codebase.

Which do you prefer?
