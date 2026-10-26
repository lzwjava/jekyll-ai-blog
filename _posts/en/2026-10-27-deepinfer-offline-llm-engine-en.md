---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DeepInfer: Offline LLM Engine"
translated: false
type: note
---

Here's what **DeepInfer** is:

## Overview

**DeepInfer** is DeepSeek's **high-performance LLM inference engine** for serving DeepSeek models in production, open-sourced (Apache 2.0). This release is **offline inference only** — batch generation via Python API — with the core machinery needed for large-scale serving, but without online serving components (KV cache system, disaggregation infra, load balancing).

It's a fork/descendant of **vLLM** (explicitly acknowledged in code comments: "Derived from vLLM; modified by DeepSeek"), with inspiration from SGLang and TensorRT-LLM.

## Key facts

- **Target model:** DeepSeek-V4.1-Flash (default checkpoint `deepseek-ai/DeepSeek-V4.1-Flash-1017`)
- **Hardware:** NVIDIA SM100 (Blackwell) GPUs and Huawei Ascend 950 NPUs
- **Scale:** ~46K lines of Python + ~6K lines of C++ (plus vendored kernels)
- **Stack:** PyTorch 2.7+ / CUDA 13 / CANN 9.2, GCC ≥ 13, Python 3.12
- **State:** Beta, very fresh repo — only 4 commits (initial commit + doc/bump updates)

## Architecture

**Python core** (`deepinfer/`):
- `engine/llm_engine.py` (~1K lines) — the orchestrator: scheduler loop, request lifecycle, batch processing, async (zero-overhead) scheduling, stats, profiling
- `worker/` — `model_runner.py`, `worker.py`, `cache_engine.py`, plus **CUDA graph runners** for prefill/decode and a flash-decoding graph runner
- `model_executor/models/deepseek.py` — the model itself, built from V4 modules: MoE MLP, MTP (multi-token prediction), **DFlash** draft model, **Engram** (ngram matching), **HC** (hybrid-cross? attention/heads), YOCO cross-layers, and multimodal embedding support
- `model_executor/layers/` — sampler, attention backends, tilelang_ops (custom TileLang kernels)

**C++ engine** (`csrc/engine/`) — the hot path, exposed via pybind11:
- `scheduler.hpp` — zero-overhead batch scheduler, block manager, flops estimator
- `prepare_sample.cpp` / `mtp_varlen.hpp` — sampling prep and MTP variable-length verification
- `zos.cpp` (ZOS status), sequence/request-output handling

**Vendored kernels** (git submodules): FlashMLA, DeepGEMM, DeepEP, DeepSelect, TileKernels, plus Ascend variants — plus one custom Triton-like TileLang op set.

## Notable features

- **Parallelism:** attention DP / balanced CP, MoE **EP with EPLB** (expert-parallel load balancing)
- **DSpark / confidence-scheduled verification** — draft-token acceleration with confidence-gated verification (env `DEEPINFER_ENABLE_MTP_VARLEN=1`)
- **SWA bounded replay** — truncates decoder prefill to a bounded suffix (`DEEPINFER_YOCO_PREFILL_*` env vars)
- **Batch-invariant inference & deterministic sampling** — identical results regardless of batch composition
- **Structured outputs** — regex / JSON schema / EBNF grammar constrained generation
- **Async scheduling enabled by default**, overlapping CPU scheduling with GPU execution

## Supporting pieces

- `eval/` — offline benchmark harness for AIME 2026, HLE (incl. image tasks), GPQA Diamond; separate generate-then-score stages reporting Pass@1
- `examples/` — offline inference, benchmarks, sweeps, YOCO tests
- `build.sh` / `setup.py` — builds the CUDA/NPU extensions (`DEEPINFER_ACCELERATOR=nvidia|ascend`)
- Vendored `deep_cluster` package for hardware-aware tuning (bf16 TFLOPS limits)

**Bottom line:** this is DeepSeek's battle-tested production inference stack, stripped down to an offline, batch-oriented API and released as reference/serving infrastructure — heavy on custom kernels and C++ scheduling for throughput, and delivering DeepSeek-V4.1-Flash at scale (prefill on 4 SM100s, decode on 64).
