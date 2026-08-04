---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clean Slate Evaluation Retry
translated: false
type: note
---

My earlier launch attempt got killed with the tool call, so nothing is running now — the slate is clean. Here's the command, exactly as verified:

```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py \
  --dataset gsm8k,math500,humaneval,mbpp,alpaca \
  --num-samples 100 \
  --max-new-tokens 128
```

Or as a background job with logging:

```bash
cd /mnt/data/DeepSpec
nohup bash -c 'CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py --dataset gsm8k,math500,humaneval,mbpp,alpaca --num-samples 100 --max-new-tokens 128' > /tmp/eval_big.log 2>&1 &
tail -f /tmp/eval_big.log   # to watch progress
```

Verified pieces:
- `/usr/bin/python3.12` ✅ exists, torch 2.11.0 + CUDA working, 1 GPU
- Draft checkpoint ✅ `/home/lzw/checkpoints/deepspec/dspark_block7_qwen3_4b_fp8_toy/step_latest/`
- GPU free (2592 MiB used), no stale process
- All flags match `toy_run/eval_smoke.py`

Reminders: expect ~30 min for 500 samples, and the ~7% numbers from the earlier run are likely truncation artifacts of `--max-new-tokens 128` — don't treat them as real quality metrics.