---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual 232M Model Training Config
translated: false
type: note
---

Real training config written: **`/mnt/data/nanoGPT/config/train_bilingual.py`**

Key numbers:

- **Corpus**: 434M train tokens, 22.9M val tokens, vocab=65536
- **Model**: L18/H16/C896 → ~232M params (same body as your gpt2-200m run; the 65k embedding adds ~13M vs GPT-2's 50k)
- **Throughput**: 4 × 1024 × 128 = 524,288 tokens/step → ~828 steps/epoch
- **Budget**: `max_iters=5000` ≈ 2.62B tokens ≈ ~6 epochs over the 434M train split. Your corpus is small, so multi-epoch is unavoidable; watch val loss for overfitting.
- **VRAM**: bs=4/block=1024 peaked ~8 GB on the 4070 for the 219M run; the +13M embed keeps it under 12 GB. `compile=True`.
- LR 4e-4 → 4e-5 cosine, 500-step warmup.

Run from the nanoGPT dir:

```bash
cd /mnt/data/nanoGPT
python3.12 train.py config/train_bilingual.py
```

Resume (after a checkpoint exists):

```bash
python3.12 train.py config/train_bilingual.py --init_from=resume
```

Caveats:

- Only ~434M train tokens is data-limited for a 232M model (Chinchilla wants ~4.6B). Loss will plateau and val loss will likely start rising after a few epochs — `eval_interval=250` + `always_save_checkpoint=True` means the best-val checkpoint is kept (it only overwrites `ckpt.pt` when val loss improves), so you can stop early when val loss bottoms out.
- If you want more data, scale up by re-mixing from your full `fineweb_edu_shard.jsonl` (3.5 GB) + `fineweb2_cmn_shard.jsonl` (8 GB) sources instead of the 2 GB sample — the prep pipeline is streaming and handles it fine.
