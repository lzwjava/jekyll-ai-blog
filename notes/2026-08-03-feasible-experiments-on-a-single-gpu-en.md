---
audio: false
generated: true
image: false
lang: en
layout: post
title: Feasible Experiments on a Single GPU
translated: false
type: note
---

Here's the deal: **DeepSpec is a speculative-decoding draft-model training/eval repo**, and its default pipeline is built for a datacenter node — 8 GPUs, ~38 TB of disk for the target cache. This machine has **1 × RTX 4070 (12 GB, ~2 GB free) and 703 GB free disk**, so let me be upfront about what's runnable here vs. not.

## The intended workflow (per the README)

```bash
# 1. Install deps (torch 2.9.1, transformers 5.10.2, ...)
python -m pip install -r requirements.txt

# 2. Data prep (3 stages): download prompts → regenerate answers with target
#    model via SGLang → precompute target cache (~38 TB for Qwen3-4B!)
bash scripts/data/prepare_data.sh

# 3. Train a draft model against the cached target outputs
bash scripts/train/train.sh          # spawns 1 worker per visible GPU (expects 8)

# 4. Evaluate speculative-decoding acceptance on benchmarks
bash scripts/eval/eval.sh
```

## What's feasible on *this* machine

**✅ Doable: evaluation using the released checkpoints** (HF is reachable, torch 2.10 + CUDA already installed):

```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 python eval.py \
    --target_name_or_path Qwen/Qwen3-4B \
    --draft_name_or_path deepseek-ai/dspark_qwen3_4b_block7 \
    --max-new-tokens 512
```

This downloads the target + draft models and runs the 9 benchmarks (gsm8k, math500, humaneval, …). Caveats: it spawns one worker per visible GPU (fine — 1 GPU), it needs ~8 GB VRAM for Qwen3-4B in bf16 plus the draft model, so **close the desktop/GNOME apps to free VRAM first**, and expect it to be slow on a single 4070. You can trim work with `--tasks` if you want, but note the flag isn't wired up in `eval.py` — it hardcodes `TASKS`.

**❌ Not feasible here: training.** Two blockers:
- The default target cache needs **~38 TB of disk** (you have 703 GB). You'd have to shrink the dataset to a tiny fraction and reduce `model.target_layer_ids` in `config/dspark/dspark_qwen3_4b.py`, which changes results meaningfully.
- Training assumes 8 GPUs (`train.sh` uses `CUDA_VISIBLE_DEVICES=0..7`); a single 12 GB card can't practically train a Qwen3-4B draft even with `local_batch_size=1`.

**❌ Not feasible: data prep.** Requires serving Qwen3-4B with SGLang on 8 GPUs (`scripts/data/launch_sglang_server.sh` starts 8 workers).

## If you want to run *something* real on this box

**Option 1 — eval on released checkpoints (recommended, above).** Use any row from the [Released Checkpoints table in the README](README.md); just match `--target_name_or_path` to the column.

**Option 2 — toy training run.** Cut the data pipeline to a few hundred samples (e.g. `--test-size` larger / filter the regen JSONL), reduce `max_length` and `target_layer_ids`, point `data.target_cache_path` at a small cache dir, set `CUDA_VISIBLE_DEVICES=0`, and lower `train.local_batch_size=1`. You'll still likely OOM or run for days on one 4070 — treat it as a smoke test, not real training.

**Option 3 — clone to a bigger box.** This repo is really meant for an 8×80 GB node. If you have access to one (or a cloud A100/H100 node), the three commands at the top are all you need.

Want me to run the eval option now (freeing VRAM first), or set up a minimal smoke-test training run with a tiny dataset?