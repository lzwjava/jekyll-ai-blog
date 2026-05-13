---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Math for GPT-2 Medium on GPU
translated: false
type: note
---

Yes, GPT-2 medium (350M) **fits on a 12 GB 4070**, but it's tight and slow.

**Memory math (bf16 mixed precision, AdamW):**
- Params + grads + Adam(m,v) ≈ 350M × 16 B ≈ **5.6 GB** static
- Activations at `batch_size=1, block_size=1024, n_layer=24` ≈ **~3–4 GB**
- Total ≈ **9–10 GB** → fits in 12 GB with headroom

**Required config tweaks (vs your current):**
```python
n_layer = 24
n_head = 16
n_embd = 1024

batch_size = 1                  # was 4
gradient_accumulation_steps = 512  # was 128 → keeps ~524K tokens/step
learning_rate = 3e-4            # GPT-3 medium uses lower LR than small
min_lr = 3e-5
```

**Caveats:**
- **Time:** medium is ~2.8× more FLOPs per token. Your current run is ~22h for 10B tokens at 12% MFU → medium would be **~60–70h** for the same 10B tokens, likely worse MFU at `batch_size=1`.
- Chinchilla-optimal for 350M is ~7B tokens, so 10B is fine, but expect ~3 days of GPU time.
- If OOM, try `batch_size=1, block_size=512` first to confirm headroom, then increase.

If you want, I can write `config/train_fineweb_gpt2_medium.py` ready to run. Want me to?