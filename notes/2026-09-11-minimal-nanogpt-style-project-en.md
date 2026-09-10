---
audio: false
generated: true
image: false
lang: en
layout: post
title: Minimal nanoGPT-Style Project
translated: false
type: note
---

Done. Created a nanoGPT-style project in `/mnt/data/igpt`:

| File | Purpose |
|------|---------|
| `train.py` | The entire project in one file (750 lines) |
| `README.md` | Install, quick start, how it works, flags, scaling recipe |
| `.gitignore` | Python + `data/`, `out/`, checkpoints, editor/OS files |

### What's inside `train.py`

- **Data prep** — auto-downloads tiny shakespeare (or `--dataset path/to.txt`), tokenizes once into cached `train.bin`/`val.bin` (uint16) + `meta.pkl`
- **Tokenizers** — `CharTokenizer` (self-contained, ~65 vocab) and `BPETokenizer` (GPT-2 BPE via `tiktoken`), same `encode`/`decode` interface
- **Model** — decoder-only GPT: pre-LN blocks, causal attention via `F.scaled_dot_product_attention(is_causal=True)`, GELU MLP, weight tying, GPT-2 init with residual scaling (default ≈10.7M params)
- **Training** — AdamW (decay on matrices only), warmup + cosine LR, grad accumulation, bf16/fp16 AMP with `GradScaler`, grad clipping, best-val checkpointing, resume, `torch.compile`, DDP via `torchrun`
- **Sampling** — `--sample` loads `out/ckpt.pt` without touching the dataset; temperature + top-k

### Verified end-to-end

- char + BPE tokenizers, CPU (fp32) and CUDA (bf16, fused AdamW)
- `--init_from resume`, `--sample`, `--eval_only`, `--help`, tokenizer round-trip assert
- Real convergence run (CUDA, default config, 300 iters): **val loss 4.30 → 1.92**, sample:

```
ROMEO:
You before will and is and the a see bood to take
Or them all and bart that us hall but comel.
```

Quick start:
```bash
python train.py
python train.py --sample --prompt "ROMEO:" --num_samples 3
```

The three files are untracked on `main` (repo has no commits yet) — tell me if you'd like me to make the initial commit.