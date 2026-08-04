---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSpec Runs on One GPU
translated: false
type: note
---

Done — I got DeepSpec running end-to-end on your machine. Here's the full picture:

## What DeepSpec is

A framework for **speculative decoding**: training a small *draft* model that proposes tokens, which a large *target* model (e.g. Qwen3-4B) verifies in parallel — giving big speedups. Three pipelines: data prep → training → evaluation.

## Reality check on your hardware

| Requirement | This machine |
|---|---|
| Default configs assume **8 GPUs** | 1× RTX 4070 (12GB) |
| Target cache for real configs | ~38 TB (!) |
| Your box | 1 GPU, 12GB, ~3GB used by desktop apps |

So the paper's full configs aren't feasible here. But there's a **toy setup** (already present from an earlier session) that exercises the same code path: tiny 114-sample dataset, Qwen3-4B-FP8 target cache (477MB), 2 draft layers, 7-token blocks. I ran it all the way through:

## What I ran (all worked ✅)

**1. Training** (~20s):
```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 /usr/bin/python3.12 train.py \
  --config config/dspark/dspark_qwen3_4b_fp8_toy.py \
  --opts "data.target_cache_path=${HOME}/.cache/deepspec/qwen3_4b_fp8_toy_cache"
```
Loss dropped 3.34 → 2.66, checkpoints saved to `~/checkpoints/deepspec/dspark_block7_qwen3_4b_fp8_toy/`.

**2. Evaluation** (speculative decoding demo, `toy_run/eval_smoke.py` — 3 gsm8k samples, 128 tokens):
```
|  gsm8k  | Qwen3-4B-FP8 | step_latest | 7.00+1 | accept_len 1.00 | verify_rate 0.1253 | accept_rate@0 0.0026 |
```
The draft proposes 7-token blocks, the target verifies them, and acceptance rates are measured. Numbers are low because it's a 100-sample/2-epoch smoke model — a real checkpoint accepts 2–4 tokens per block. The mechanism works: propose → verify → reject-sample → commit.

## Two bugs I found & fixed

1. **NaN bug** (real code bug): `build_draft_config` deep-copies the target config *including* Qwen3-4B-FP8's `quantization_config`, so transformers built FP8 linears at eval time expecting `weight_scale_inv` weights that the bf16 checkpoint doesn't have → NaN logits → crash. Fixed by stripping `quantization_config` in `deepspec/modeling/dspark/{qwen3,eagle3/qwen3}/config.py`.
2. **Missing dep**: `prettytable` wasn't installed → `pip install --break-system-packages prettytable`.

## Notes for the real thing

- For actual results, run `bash scripts/train/train.sh` and `bash scripts/eval/eval.sh` on an 8-GPU node with the `config/*.py` configs (real configs point at `Qwen/Qwen3-4B`, 38TB cache).
- Released checkpoints (e.g. `deepseek-ai/dspark_qwen3_4b_block7`) are listed in the README — those load directly via `--draft_name_or_path`.
- Old broken checkpoints are preserved at `~/checkpoints/deepspec/dspark_block7_qwen3_4b_fp8_toy.bak` if you want them; `toy_run/eval_smoke.py` is reusable (try `--dataset math500 --num-samples 5`).

Want me to try anything else — e.g. run a bigger eval set, or wire the real released DSpark checkpoint once you have more VRAM?