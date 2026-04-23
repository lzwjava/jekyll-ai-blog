---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sample Python Code for Model Checkpoints
translated: false
type: note
---

You have two checkpoints available. Here are sample commands:

**From your FineWeb checkpoint (GPT-2 style, BPE tokenizer):**
```bash
python sample.py \
    --out_dir=out-fineweb \
    --start="The future of artificial intelligence is" \
    --num_samples=3 \
    --max_new_tokens=200
```

**From your Shakespeare char-level checkpoint:**
```bash
python sample.py \
    --out_dir=out-shakespeare-char \
    --start="To be or not to be" \
    --num_samples=3 \
    --max_new_tokens=200
```

**From a pretrained GPT-2 (no local checkpoint needed):**
```bash
python sample.py \
    --init_from=gpt2 \
    --start="Once upon a time" \
    --num_samples=2 \
    --max_new_tokens=100
```

**Key flags for `sample.py`:**

| Flag               | Default | Description                          |
| ------------------ | ------- | ------------------------------------ |
| `--num_samples`    | 10      | Number of samples to generate        |
| `--max_new_tokens` | 500     | Tokens per sample                    |
| `--temperature`    | 0.8     | Higher = more random                 |
| `--top_k`          | 200     | Top-k sampling cutoff                |
| `--start`          | `"\n"`  | Prompt string (or `FILE:prompt.txt`) |
| `--device`         | `cuda`  | Use `cpu` if no GPU                  |