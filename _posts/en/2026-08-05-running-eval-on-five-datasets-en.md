---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running Eval on Five Datasets
translated: false
type: note
---

Your eval is still running in the background — 3 of 5 datasets done (gsm8k, math500, humaneval), currently on mbpp → alpaca next. 

Here's the command to run it yourself:

```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py \
  --dataset gsm8k,math500,humaneval,mbpp,alpaca \
  --num-samples 100 \
  --max-new-tokens 128
```

**Flags you can tweak:**
- `--dataset` — comma-separated, any of: `gsm8k, math500, aime25, aime24, humaneval, mbpp, lbpp, livecodebench, mt-bench, alpaca, arena-hard-v2, swe-bench`
- `--num-samples` — samples per dataset (default 3; ~3.5s/sample on this GPU)
- `--max-new-tokens` — output length; keep ≤128 to stay within 12GB VRAM
- `--target_name_or_path` / `--draft_name_or_path` — defaults to the toy FP8 setup

**To run it in the background with logging:**
```bash
cd /mnt/data/DeepSpec
nohup bash -c 'CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py --dataset gsm8k,math500,humaneval,mbpp,alpaca --num-samples 100 --max-new-tokens 128' > /tmp/eval_big.log 2>&1 &
tail -f /tmp/eval_big.log   # watch progress
```

Run it from a fresh terminal (GPU is busy until the background one finishes). Want me to also add a README note in `toy_run/` documenting this command?