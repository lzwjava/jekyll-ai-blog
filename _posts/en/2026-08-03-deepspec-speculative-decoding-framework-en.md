---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DeepSpec: Speculative Decoding Framework"
translated: false
type: note
---

This is **DeepSpec** — an open-source research codebase from **DeepSeek AI** (<https://github.com/deepseek-ai/DeepSpec>) for training and evaluating **draft models for speculative decoding**. It's the official implementation accompanying the **DSpark paper** ("DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation", arXiv:2607.05147).

## What it does

Speculative decoding speeds up LLM inference by having a small "draft" model propose tokens that a large "target" model verifies in parallel. DeepSpec provides the full pipeline to train those draft models against a target model (Qwen3 or Gemma 4 family) and evaluate the resulting speedup/acceptance on benchmarks.

## Structure

**Entry points**

- `train.py` — spawns one training worker per visible GPU (not torchrun; uses `torch.multiprocessing.spawn`)
- `eval.py` — evaluates a trained draft checkpoint against the target model on 9 benchmarks (gsm8k, math500, aime25, humaneval, mbpp, livecodebench, mt-bench, alpaca, arena-hard-v2)
- `config/` — 12 per-algorithm/per-model configs (dspark, dflash, eagle3 × Qwen3 4B/8B/14B, Gemma 12B)

**`deepspec/` package (~10.8k lines, 65 Python files)**

- `modeling/` — the three draft model architectures:
  - **DSpark** (the new algorithm): block-wise semi-autoregressive draft model with multi-layer "anchored" attention over target hidden states, a **Markov head** for token-level bias, and a **confidence head** for early stopping
  - **DFlash** — DSpark minus the Markov/confidence heads (CE-only)
  - **Eagle3** — adapted from SpecForge
- `trainer/` — distributed trainers (`base_trainer`, `dspark_trainer`, `eagle3_trainer`), checkpoint manager with atomic `step_latest` symlinks
- `eval/` — speculative-decoding evaluators with draft proposal / verification loop, confidence-head calibration recorder
- `data/` — target-cache dataset loader, CUDA prefetcher, JSONL dataset, parser
- `utils/` — sampling, fused optimizer, distributed init, config parsing, metrics, HFAI suspend support

**`scripts/`** — the 3-stage workflow:

1. `data/` — download/split `open-perfectblend`, regenerate answers with the target model via SGLang servers, and precompute a per-token hidden-state **target cache** (⚠️ ~38 TB for the default Qwen3-4B setting — a real constraint)
2. `train/` — `train.sh` launches training against the cache; checkpoints land in `~/checkpoints/<project>/<exp>/step_*`
3. `eval/` — `eval.sh` runs acceptance-rate evaluation

## Notable details

- **Training data**: draft models are trained to predict the *target model's* outputs from cached target hidden states, with a hybrid loss (CE + L1 on hidden states + confidence-head loss, with token-distance decay)
- **Attribution**: Eagle3 code is adapted from SpecForge (Apache-2.0); DFlash design from z-lab/dflash (MIT) — see `NOTICE`
- **Released checkpoints**: `deepseek-ai/dspark_qwen3_4b_block7`, `deepseek-ai/eagle3_*`, etc. on HuggingFace
- **Hardware assumption**: single node, 8 GPUs; per-GPU batch size 1, global batch 512

In short: a research-grade implementation of a speculative-decoding draft-model training + evaluation framework, with DSpark as the headline contribution.
