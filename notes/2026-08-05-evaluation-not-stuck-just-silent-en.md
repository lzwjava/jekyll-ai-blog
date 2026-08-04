---
audio: false
generated: true
image: false
lang: en
layout: post
title: Evaluation not stuck, just silent
translated: false
type: note
---

It's **not stuck** — the eval is running fine. Here's the evidence:

**GPU + worker actively computing:**
```
GPU util: 73% → 64% → 75% (polled over 9s), mem steady at 9887 MiB
Worker child 44161: 101% CPU, 1.95 GB RSS, actively crunching
```

**Why it looks stuck — the script has no per-sample progress output.** Looking at the code flow in `base_evaluator.py`:

1. `Loading weights: 100%` — both models loaded ✅
2. `Download complete: 0.00B` — that was the `kernels-community/finegrained-fp8` Triton kernel package being fetched from HF hub (first-run only; the 0.00B is just a garbled progress bar)
3. Now it's inside `run_dataset()` → `generate_one_sample()` for gsm8k. The loop has **no tqdm/no print per sample** — results only appear as a table row at the **end of each dataset** via `print_dataset_result()`.

So you'll see nothing on screen for ~6 minutes per dataset (100 samples × ~3.5s/sample), then a row like:

```
+-------+--------------+-------------+--------+------+...+
| gsm8k | Qwen3-4B-FP8 | step_latest | ...    |      |
+-------+--------------+-------------+--------+------+...+
```

**Timeline estimate:**
- gsm8k row → ~6 min in (you're at ~3 min now)
- math500 → ~12 min
- humaneval → ~18 min
- mbpp → ~24 min
- alpaca → ~30 min

Ways to watch progress in another terminal:
```bash
nvidia-smi -l 10                       # GPU activity
ps -o pid,etime,time,%cpu -p $(pgrep -f spawn_main)   # worker CPU time growing
```

If it were truly hung, GPU util would be ~0% and worker CPU would be flat. Neither is true. Just let it cook — first gsm8k row should appear around the 6-minute mark. If you want per-sample progress next time, I can add a `tqdm` to the loop in `run_dataset()`.