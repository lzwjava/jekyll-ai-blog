---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Nano-vLLM: Minimal vLLM Reimplementation"
translated: false
type: note
---

This agent project is **nano-vllm** — a from-scratch reimplementation of vLLM's serving engine in ~1,200 lines of Python. Here's how it works, top to bottom:

## The core loop (LLMEngine → Scheduler → ModelRunner)

**1. You call `llm.generate(prompts, sampling_params)`** (`llm.py` → `engine/llm_engine.py`). This:

- tokenizes each prompt into a `Sequence`
- dumps them into the `Scheduler`'s waiting queue
- then repeatedly calls `step()` until every sequence finishes

**2. Each `step()` is one GPU forward pass, and this is the heart of the system:**

```
uvloop:   step() -> scheduler.schedule() -> model_runner.run() -> scheduler.postprocess()
```

## Why it's fast: continuous batching

Naive serving processes one request at a time. nano-vllm instead packs *many* sequences into one forward pass:

- **Prefill phase** — new prompt tokens are processed in a packed batch (`prepare_prefill` builds one contiguous tensor); the scheduler greedily fills up to `max_num_batched_tokens` and `max_num_seqs`.
- **Decode phase** — when nothing is waiting, each running sequence contributes exactly **1 token** (`input_ids[i] = seq.last_token`), so all sequences advance in parallel. As soon as one finishes (`EOS` / `max_tokens`), it's removed and the next waiting sequence is **scheduled in immediately** (vLLM's "continuous batching") — no waiting for the batch to drain.

So a 256-request benchmark runs them all concurrently instead of serially. That's how it hits ~1434 tok/s on a laptop 4070.

## PagedAttention: KV cache as pages

Instead of one contiguous KV buffer per sequence, the KV cache for every layer is a single global tensor:

```python
self.kv_cache = torch.empty(2, num_layers, num_blocks, block_size, num_kv_heads, head_dim)
```

Each `Sequence` gets a `block_table` (list of block IDs), like a page table. A `BlockManager` tracks free blocks (`ref_count`, free list). Two consequences:

- **Zero fragmentation** — a finished sequence's blocks are immediately reusable by others, even if its story ended at position 7771.
- **Prefix caching** — blocks store a rolling `xxhash` (`hash_blocks`). When a new prompt arrives, `scheduler.can_allocate` checks already-computed hashes: if a prompt shares a prefix with a previous one, those blocks are **reused with `ref_count += 1`** and only the suffix is computed. This is the `block_tables`/`_gather_kv_from_cache` path in `attention.py`.

During decode the runner reads the full history by *gathering* from the paged cache, so attention cost is exactly proportional to sequence length — the reason decode is memory-bandwidth-bound.

## The model runner (`model_runner.py`)

This is the only part that touches the GPU:

```python
dist.init_process_group("nccl", ...)       # Tensor parallelism (world_size ranks)
warmup_model()                              # dummy run to allocate workspace/mem pools
allocate_kv_cache()                         # sizes cache from free GPU mem * gpu_memory_utilization
capture_cudagraph()                         # unless enforce_eager
run()  -> prepare_prefill/decode + forward + sampler
```

Key optimizations that mirror real vLLM:

- **`prepare_prefill`** builds `cu_seqlens_q/k`, `slot_mapping`, `block_tables` so a single `flash_attn_varlen_func` call handles a whole ragged batch (including prefix-cache offset causal masks).
- **CUDA graphs** — the decode forward pass is captured into a `CUDAGraph` per batch-size bucket (`graph_bs = [1,2,4,8,16,...]`). Graph capture eliminates Python/launch overhead per token; the only `.item()`-free path is used because conditionals are illegal during capture (see the `is_current_stream_capturing()` branch in `attention.py`).
- **Chunked prefill** — one overly-long prompt can't starve the batch; the scheduler breaks prefill into chunks (`only allow chunked prefill for the first seq`).
- **Preemption** — if decode has no free blocks, the scheduler evicts the LIFO running sequence back to WAITING and frees its blocks.
- **Tensor parallelism** — rank-0 orchestrates via shared-memory IPC (page-sized pickle in `SharedMemory`), workers run slices; only rank 0 samples.
- **Pin-memory + `non_blocking=True`** H2D copies of inputs.

## The learning angle (from `AGENTS.md`)

The point of this repo isn't "use vLLM" — it's to *see* the serving machinery. The `experiments/` folder is the designed learning loop:

```bash
python3.12 experiments/04_scheduler_watch.py     # watch continuous batching live
python3.12 experiments/07_mixed_length_batch.py  # mixed-length batching
```

Experiment 1 is the "aha": decode latency grows linearly with prompt length (31ms/tok → 1159ms/tok from 4→2048 tokens) because attention re-reads the whole KV cache every step — the exact problem PagedAttention + batching solve. This is the inference-systems analog of nanoGPT's loss curve.

Note the env detail: always use `python3.12` (system `/usr/bin/python3.12`), never `python3`, since the deps target `>=3.10,<3.13`.

Want me to walk through any piece in more detail — say the scheduler's preemption logic, CUDA graph capture, or prefix caching hashing?
