---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Optimized nanoGPT Config for RTX 4070
translated: false
type: note
---

Here's an adjusted nanoGPT config optimized for your RTX 4070 (12 GB VRAM) when using **just this single Parquet file** (~3.1 GB, from CC-MAIN-2013-20/000_00000.parquet).

### Key Adjustments and Why

- **Dataset size estimate**: This one Parquet contains roughly 1–2 billion tokens (based on FineWeb's structure, where the full CC-MAIN-2013-20 crawl has ~144.5B tokens across ~100–150 files, and each file averages 2–4 GB with good compression). It's much smaller than the full FineWeb, so I've reduced `max_iters` and `lr_decay_iters` to target ~2–3B total tokens seen (about 1–2 epochs for good convergence without overfitting on a 125M param model).
- **Memory fit**: Sticking with the ~125M param model (12L/12H/512embd) – it uses ~9–10 GB VRAM during training on your 4070. If you hit OOM, drop `batch_size` to 12 or `gradient_accumulation_steps` to 24.
- **Training duration**: With 5000–10000 iters, this should take ~5–10 hours on a 4070 (assuming ~1–2 iters/sec). Monitor loss; stop early if it plateaus.
- **Other tweaks**: Slightly lower LR since data is smaller (less diversity). Use `block_size=1024` for best quality, as FineWeb docs emphasize longer contexts.
- **Setup note**: Your wget downloads one file to `wikipedia_test_dump`. To use it in nanoGPT:
  - Move/rename it to `data/fineweb/train/000_00000.parquet` (or modify `data/fineweb/prepare.py` to point to your dir and process only this file).
  - Run `prepare.py` to tokenize into `train.bin`/`val.bin`.
  - If prepare.py expects multiple files, hack it to loop over just this one.

### Recommended Config for Single Parquet (~1–2B Tokens)

```python
out_dir = 'out-fineweb-single-parquet'
eval_interval = 500       # Evaluate more often on small data
eval_iters = 200
log_interval = 50         # Log more frequently
always_save_checkpoint = True

wandb_log = True          # Optional
wandb_project = 'fineweb'
wandb_run_name = '125M-single-parquet-4070'

dataset = 'fineweb'       # Assumes you adapted prepare.py for your single file
gradient_accumulation_steps = 32     # Effective batch size: 16 * 32 = 512 sequences
batch_size = 16
block_size = 1024                    # Matches FineWeb's processing

# Model (~125M parameters) – perfect for 12 GB VRAM
n_layer = 12
n_head = 12
n_embd = 512
dropout = 0.0                        # Add 0.1 if overfitting
learning_rate = 5e-4                 # Slightly lower for smaller data
max_iters = 6000                     # ~3B tokens seen (adjust up to 10000 if loss keeps dropping)
warmup_iters = 500                   # Shorter warmup
lr_decay_iters = 6000
min_lr = 5e-5
beta2 = 0.99

# Extras for speed/stability
compile = True            # PyTorch compile for 20–30% faster training
bias = False              # Like LLaMA/Mistral
weight_decay = 0.1
```

### Smaller Model Option (If You Want Faster Training or Less Memory)

If the above hits ~11 GB VRAM peak, try this ~84M param config (uses ~7–8 GB):

```python
n_layer = 6
n_head = 6
n_embd = 384
learning_rate = 6e-4      # Higher for smaller model
max_iters = 8000          # Compensate with more iters (~3–4B tokens)
```

Still solid quality, but weaker than 125M.

### Training Tips

- **Total tokens per iter**: ~512 sequences * 1024 tokens = ~0.5M tokens.
- **Epochs**: With ~1.5B tokens in the file, 6000 iters ≈ 2 epochs. FineWeb is high-quality, so 1–3 epochs is ideal – watch val loss.
- **If data is too small**: Loop multiple epochs by increasing `max_iters`. Or download a few more Parquets (e.g., 000_00001.parquet) for better diversity.
- **Monitor**: Use wandb to track. If loss doesn't drop below ~3.5–4.0 perplexity, add dropout=0.1.
- **Hardware**: On 4070, enable `--compile` and run with `torch.backends.cuda.matmul.allow_tf32=True` for speed.

This should give you a decent small GPT on this subset. If you share loss curves or exact token count from prepare.py, I can refine further! 🚀
