---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nano-vLLM Architecture and Performance
translated: false
type: note
---

Here's a comprehensive explanation of **Nano-vLLM**:

---

## What is Nano-vLLM?

**Nano-vLLM** is a lightweight, from-scratch reimplementation of [vLLM](https://github.com/vllm-project/vllm) — a high-performance LLM inference engine. It achieves **comparable throughput** (even slightly faster in benchmarks) in **~1,200 lines of Python code**, making it an excellent educational resource for understanding how modern LLM inference engines work under the hood.

---

## Architecture Overview

The project is organized into these layers:

```
nanovllm/
├── llm.py              # Entry point (inherits LLMEngine)
├── config.py            # Configuration dataclass
├── sampling_params.py   # Sampling parameters (temperature, max_tokens)
├── engine/
│   ├── llm_engine.py    # Main orchestration loop (generate, step)
│   ├── scheduler.py     # Batching & scheduling logic
│   ├── model_runner.py  # GPU model execution, KV cache, CUDA graphs
│   ├── sequence.py      # Request/sequence state tracking
│   └── block_manager.py # KV cache block allocation & prefix caching
├── models/
│   └── qwen3.py         # Qwen3 model definition (transformer layers)
├── layers/
│   ├── attention.py     # FlashAttention wrapper + custom KV cache Triton kernel
│   ├── linear.py        # Tensor-parallel linear layers
│   ├── embed_head.py    # TP-aware embedding & LM head
│   ├── sampler.py       # Temperature-scaled sampling (torch.compiled)
│   ├── activation.py    # SiLU activation
│   ├── layernorm.py     # RMSNorm
│   └── rotary_embedding.py  # RoPE
└── utils/
    ├── context.py       # Thread-local context (prefill/decode metadata)
    └── loader.py        # Safetensors weight loader with TP sharding
```

---

## Key Features

### 1. **Continuous Batching** (`scheduler.py`)

Like vLLM, Nano-vLLM uses **iterative-level scheduling** — after each step, the scheduler decides which sequences to process:

- **Prefill phase**: Processes prompt tokens for new sequences, supports **chunked prefill** (partial prompt processing) to fill the batch optimally.
- **Decode phase**: Generates one token per active sequence in the batch.
- **Preemption**: When KV cache runs out, running sequences are evicted back to the waiting queue (their blocks are freed).

### 2. **Paged KV Cache** (`block_manager.py`, `model_runner.py`)

KV cache is divided into fixed-size **blocks** (default 256 tokens each), managed by a `BlockManager`:

- **Dynamic allocation**: Blocks are allocated on demand as sequences grow.
- **Prefix caching** (`hash_blocks` / `can_allocate`): Uses **xxhash** to compute hashes of token blocks. When a new request shares a common prefix with a previous one, cached KV blocks are **reused** (reference-counted), avoiding redundant computation.

### 3. **Tensor Parallelism** (`linear.py`, `embed_head.py`)

Supports splitting model layers across multiple GPUs:

- `QKVParallelLinear`, `MergedColumnParallelLinear`, `RowParallelLinear` — shard weights along the hidden/head dimension.
- `VocabParallelEmbedding` / `ParallelLMHead` — distribute vocabulary across GPUs with `all_reduce` / `all_gather`.
- Multi-process setup using `torch.multiprocessing` with shared memory (`SharedMemory`) for IPC.

### 4. **FlashAttention Integration** (`attention.py`)

Uses the `flash-attn` library for both prefill (`flash_attn_varlen_func`) and decode (`flash_attn_with_kvcache`). A custom **Triton kernel** (`store_kvcache_kernel`) efficiently writes KV cache entries into the paged cache blocks.

### 5. **CUDA Graph Capture** (`model_runner.py`)

For **decode** steps (which have fixed-size operations), CUDA graphs capture the entire model forward pass, eliminating Python and CUDA launch overhead. This is disabled when `enforce_eager=True`.

### 6. **Torch Compiled Sampler** (`sampler.py`)

The sampling step uses `@torch.compile` for faster top-k style sampling with temperature scaling.

---

## Performance

On an RTX 4070 Laptop (8GB) with Qwen3-0.6B (256 sequences):

| Engine | Throughput (tok/s) |
|--------|-------------------|
| vLLM   | 1,361.84          |
| Nano-vLLM | **1,434.13**   |

---

## How It Works End-to-End

1. **User calls** `llm.generate(prompts, sampling_params)`.
2. **Requests are enqueued** as `Sequence` objects.
3. **Scheduler** decides which sequences to run each iteration (prefill or decode).
4. **ModelRunner** prepares inputs (token IDs, positions, slot mappings, block tables), runs the model, and samples output tokens.
5. **Results** are collected and decoded back to text.

This is a fantastic resource for anyone wanting to understand LLM inference internals — batching, KV cache management, prefix caching, tensor parallelism, and GPU optimization techniques — all in readable, self-contained code.
