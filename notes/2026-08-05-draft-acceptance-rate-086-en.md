---
audio: false
generated: true
image: false
lang: en
layout: post
title: Draft acceptance rate 0.86%
translated: false
type: note
---

I dug through the eval code and the draft checkpoint. Here's the full picture.

## How to read the table

```
dataset | target_model | draft_model | #propose | accept_len | verify_rate | accept_rate@0 ... @6
gsm8k   | Qwen3-4B-FP8 | step_latest | 7.00+1   | 1.01       | 0.1261      | 0.0086 0.0000 ... 0.0000
```

Columns (from `build_results_table` + `build_metrics_row` in `deepspec/eval/base_evaluator.py`):

| column | value | meaning |
|---|---|---|
| `#propose` | `7.00+1` | each speculative round proposes **7 draft tokens** (always the full block — see below) + the 1 anchor token (`+1` is hardcoded in the format string) |
| `accept_len` | `1.01` | average tokens committed per round = `avg(accepted_draft_tokens + 1)`. **Only 0.01 draft tokens are accepted on average** — you always commit the 1 guaranteed target token, never the draft's |
| `verify_rate` | `0.1261` | `accept_len / (propose + 1)` = `1.01/8 ≈ 0.126` — only **12.6% of the token positions you compute actually end up in the output** |
| `accept_rate@k` | `0.0086, 0, 0, …` | probability the k-th draft token is accepted. The **first draft token is accepted 0.86% of the time, positions 1–6 never**. This is the smoking gun |

So the table is telling you: **the draft proposes 7 tokens and gets rejected ~99% of the time.**

## Why it's so slow

1. **~0% draft acceptance = pure overhead, no speedup.** Every round still runs:
   - draft forward (7 tokens through the 2-layer DSpark block), then
   - target **verification forward of 8 positions** through the full Qwen3-4B target.
   
   Since you only commit 1.01 tokens per round, you're doing **~8× the target FLOPs per output token** compared to plain autoregressive decoding. Roughly 8× slower than baseline, before any overhead.

2. **The draft is a toy.** `dspark_block7_qwen3_4b_fp8_toy/step_latest` is a 2-layer model (`num_hidden_layers=2`, ~2 GB) trained on a 114-sample toy set (`perfectblend_train.jsonl`) per the checkpoint's `train_config.py`. Its distribution has nothing to do with gsm8k/math500/humaneval/mbpp/alpaca, so it proposes tokens the target almost never agrees with.

3. **The confidence threshold is a no-op here.** `enable_confidence_head = False` and `confidence_head_alpha = 0.0` in the toy config → `model.confidence_head is None` → `_confident_prefix_length` always returns the full block. So `--confidence-threshold 0.0` means "always propose all 7", guaranteeing wasted verification work on a bad draft.

4. **The workload is 5 datasets × 100 samples × up to 128 tokens = 500 samples**, batch-size-1, sequential, on one RTX 4070 (12 GB), with per-round Python/torch overhead: markov-head sampling (7 sequential steps over a 151,936 vocab), softmax over the full vocab at every verify, gather/cumprod/residual-sampling, KV-cache crops. FP8 targets also carry some CPU-side dequant/kernel overhead (`kernels-community/finegrained-fp8` v2 vs v4 also printed a notice).

Your run is still going right now (PID 49938, ~19 min in, 2/5 datasets done — matches ~9–10 min/dataset, so ~30 more minutes for humaneval+mbpp+alpaca).

## What to do

- For a genuine smoke test, use the sizes the script's docstring intends — kill the current run and do:
  ```bash
  CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py --dataset gsm8k --num-samples 3 --max-new-tokens 128
  ```
- To actually observe speedup you need a draft trained on the eval distribution (the real DSpark checkpoint, not the toy), and ideally a **baseline comparison**: time plain autoregressive sampling on the same target for the same samples and compare tokens/sec — with a 0.86% first-token acceptance rate the gap will be huge (spec ≈ 8× slower).
- If you must keep this toy draft for machinery testing, shrink the proposal length (smaller `block_size`, e.g. 2) so each rejected round wastes less verification work, or temporarily patch `_confident_prefix_length`/proposal to early-stop.
- Minor: the metrics row naming (`7.00+1`, `verify_rate`) is confusing — `verify_rate` is really "kept/computed ratio", not a rate.

Want me to kill the running job and rerun the small smoke test, or add a baseline (plain decoding) comparison to `eval_smoke.py` so you can see the slowdown factor quantitatively?