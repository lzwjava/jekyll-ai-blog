---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoGPT Wikipedia training run
translated: false
type: note
---

Running smoothly. Here's the summary.

## Data copied
`nanoGPT/data/wikipedia_local/` → **`/mnt/data/igpt/data/wikipedia/`**

| file | size | contents |
|---|---|---|
| `train.bin` | 172 MB | **85,970,233** GPT-2 BPE tokens |
| `val.bin` | 118 KB | 59,058 tokens |
| `meta.pkl` | 73 B | created by me (was missing) — `{tokenizer: bpe, encoding_name: gpt2}` |

Kept separate from the existing char-level `data/` so `--data_dir data` still works.

## Two fixes to `train.py` (both needed for a long run)
1. **`estimate_loss()` had no `torch.no_grad()`** — eval built a backward graph and OOM'd. Added the decorator (matching `generate()`/`sample_and_print()`).
2. **Final save overwrote `ckpt.pt` with the last state**, destroying the best-val checkpoint the README advertises. Now the final state goes to `ckpt_last.pt` and `ckpt.pt` stays best-val.

## Training launched (system `python3.12`, torch 2.11+cu130)
```
PID 670206   log: /mnt/data/igpt/out-wikipedia/train.log
data_dir=data/wikipedia  tokenizer=bpe  out_dir=out-wikipedia
n_layer=6 n_head=6 n_embd=384 (29.95M params) block_size=256 dropout=0.1
batch_size=8 × grad_accum=16  → 32,768 tok/iter
max_iters=30000 (~983M tokens ≈ 11 epochs)  lr=6e-4 cosine→6e-5  warmup=1000
```
Progress so far: **val loss 6.26 @ iter 500**, ~325 ms/iter → **ETA ≈ 2.7 h** (done ~06:03). Best checkpoint is saving every 500 iters.

Monitor / stop / sample:
```bash
tail -f /mnt/data/igpt/out-wikipedia/train.log
kill $(cat /mnt/data/igpt/out-wikipedia/train.pid)
/usr/bin/python3.12 train.py --data_dir data/wikipedia --tokenizer bpe \
  --out_dir out-wikipedia --sample --prompt "The history of" --max_new_tokens 200
```

## One caveat worth your attention
Your `llama-server` (Qwen3-8B) is holding **5.9 GB** of the 12 GB card, and the desktop ~3.5 GB, so only ~2.4 GB was usable — I had to shrink to a 30 M-param model with micro-batch 8, and free VRAM is just **~330 MiB**. If you stop `llama-server`, I can rerun with a meaningfully bigger model (e.g. `n_embd=768, n_layer=12`) and bigger batch, which would use the card properly. There's also a 3.7 B-token `fineweb/train.bin` in nanoGPT if you'd rather train on that.