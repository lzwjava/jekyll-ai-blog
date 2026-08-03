---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Architecture Overview
translated: false
type: note
---

I now have a comprehensive picture. Here's the architectural overview of the SGLang codebase.

---

# SGLang — Architecture Overview

**SGLang** is a high-performance serving framework for LLMs/multimodal models, from single GPU to large clusters. It powers production deployments (DeepSeek V3/V4, Llama, Qwen, etc.). This repo is a **hybrid Python + Rust** system (~5,200 Python files, Rust serving cores).

## Top-level layout

| Directory | Role |
| --- | --- |
| `python/sglang/lang/` | **Frontend DSL** — `@function`-decorated Python programs compiled to an IR (`ir.py`, `tracer.py`) and executed by an interpreter (`interpreter.py`) against pluggable backends (`backend/`: OpenAI, runtime endpoint, etc.) |
| `python/sglang/srt/` | **SRT (SGLang Runtime)** — the core serving engine |
| `rust/sglang-server/` | **Rust serving core** — API server (axum), tokenizer/detokenizer, tokenizer-manager rings; embedded via pyo3 |
| `rust/sglang-grpc/` | Rust gRPC server + pyo3 bridge to the Python scheduler |
| `rust/sglang-mm/` | Multimodal (image/audio/video) processing server ("inkling") |
| `proto/sglang/runtime/v1/` | gRPC contract (`SglangService`: typed + OpenAI-compatible + admin RPCs) |
| `sgl-model-gateway/` | Model gateway (Rust), router/front-end |
| `benchmark/`, `examples/`, `test/`, `docs_new/` | Benchmarks, examples, tests, docs |

## The runtime core (`python/sglang/srt/`)

```
┌─────────────┐   ┌───────────────────────┐   ┌──────────────────────────────┐
│ entrypoints │──▶│ TokenizerManager      │──▶│ Scheduler ──▶ TpWorker/      │
│ (HTTP/gRPC/ │   │ (request intake,      │   │ (event loop, batch           │
│  engine)    │   │  detokenize, egress)  │   │  planning, cache mgmt)       │
└─────────────┘   └───────────────────────┘   └──────────────────────────────┘
                                                       │
                                     ┌─────────────────┼──────────────────┐
                                     ▼                 ▼                  ▼
                              model_runner/      mem_cache/          layers/
                              (CUDA graphs,      (radix tree KV       (attention
                               forward, sampler)  cache, memory       backends,
                                                   pools)              MoE, etc.)
```

**Request flow:** HTTP/gRPC entrypoints (`entrypoints/http_server.py`, `grpc_server.py`, `engine.py` for offline use) → `TokenizerManager` (owns per-request state, tokenization, detokenization, streaming) → `Scheduler` via the request receiver.

**`Scheduler`** (`managers/scheduler.py`, ~4,850 lines) is the heart:

- Single-threaded event loop (`event_loop_normal` / `event_loop_overlap`) that continuously: receives requests → plans the next batch → launches GPU forward → processes results.
- **CPU/GPU overlap**: the scheduler runs on a separate CUDA stream (`schedule_stream`) so next-batch planning overlaps the current forward; WAR barriers (`_apply_war_barrier`) fence shared-buffer writes.
- Schedules via pluggable **`SchedulePolicy`** (`schedule_policy.py`: FCFS, longest-prefix-first, etc.).
- Decomposed into **`scheduler_components/`** — request receiver, output sender/streamer, metrics reporter, idle sleeper, weight updater, IPC channels, invariant checker, etc.
- Supports **prefill–decode disaggregation** (`disaggregation/`: separate prefill/decode processes exchanging KV via Mooncake/etcd rendezvous), **DP attention**, **speculative decoding** (`speculative/`), **LoRA** (`lora/`), **elastic EP** (`elastic_ep/`), and multimodal (`multimodal/`, `managers/mm_utils.py`).

**`TpWorker`** (`managers/tp_worker.py`) drives the actual GPU work: `model_runner.py` + `runner/` (eager, CUDA-graph decode/prefill runners, flashinfer autotune) + `layers/` — attention has **20+ backend implementations** (flashinfer, flash-attention, Triton, torch-native, MLA variants, sparse/hybrid/NSA, etc.), plus MoE kernels (deep_gemm, eplb).

**`mem_cache/`** — memory management: **RadixAttention** (`radix_cache.py`, hierarchical radix-tree prefix caching for automatic reuse across requests), unified memory pool/allocator, chunk cache, mamba pools, HiCache hybrid offload, eviction policies, and C++ radix tree bindings.

**`distributed/`** — tensor/pipeline/data parallelism (`parallel_state.py`, NCCL device communicators, bootstrap), used by `connector/` (e.g., DeepSeek connector), `eplb/` (expert-parallel load balancing).

**`hardware_backend/`** — GPU/CPU/NPU/XPU/MLX/MUSA abstractions; `platforms/` per-accelerator detection. **`constrained/`** — structured output: xgrammar/llguidance/outlines grammar backends with a compressed-FSM reasoner. **`checkpoint_engine/`, `model_loader/`, `weight_cache/`** — model loading & weight management. **`tokenizer/`**, `configs/`, `arg_groups/` — tokenizer + typed config groups. **`observability/`**, `plugins/`, `state_capturer/`, `compilation/` (torch.compile), `dllm/` (disaggregated long LLM).

## The Rust serving core (`rust/sglang-server/`)

A performance-critical rewrite of the frontend, **embedded into Python via pyo3** (`cdylib`):

- **Thread layout**: axum API server (tokio, core set A) → tokenizer (pinned OS threads, set B) → detokenizer (shards, set C) → TM ingress/egress (ring buffers, `ring.rs`).
- `api_server/` — `openai.rs`, `native_api.rs`, `submit.rs`, streaming frames.
- `tokenizer_manager/{ingress,egress}.rs` — FSM driving request intake/egress; Python's `TokenizerManager` drains ingress / pushes batches across the FFI boundary.
- `runtime.rs` bootstraps everything; `request_shutdown` aborts in-flight work with a bounded join.
- `sglang-grpc/` — Rust gRPC servicer whose `RuntimeHandle` calls back into Python's scheduler (`grpc_bridge.py`); compiled as `sglang/srt/grpc/_core.so`.

## Process topology

- **One process**: scheduler + GPU worker + tokenizer manager; the Rust server runs in the same process, keeping tokenize/detokenize/HTTP off the Python GIL.
- **Distributed**: multiple scheduler processes coordinate via Redis/NATS (etcd for disaggregation), gRPC KV-transfer for PD-disagg, Ray for cluster launching, and `sgl-model-gateway` for routing/load balancing.

## Key architectural ideas

1. **RadixAttention** — prefix caching as the backbone optimization; all KV memory is tree-structured and shared across requests.
2. **Zero-overhead continuous batching** — the tight scheduler loop with CPU/GPU overlap; batching is the default, not a special mode.
3. **Pre-decode disaggregation** — separate prefill (compute-heavy) and decode (memory-bound) pools, with KV cache shipped between them.
4. **Pluggability everywhere** — attention backends, schedule policies, grammar backends, hardware platforms, model implementations (`models/` has ~150+ model classes), and runner backends are all registry/class-based.
5. **Frontend/backend split** — the `lang` DSL is decoupled from any runtime; backends (`runtime_endpoint.py`, OpenAI, etc.) are swappable.

Recent commits show active work on the Rust server (TCP TTFT stalls), quantization kernels, and a runtime-context config refactor moving toward per-role namespace enforcement.
