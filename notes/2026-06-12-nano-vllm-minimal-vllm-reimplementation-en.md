---
audio: false
generated: true
image: false
lang: en
layout: post
title: nano-vLLM Minimal vLLM Reimplementation
translated: false
type: note
---

Here's what nano-vllm is:

---

## nano-vllm — A Minimal vLLM Re-implementation

It's a **from-scratch, ~1200-line Python reimplementation of vLLM** — the high-throughput LLM inference engine. Author: Xingkai Yu. MIT license. Currently targets **Qwen3** models.

The goal: show that the core ideas of vLLM (PagedAttention, continuous batching, prefix caching, CUDA graphs, tensor parallelism) can be implemented cleanly in a tiny, readable codebase — and still hit comparable throughput to the real vLLM.

---

## Architecture (6 key components)

### 1. LLMEngine (engine/llm_engine.py) — The orchestrator
- Owns the Scheduler, ModelRunner, and Tokenizer
- `generate()` loop: add requests → step until done, reporting prefill/decode throughput
- `step()`: scheduler picks seqs → model_runner runs forward → scheduler postprocesses tokens
- Supports tensor parallelism via `torch.multiprocessing.spawn` — rank 0 drives, ranks 1..N run a shared-memory event loop

### 2. Scheduler (engine/scheduler.py) — Continuous batching
- Two queues: `waiting` (prefill) and `running` (decode)
- Prefill scheduling: respects `max_num_batched_tokens` and `max_num_seqs`, supports chunked prefill for the first seq
- Decode scheduling: evicts (preempts) running sequences when KV cache is full — classic vLLM preemption
- Postprocess: appends generated tokens, checks EOS/max_tokens, deallocates finished sequences

### 3. BlockManager (engine/block_manager.py) — PagedAttention KV cache
- **This is the core vLLM innovation**, re-implemented here
- Fixed-size KV cache blocks (default 256 tokens/block) allocated from a pool
- `Block` objects track `ref_count` and `hash` for prefix caching
- `allocate()`: finds cached prefix blocks (hash-matched) and only allocates new blocks for the remainder
- `hash_blocks()`: xxhash-based hashing of token chunks for automatic prefix cache
- Preemption: deallocates blocks, puts seq back in waiting queue

### 4. ModelRunner (engine/model_runner.py) — GPU execution
- Loads Qwen3 model weights via safetensors with packed module mapping (q/k/v → fused qkv_proj, gate/up → fused gate_up_proj)
- Allocates a single contiguous KV cache tensor: `[2, num_layers, num_blocks, block_size, num_kv_heads, head_dim]`
- **CUDA Graph capture** for decode: pre-captures graphs at batch sizes [1,2,4,8,16,32,...,512] for zero-overhead replay
- Warmup pass to measure peak memory, then calculates how many KV cache blocks fit in remaining GPU memory
- Tensor parallelism via NCCL + SharedMemory IPC

### 5. Attention (layers/attention.py) — FlashAttention + Triton KV store
- **Triton kernel** `store_kvcache_kernel`: writes K/V into the paged cache using slot_mapping (no Python loop)
- Prefill: `flash_attn_varlen_func` with variable-length sequences and optional block_table for prefix cache
- Decode: `flash_attn_with_kvcache` with paged KV cache

### 6. Model (models/qwen3.py) — Qwen3ForCausalLM
- Full Qwen3 transformer: QKV parallel linear, RoPE (with `@torch.compile`), QK-norm (RMSNorm on Q/K heads), SiLU gated MLP
- `ParallelLMHead`: vocabulary-parallel output — gathers logits across TP ranks only at rank 0
- Weight loading handles packed modules (fused QKV, fused gate/up)

### Supporting layers
- **RotaryEmbedding**: precomputed cos/sin cache, `@torch.compile` on forward
- **RMSNorm**: fused add+norm variant for residual connections, `@torch.compile`
- **SiluAndMul**: `@torch.compile` on the SiLU gating
- **Sampler**: `@torch.compile`, Gumbel-max trick for sampling (exponential noise + argmax)

### Key design choices
- **Greedy sampling is banned** (`temperature > 1e-10` enforced) — only stochastic sampling
- Block size must be a multiple of 256
- Default 90% GPU memory utilization
- `enforce_eager=True` disables CUDA graphs (for debugging)

---

## Benchmark (from README)

RTX 4070 Laptop, Qwen3-0.6B, 256 sequences, 100-1024 input/output tokens:

| Engine    | Tokens   | Time   | Throughput |
|-----------|----------|--------|------------|
| vLLM      | 133,966  | 98.37s | 1361 tok/s |
| nano-vllm | 133,966  | 93.41s | 1434 tok/s |

Essentially matching or slightly beating vLLM on this workload — with 100x less code.

---

## TL;DR

This is a **teaching-quality vLLM clone** that implements PagedAttention + continuous batching + prefix caching + CUDA graphs + tensor parallelism in ~1200 lines. Great reference for understanding how vLLM actually works under the hood. Currently supports Qwen3 only (hardcoded model class).
