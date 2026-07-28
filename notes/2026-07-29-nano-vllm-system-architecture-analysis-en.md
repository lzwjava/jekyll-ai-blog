---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nano-vLLM System Architecture Analysis
translated: false
type: note
---

Now I have a thorough understanding of the entire system. Here's my analysis:

---

## How Nano-vLLM Works

Nano-vLLM is a **lightweight production inference engine** (not a training/single-inference framework). It implements the core architecture of vLLM (a high-throughput LLM serving system) in ~1,200 lines of readable Python. Here's the architecture:

### 1. Architecture Overview

```
LLM (user-facing API)
 └─ LLMEngine
     ├─ ModelRunner (loads model, runs forward pass)
     ├─ Scheduler (manages batching + scheduling)
     ├─ BlockManager (paged KV cache with prefix caching)
     └─ Sequence (tracks per-request state)
```

### 2. Core Components

**Scheduler** (`scheduler.py`): The heart of the system. It has two modes:
- **Prefill** (first-time compute): Processes prompt tokens. Supports *chunked prefill* — if a prompt is too long, it's split across multiple steps.
- **Decode** (autoregressive generation): Produces one token per sequence per step. If KV cache runs out, it *preempts* sequences (deallocates their cache, moves them back to the waiting queue).

**Paged KV Cache** (`block_manager.py`): Instead of a monolithic KV cache per sequence, KV cache is split into fixed-size **blocks** (256 tokens each). A `BlockManager` maintains:
- A free list of blocks
- A hash table from content hash → block ID for **prefix caching** (sharing common prefixes)
- Reference counting for block sharing (copy-on-write semantics)

**Attention with Paged Cache** (`attention.py`): Custom attention that:
- Stores computed K/V entries into the paged cache via `slot_mapping`
- During prefill with prefix cache, *gathers* cached K/V from the paged cache and concatenates with newly computed ones
- During decode, gathers all cached K/V from paged blocks before calling `scaled_dot_product_attention`

**Tensor Parallelism** (`linear.py`, `embed_head.py`): Uses NCCL to shard QKV projections, embedding, and LM head across multiple GPUs. Uses `all_reduce` for row-parallel layers and `gather` for the LM head output.

**CUDA Graphs** (`model_runner.py`): Captures decode iterations into CUDA graphs for ~10-30% faster single-token generation. Falls back to eager mode for large batch sizes (>512 sequences) or during prefill.

**Sampler** (`sampler.py`): A temperature-scaled random sampling using the Gumbel-max trick: `argmax(softmax(logits / T) / exp(1))`.

### 3. Lifecycle of a Request

```
generate(prompts)
  ├─ add_request() -> create Sequence, add to waiting queue
  └─ while not is_finished():
        step()
          ├─ scheduler.schedule() -> pick sequences for prefill/decode
          ├─ model_runner.run(seqs, is_prefill)
          │     ├─ prepare_inputs() -> build input_ids, positions, block tables, slot mappings
          │     ├─ model.forward(input_ids, positions) -> hidden states
          │     │     └─ per layer: attn + MLP (with paged K/V store/load)
          │     └─ lm_head(hidden_states) -> logits
          └─ scheduler.postprocess() -> append tokens, detect EOS
```

---

## Differences from Normal nanoGPT Inference

### 1. **Batching (Continuous Batching)**

| nanoGPT | Nano-vLLM |
|---------|-----------|
| Single sequence at a time | **Multiple sequences batched together** |
| Fixed batch (all same length) | **Variable-length sequences dynamically scheduled** |
| No scheduling overhead | Scheduler decides which sequences run each step |

### 2. **Memory Management: Paged KV Cache vs. Monolithic Cache**

| nanoGPT | Nano-vLLM |
|---------|-----------|
| Allocates `max_seq_len × num_layers × ...` per sequence (wasteful) | **Paged blocks** allocated on-demand; no pre-allocation |
| No sharing between sequences | **Prefix caching**: identical prompt prefixes share KV blocks (detected via xxhash) |
| KV cache fragmentation | **Defragmentation-free** due to paging |
| OOM for long sequences | Blocks evicted/preempted gracefully |

### 3. **Prefill vs. Decode Separation**

| nanoGPT | Nano-vLLM |
|---------|-----------|
| Single forward pass, no distinction | Two distinct phases: **prefill** (compute-heavy, batch all prompt tokens) and **decode** (memory-bound, 1 token/seq) |
| No chunking | **Chunked prefill**: splits very long prompts across multiple steps to avoid GPU OOM |

### 4. **Optimizations Absent in nanoGPT**

| Feature | What it does |
|---------|-------------|
| **Tensor Parallelism** | Shards model across multiple GPUs (QKV splits, all-reduce) |
| **CUDA Graphs** | Captures decode kernel launches into a reusable graph, reducing CPU launch overhead |
| **Prefix Caching** | Content-based hash matching to reuse KV cache blocks across requests with shared prefixes (e.g., system prompts) |
| **Preemption** | If KV cache is full, the scheduler kicks out running sequences (deallocates blocks) and reschedules them later |
| **Variable-batch CUDA Graphs** | Pre-captures graphs for batch sizes `[1, 2, 4, 8, 16, 32, ... 512]` and selects the closest matching one |

### 5. **Throughput Focus**
- nanoGPT's `sample.py` inference is designed for **single-sample generation**, prioritizing simplicity
- Nano-vLLM is designed for **high-throughput serving**: benchmarks show ~1434 tok/s on a laptop RTX 4070, matching/beating vLLM itself

### 6. **Architecture Support**
- Nano-vLLM currently implements the **Qwen3** model architecture specifically
- nanoGPT supports the original GPT-2 small/medium/large
- Nano-vLLM supports modern features like GQA (Grouped Query Attention), RoPE (Rotary Position Embedding), QKV bias, QK-Norm, etc.

### 7. **Sampling**
- Nano-vLLM only supports **temperature-based random sampling** (no top-k, top-p, or greedy)
- nanoGPT supports temperature, top-k, and top-p sampling

In short: **nanoGPT** ≈ single-sequence inference playground; **Nano-vLLM** ≈ a full production-grade inference engine implementing the same scheduling, caching, and parallelism techniques as vLLM, just in a clean, minimal codebase.
