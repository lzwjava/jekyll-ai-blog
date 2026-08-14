---
audio: false
generated: true
image: false
lang: en
layout: post
title: Data Prep Steps
translated: false
type: note
---

Here's the situation and what to do next.

## Where you are

- ✅ `tok_mixed/` has a fresh joint BPE (vocab=65536, 8 control tokens).
- ⚠️ The existing `data/train.bin` (90 KB) + `data/val.bin` (10 KB) are **stale smoke-test artifacts** — they were NOT made with this tokenizer and from this data. You must re-run `prepare.py`.
- ❌ You **cannot `generate.py` yet** — it requires `--model out/ckpt.pt`, i.e. a trained GPT checkpoint. This repo is only data-prep + generation; actual training is done with [nanoGPT](https://github.com/karpathy/nanoGPT) or [nanochat](https://github.com/duyn/nanochat) pointing at the `data/` dir you produce.

So the order is: **prepare → train (nanoGPT/nanochat) → generate**.

## Step 1 — (optional but recommended) check the real token ratio

`ratios.json` is stale (only ~7.6k tokens). Re-measure on the sample to confirm your `zh_token_frac` is where you want it before you spend compute training:

```bash
python3.12 -m scripts.measure_token_ratio \
    --input mixed_sample_2gb.txt --out ratios.json --tok-prefix tok_mixed
```

If `zh_token_frac` is too low, bump `--zh-frac` in `mix_bilingual.py` and re-mix. (Note: the 2 GB sample is a slice of `mixed.txt`; measuring it is a proxy, not exact.)

## Step 2 — tokenize into `.bin` (this is the "next" step)

```bash
python3.12 -m scripts.prepare \
    --input mixed_sample_2gb.txt \
    --tok-prefix tok_mixed \
    --out-dir data \
    --val-frac 0.05
```

Notes:

- `prepare.py` loads the **whole file + token ids into RAM**. With 62 GB RAM the 2 GB sample (and even the 11 GB `mixed.txt`) is fine; just don't point it at something larger than memory.
- vocab is exactly 65536 → `prepare.py` uses **uint16** (its check is `vocab_size <= 65536`). So `.bin` ≈ 2 bytes/token. Ignore the trainer's slightly conservative warning.
- I used `--val-frac 0.05` so you don't waste 10% of a modest corpus on validation. Tune to taste.
- This overwrites the old `data/train.bin`/`val.bin` (good — you want that).

If you instead want to train on the **full** corpus eventually, run it against `mixed.txt` (≈11 GB). For a first run-on-the-4070, the 2 GB sample is a reasonable starting point.

## Step 3 — train a model (outside this repo)

This repo has no `train.py`. Clone nanoGPT (or nanochat), point its `data_dir` at `/mnt/data/bilingual-gpt/data`, set vocab_size=65536, and use the control tokens. Rough nanoGPT flow:

```bash
git clone https://github.com/karpathy/nanoGPT
cd nanoGPT
# edit train.py: vocab_size=65536, dataset path -> /mnt/data/bilingual-gpt/data
python train.py config/train_gpt2.py \
    --device cuda --dtype bfloat16 \
    --n_layer 12 --n_head 12 --n_embd 768 \
    --batch_size 12 --block_size 1024 --grad_clip 1.0 \
    --learning_rate 3e-4 --warmup_iters 100 --lr_decay_iters ... \
    --out_dir out
```

On a 12 GB 4070, keep `block_size`≤1024 and `batch_size` modest (or use grad-accum). A ~125M-param model is realistic here. For anything bigger, consider the nanochat path or a smaller corpus.

## Step 4 — generate (only now)

```bash
python3.12 -m scripts.generate \
    --model out/ckpt.pt --tok-prefix tok_mixed \
    --lang zh --prompt "机器学习是什么？" --max-new-tokens 200
```

So: run **Step 2 now**, then you'll be ready to train. Want me to run `measure_token_ratio` and `prepare` for you?
