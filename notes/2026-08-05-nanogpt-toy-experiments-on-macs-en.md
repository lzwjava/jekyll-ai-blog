---
audio: false
generated: true
image: false
lang: en
layout: post
title: nanoGPT Toy Experiments on Macs
translated: false
type: note
---

Question: Can I run nanoGPT-style small experiments (e.g. 1000 steps, tiny model) on an M2 Air or a 2017 Mac Pro (Intel)?

Answer: Yes, both work fine for toy-scale runs — you're not training GPT-2, you're training a few-hundred-K to few-M param char-level model. That's KB-to-MB of activations, trivial FLOPs.

**M2 Air**: use `--device=mps`. Real numbers from someone running this exact nanoGPT shakespeare_char config: with --device=cpu, each iteration takes ~410-550ms, and switching to --device=mps drops that to ~140-250ms per iteration, roughly a 2-3x speedup from using the on-chip GPU. At that rate 1000 steps is 2-5 minutes.

**Mac Pro 2017 (Intel, AMD GPU)**: no MPS, no CUDA on macOS. You're on `--device=cpu` only. Still fine at this scale — even on M2 the pure CPU path did ~410-550ms/iter for a 4-layer/64-embd model, so a 1000-step toy run is single-digit minutes on any modern-ish x86 CPU too. Don't expect torch.compile to help (Triton isn't meaningful here and often breaks on non-CUDA), so always pass `--compile=False`.

Setup + exact commands:

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
pip install torch numpy transformers datasets tiktoken wandb tqdm

# tiny char-level dataset, tokenizes in seconds
python data/shakespeare_char/prepare.py

# M2 Air (MPS)
python train.py config/train_shakespeare_char.py \
  --device=mps --compile=False \
  --n_layer=4 --n_head=4 --n_embd=128 --block_size=64 --batch_size=12 \
  --max_iters=1000 --lr_decay_iters=1000 --eval_iters=20 --log_interval=1 --dropout=0.0

# Mac Pro 2017 (CPU only)
python train.py config/train_shakespeare_char.py \
  --device=cpu --compile=False \
  --n_layer=4 --n_head=4 --n_embd=64 --block_size=64 --batch_size=8 \
  --max_iters=1000 --lr_decay_iters=1000 --eval_iters=1 --log_interval=1 --dropout=0.0
```

Notes:
- Set `PYTORCH_ENABLE_MPS_FALLBACK=1` before running on M2 — some ops still aren't implemented in MPS and will otherwise hard-error rather than silently falling back to CPU.
- If you want it more legit than "does loss go down," bump `max_iters` to ~3000-6000; one MPS run reached loss 3.25 after 6184 iterations in 3.5 minutes — that's when generated text starts looking like actual Shakespeare-ish structure instead of noise.
- If you want to skip Python entirely and go lower-level, Karpathy's `llm.c` compiles and runs pure C on CPU with no PyTorch dependency at all — worth trying on the Mac Pro since there's no GPU path there anyway.

References:
- [Running nanoGPT on a MacBook M2 — Simon Willison](https://til.simonwillison.net/llms/nanogpt-shakespeare-m2)
- [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- [PyTorch training on Apple Silicon — Hugging Face](https://huggingface.co/docs/transformers/v4.47.1/perf_train_special)