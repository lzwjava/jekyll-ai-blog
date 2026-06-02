---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing GPU Memory Errors
translated: false
type: note
---

Yes, you're hitting an out-of-memory (OOM) error because even the "125M" nanoGPT-style model with your current settings is pushing the limits of a 12 GB GPU (e.g. 3090/4090/3090 Ti/A6000). Let's break down exactly what's using VRAM and what you should change first.

### Current VRAM Consumption Estimate (at your settings)
- Model size: true ~124M params → ~500–550 MB (in FP16/BF16)
- Optimizer states (AdamW): ~1–1.2 GB
- Gradients: ~500 MB
- Activations (the killer):
  - batch_size = 16
  - block_size = 1024
  - gradient_accumulation_steps = 32
  → Micro-batch of 16 sequences × 1024 tokens = 16 384 tokens per forward/backward pass
  - With 12 layers, 768 dim, 12 heads → activations easily eat 9–11 GB just for one micro-batch

So total → you are very close to or over 12 GB, especially once PyTorch overhead, compile cache, CUDA graphs, etc. kick in.

### What does `batch_size` actually do?
`batch_size` in nanoGPT is the micro-batch size (the number of sequences processed in a single forward/backward pass before gradients are applied).

Your effective (total) batch size is:

effective_batch_size = batch_size × gradient_accumulation_steps
= 16 × 32 = 512 sequences

This 512 is what matters for gradient quality/noise. The micro-batch (16) mostly affects VRAM and speed.

### Best fixes (ranked by effectiveness for your 12 GB card)

| Option | New values | Effective batch | VRAM saved | Effect on training | Recommendation |
|------|------------|------------------|------------|---------------------|----------------|
| 1. Reduce micro-batch only | batch_size = 8<br>gradient_accumulation_steps = 64 | still 512 | ~40–50% less activations → fits comfortably | Almost zero impact on final model | BEST CHOICE |
| 2. Reduce micro-batch a bit more | batch_size = 4<br>gradient_accumulation_steps = 128 | still 512 | even safer, slightly slower | Still negligible difference | If still OOM |
| 3. Reduce both (easier but slightly worse) | batch_size = 8<br>gradient_accumulation_steps = 32 | now 256 | big VRAM save | Slightly noisier gradients, may need 10–20% more steps to converge | Acceptable |
| 4. Reduce model size | n_layer=9 or n_embd=512 | smaller model | huge VRAM save | You lose capacity | Only if you want very fast experiments |

### Recommended config that will definitely fit on 12 GB
```python
batch_size = 8                    # ← main change (was 16)
gradient_accumulation_steps = 64  # ← increase to keep effective batch 512
block_size = 1024                 # keep
# everything else unchanged
```

This will drop activation memory by roughly half and still give you the same gradient quality. Training will be ~10–15% slower in real time (more accumulation steps = more Python overhead), but it will actually run instead of crashing.

### Extra safe mode (if you still OOM after the above)
```python
batch_size = 4
gradient_accumulation_steps = 128   # effective batch still 512
# or even batch_size=2 + 256 if you're on a very strict 12 GB card
```

### Other tiny tweaks that help a few hundred MB
```python
compile = False          # compile can use 1–2 GB extra cache on first run
torch.set_float32_matmul_precision('medium')  # remove or set to 'high' if you have it
```

### TL;DR
Yes — change batch_size to 8 and gradient_accumulation_steps to 64.
You keep the same effective batch size (512), same model quality, same number of tokens seen, but VRAM drops enough to fit comfortably on 12 GB.

You'll be fine after that change. Happy training!
