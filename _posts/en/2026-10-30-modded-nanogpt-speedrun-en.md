---
audio: false
generated: true
image: false
lang: en
layout: post
title: Modded NanoGPT Speedrun
translated: false
type: note
---

This is **modded-nanogpt** — the NanoGPT speedrun. Here's the project status and what to do:

## What the project is
Compete to train a GPT-2-small to **≤3.28 FineWeb val loss on 8×H100 in the least wall-clock time**. Current record: **0.665 min (39.9s)** — ANVIL2 (`records/track_1_short/2026-08-30_ANVIL2`).

- `train_gpt.py` + `track_1_short/` — track 1 trainer (model, optimizer, schedules, kernels)
- `train_gpt_medium.py` — track 2 (GPT-2 Medium, target 2.92)
- `records/track_3_optimization/` — track 3 (minimize steps, unlimited time)
- `run.sh` — launches `torchrun --standalone --nproc_per_node=8 train_gpt.py`

Git is clean and up to date with `origin/master`.

## Your environment
- ✅ torch 2.10.0+cu128 installed, CUDA available, `torchrun` on PATH
- ⚠️ Only **1× RTX 4070 (12GB)** — not 8×H100, so official record timing isn't possible here
- ❌ Training data not downloaded yet (`fineweb10B/` missing)
- ❓ FlashAttention-3 kernel cache (`devenpzak/flash-attn3-12864`) not verified

## What to do, by goal

**A. Run the current record locally (smoke test):**
```bash
pip3 install -r requirements.txt
python3 data/cached_fineweb10B.py 9        # ~900M tokens
sed -i 's/nproc_per_node=8/nproc_per_node=1/' run.sh
./run.sh
```
Note: on 12GB you may need to shrink the attention sequence length (README: PR #38 guide) — that changes training behavior, so results won't be comparable to the record. First run also pays ~7 min of `torch.compile` time.

**B. Compete for a new record** (the actual "project task"):
1. Read the **Rules** section of `README.md` (fixed data pipeline, ≤3.28 val loss at p<0.01, no extra inductor flags, must beat prior record on same hardware)
2. Find an improvement — algorithmic (architecture/optimizer/schedule) or systems (kernels, CUDA graphs, comms)
3. Validate on 8×H100 (e.g., PrimeIntellect, used for official runs), provide run logs, open a PR

**C. Contribute without a record:** pick up open PRs, improve docs/readability, or work track 2/3.

Which goal do you want to pursue? If it's A, I can start the data download and prep the run now.
