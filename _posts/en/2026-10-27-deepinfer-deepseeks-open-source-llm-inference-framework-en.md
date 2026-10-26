---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DeepInfer: DeepSeek's Open-Source LLM Inference Framework"
translated: false
type: note
---

**DeepInfer is DeepSeek's open-source, high-performance LLM inference framework** — the engine behind the DeepSeek-V4.1-Flash production service, released as a cut-down but real system for offline inference. It is a Python + C++ (pybind11) stack: Python for model/engine orchestration, C++ for the hot scheduling path, TileLang/CUDA/Ascend kernels for compute, and a set of vendored DeepSeek kernel libraries (FlashMLA, DeepGEMM, DeepEP, DeepSelect) as git submodules.

This working copy is the public release (commits dated 2026‑10‑20/21, ~8.5 MB, 342 files), corresponding to [README.md](README.md).

![DeepSeek V4.1 Flash inference system architecture](doc/images/architecture_overview.png)

## Where it sits in the production picture

The [deployment Q&A](doc/inference_deployment_qa.md) describes the full production system: a **disaggregated E/P/D architecture** (vision encoder / prefill / decode), Wide‑EP for decode (EP64–128), dedicated 3FS KV-cache storage, four load balancers (VE, prefill, decode, expert-parallel), DeepSeek Recipe for API encoding/decoding, and 72h+ KV retention.

This repository implements the **engine core** of that picture; the README explicitly says the following are *not* included:

- the KV cache storage system,
- full VE/Prefill/Decode disaggregation (most engine hooks are there),
- data-parallel replica load balancing.

Similarly, [llm_engine.py](deepinfer/engine/llm_engine.py#L140) notes there is **no online-serving wrapper** — the user-facing entry point here is the offline `LLM` class.

## How a request flows

```
LLM.generate()                    deepinfer/entrypoints/llm.py
  └─ add_request() → Sequence     deepinfer/engine/llm_engine.py
      └─ C++ Scheduler            csrc/engine/scheduler.hpp
while unfinished:
  engine.step()                   deepinfer/engine/llm_engine.py#L860
    ├─ scheduler.schedule()       C++: prefix cache, chunked prefill, preemption,
    │                             block alloc, batch-invariant DP coordination
    ├─ _run_workers("execute_model_step")
    │    Worker.execute_model_step   deepinfer/worker/worker.py#L89
    │      1. forward current step (model runner, CUDA graphs)
    │      2. post-process *previous* step   ← overlap trick
    │      3. sample current step
    │      4. post-process current step (deferred in ZOS decode)
    └─ RequestOutput (pooled, zero-copy) → LLM clones them
```

The scheduler is deliberately in C++ (`csrc/engine/scheduler.hpp`, block manager, FLOPs estimator, MTP bookkeeping) so per-step batch decisions are cheap; Python only drives the loop (see [_C/engine.pyi](deepinfer/_C/engine.pyi) for the binding surface).

## Main subsystems

| Area | Where | What it does |
| :--- | :--- | :--- |
| Engine / scheduler | [csrc/engine](csrc/engine), [deepinfer/engine](deepinfer/engine) | Iteration-level scheduling, chunked prefill, prefix caching, preemption, KV block pools, **zero-overhead async scheduling** |
| Workers | [deepinfer/worker](deepinfer/worker) | Process-per-rank execution, CUDA graph capture, cache engine, ZOS step state, profiling |
| Model executor | [deepinfer/model_executor](deepinfer/model_executor) | V4.1 modules — MLA/index attention, MoE, YoCo, Engram, HC heads; DFlash MTP draft; vision encoder (ViT + aligner) |
| Kernels | [layers/tilelang_ops](deepinfer/model_executor/layers/tilelang_ops), [csrc](csrc), `vendor/` | TileLang kernels with separate `cuda/` and `asc/` implementations, plus vendored FlashMLA/DeepGEMM/DeepEP |
| EPLB | [eplb](deepinfer/model_executor/eplb) | Redundant experts, load statistics, periodic rebalance, in-place weight shuffle over symmetric memory |
| Structured output | [structure_output](deepinfer/structure_output) | XGrammar compilation/matching, token masks, async compile thread pool |
| Multimodal | [ve](deepinfer/ve), [vision_encoder](deepinfer/model_executor/models/vision_encoder) | Image preprocessing off the critical path, shared-memory pools, VL metadata |
| Cluster/hardware | [deep_cluster](deep_cluster) | Hardware-neutral accelerator discovery (NVIDIA/Ascend/CPU), NUMA/CPU binding |
| Stable API types | [sampling_params.py](deepinfer/sampling_params.py), [sequence.py](deepinfer/sequence.py), [config.py](deepinfer/config.py) | `SamplingParams` (incl. `so_args`, `seq_seed`), sequences, engine config |
| Tests / examples / eval | [tests](tests), [examples](examples/README.md), [eval](eval) | PPL regression baselines, batch-invariance and sampler tests, offline + benchmark + Pareto sweep scripts |

## The features that define the project

- **Zero-overhead batch scheduling (ZOS)** — the headline optimization, on by default. `schedule(N+1)` and post-processing of `N-1` are overlapped with GPU `forward(N) → sample(N)`, removing the idle bubble. Implemented via the deferred `WorkerStepState` pipeline in [worker.py](deepinfer/worker/worker.py#L89).
- **DSpark / variable-length speculative decoding** — MTP draft tokens (default 5), confidence-scheduled verification where a TileLang kernel recomputes per-request lengths on-GPU. See [mtp/dflash.py](deepinfer/model_executor/models/mtp/dflash.py) and `DEEPINFER_ENABLE_MTP_VARLEN`.
- **SWA bounded replay / YoCo** — decoder prefill recomputes only a bounded 128-token suffix instead of thousands of tokens, using the YoCo truncation mode (`DEEPINFER_YOCO_PREFILL_TRUNCATION_MODE=compact`). See [yoco.py](deepinfer/model_executor/models/v4_modules/yoco.py).
- **Batch-invariant and deterministic inference** — `DEEPINFER_BATCH_INVARIANT=1` makes results independent of batch composition; deterministic sampling combines it with MTP disabled and a fixed `seq_seed` (NVIDIA only).
- **Expert-parallel load balancing** — hot experts replicated across GPUs, rebalanced periodically; settings differ for prefill (small EP, aggressive rebalance) and decode (Wide-EP, lazy rebalance).
- **Structured outputs** — regex / JSON schema / EBNF constraints via XGrammar, specified through `SamplingParams(so_args=...)`.
- **Dual hardware backends** — the same Python code targets **NVIDIA SM100** and **Huawei Ascend 950**, selected by `DEEPINFER_ACCELERATOR`; `setup.py` builds either a `CUDAExtension` or an `NpuExtension` named `deepinfer._C`.

## Building and running

Linux, Python 3.12, GCC ≥ 13, plus CUDA 13 or CANN 9.2 ([README.md](README.md#L46)):

```bash
export DEEPINFER_ACCELERATOR=nvidia    # or ascend
./build.sh                             # installs deps, builds vendor libs + extension
python examples/offline_inference.py --ep 8
python examples/benchmark.py           # throughput/latency, PROF=1 for traces
```

`examples/offline_inference.py` downloads `deepseek-ai/DeepSeek-V4.1-Flash-1017` by default (or uses `DEEPINFER_HF_MODEL_DIR`), runs a fixed prompt set, and prints decode PPL and speculative-decoding acceptance rates; [tests/models/offline_decode_ppl.json](tests/models/offline_decode_ppl.json) stores golden PPL baselines per platform/workload. Configuration is almost entirely environment-driven via [environ.py](deepinfer/environ.py), which is worth reading as the de-facto feature index.

## Practical caveats for this checkout

- It **cannot run as-is here**: the `deepinfer._C` binary extension is not built (only `.pyi` stubs exist), and the platform is macOS while the code targets Linux + CUDA/CANN.
- The `vendor/` submodules (DeepEP, DeepGEMM, FlashMLA, DeepSelect, and Ascend variants) are **uninitialized** — run `git submodule update --init --recursive` before building.
- The public code is the serving engine, not the full service: you would need to supply the KV-cache store, request routing/load balancing, and an HTTP/API layer yourself.

**In one sentence:** DeepInfer is a production-grade, dual-vendor inference engine for DeepSeek-V4.1-Flash whose interesting parts are a C++ iteration-level scheduler with zero-overhead async overlap, EP/MoE-aware execution with expert load balancing and speculative decoding, bounded SWA recomputation, and a heavily kernel-optimized model runtime — open-sourced minus the infrastructure glue that makes the full cloud service.
