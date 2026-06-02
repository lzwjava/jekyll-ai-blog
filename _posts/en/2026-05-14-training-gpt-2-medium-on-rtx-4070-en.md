---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training GPT-2 Medium on RTX 4070
translated: false
type: note
---

Here's what the web sources say about training nanoGPT GPT-2-medium (350M) on an RTX 4070 (12GB) and the loss you can expect.

## Expected loss targets

Karpathy's nanoGPT README reports these from-scratch OpenWebText results:
- **GPT-2 (124M)**: train ~3.11, val ~3.12
- **GPT-2-medium (350M)**: train ~2.85, val ~2.84

The METR / nanoGPT-speedrun "medium track" uses **val loss 2.92** as the GPT-2-medium baseline target (Karpathy's 350M llm.c run).

## Reality check on hardware

- Reference recipe: 8× A100 40GB, ~4 days for the 124M; the 350M is several× heavier.
- Reported single-GPU runs: a user on an **RTX 4090** measured ~5 s/iter on the medium config (12 layers, 12 heads, 768 emb — actually closer to the 124M config), getting ~28% MFU and projecting ~35 days for the full 600k iterations. An actual 350M (24 layers, 16 heads, 1024 emb) will be meaningfully slower and tighter on memory.
- RTX 4070 has only **12 GB VRAM** vs the 4090's 24 GB and A100's 40 GB. Even the 124M model uses ~11–12 GB at default settings, so 350M will not fit out of the box.

So: training GPT-2-medium to the published ~2.85 loss on a single 4070 is *technically possible* but practically takes **weeks-to-months** of continuous training and aggressive memory tricks. Most people instead train the **124M** to ~3.1 in days, or **finetune** the released 350M weights.

## Config changes to fit 350M on a 4070

Defaults in `config/train_gpt2.py` are `batch_size=12, block_size=1024, grad_accum=40` → ~0.5M tokens/step (designed for 8 GPUs). On one 4070 you'd want roughly:

```python
# config/train_gpt2_medium_4070.py
n_layer = 24
n_head = 16
n_embd = 1024
block_size = 1024
batch_size = 1            # micro-batch — start here, raise to 2 if it fits
gradient_accumulation_steps = 480   # keep ~0.5M tokens/step
dtype = 'bfloat16'        # Ada supports bf16 natively
compile = True            # torch.compile for ~20-30% speedup
# PyTorch 2.x SDPA = Flash Attention automatically on Ada
```

Additional VRAM levers, in order of preference:
1. `dtype='bfloat16'` (must — fp32 won't fit).
2. PyTorch 2 SDPA gives Flash-Attn-equivalent kernels for free.
3. **Gradient checkpointing** — nanoGPT doesn't ship it; you'd patch `Block.forward` with `torch.utils.checkpoint.checkpoint`. Cuts activation memory ~2–3× at ~25% speed cost.
4. **8-bit AdamW** via `bitsandbytes` — saves ~2 GB on optimizer states.
5. Drop `block_size` to 512 if still OOM (hurts final loss slightly).
6. Keep weight decay off the LayerNorm/bias params (already in nanoGPT).

## Realistic recommendation

- **Don't train 350M from scratch on a 4070.** Either finetune `gpt2-medium` weights (`init_from='gpt2-medium'`) on your domain — converges in hours, lands near val ~2.85 — or train the **124M** from scratch (`config/train_gpt2.py` with `batch_size=4, grad_accum=120`) and expect val ~3.0–3.1 after ~1–2 weeks.
- If you must do 350M from scratch, expect **~1–3 months** wall-clock, final val loss **~2.85–2.95** if you can hold the ~0.5M-token effective batch.

Sources:
- [karpathy/nanoGPT README — reported losses & configs](https://github.com/karpathy/nanoGPT)
- [Issue #179: Training Time for 1x 4090 GPU](https://github.com/karpathy/nanoGPT/issues/179)
- [Issue #363: Training gpt2 on a single GPU](https://github.com/karpathy/nanoGPT/issues/363)
- [Issue #543: Calculation of Batch Size](https://github.com/karpathy/nanoGPT/issues/543)
- [METR — Evidence on AI R&D Progress from NanoGPT (medium-track 2.92 target)](https://metr.org/notes/2026-04-21-ai-rd-nanogpt-progress/)
- [KellerJordan/modded-nanogpt — bf16 / Muon / Flash tricks](https://github.com/KellerJordan/modded-nanogpt)
- [Deveraux-Parker/nanoGPT_1GPU_SPEEDRUN — single-4090 124M recipe](https://github.com/Deveraux-Parker/nanoGPT_1GPU_SPEEDRUN)
- [HN thread on smallest GPT-2 ~11–12GB VRAM](https://news.ycombinator.com/item?id=22129978)
