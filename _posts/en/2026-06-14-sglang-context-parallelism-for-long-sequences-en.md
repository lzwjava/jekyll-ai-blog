---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Context Parallelism for Long Sequences
translated: false
type: note
---

**Question:** What does this Chinese technical text about SGLang Context Parallel design mean?

**Answer:**

This is a slide/talk transcript explaining **why SGLang needs Context Parallelism (CP) for long-sequence inference**. Here's the full breakdown:

---

## Section 1: Motivation — Why Long Sequences Break Traditional Approaches

**Context length is scaling ~10x per generation** (GPT-1 2018 → now). Two problems compound as sequences grow:

**KV Cache memory**: KV cache size is `O(seq_len * num_layers * num_heads * head_dim)`. For a 128K token sequence on a large model, this can be tens of GBs — easily exceeding single-GPU VRAM.

**Attention compute**: Without sparse attention or sliding window, attention is `O(seq_len²)` in compute and memory. At 128K+ tokens, this is brutal.

**Why Tensor Parallelism (TP) fails here**: TP splits weight matrices across GPUs but doesn't split the *sequence dimension*. Each GPU still sees the full KV cache for its layers. You can't TP your way out of a 192K token sequence.

**The GQA/MLA wrinkle**: GQA (Grouped Query Attention, used in LLaMA 3) and MLA (Multi-head Latent Attention, used in DeepSeek) compress KV heads. This makes naive TP-based KV sharding even harder — you can't just split KV heads evenly across TP ranks when there are fewer KV heads than TP degree.

**Conclusion**: CP is no longer optional — it's the foundational primitive for long-sequence online serving.

---

## Section 2: SGLang Runtime Architecture (simplified baseline)

The current (pre-CP) runtime flow:

```
Client HTTP Request
    → VPC Server
    → TokenizerManager (tokenization → token IDs)
    → Runtime (collects batched requests)
    → Broadcast to N Workers (e.g. TP=4, so 4 workers)
        Each Worker:
            - Checks local RadixCache / KV cache (prefix reuse)
            - Runs BatchScheduler
            - Executes forward pass (attention + FFN)
    → Detokenizer
    → Response to client
```

Key terms decoded from the garbled OCR/transcript:

- **"Td4"** → TP degree 4 (4 tensor-parallel workers)
- **"PVit Cache / TdCache"** → RadixCache (SGLang's prefix-aware KV cache with tree structure)
- **"Batch Scanner"** → BatchScheduler / continuous batching loop
- **"DumpDump"** → likely "decode" steps (prefill → decode)
- **"Zero FQ"** → ZeroMQ (the IPC transport SGLang uses between tokenizer and runtime)

---

## Section 3: What CP Adds

The text ends by saying SGLang needs to **integrate CP into this existing framework** to minimize inference latency for long sequences.

In practice, CP in SGLang means:

```
Sequence [T0...T_N] split across CP ranks:
  CP rank 0: [T0 ... T_{N/2}]    → GPU 0
  CP rank 1: [T_{N/2}...T_N]     → GPU 1

Each rank computes local QKV, then:
  - Ring attention (pass K,V around the ring) for causal masking
  - Or: All-gather KV before attention (simpler, more memory)
```

This is **Ring Attention** — the standard CP primitive. SGLang's implementation handles the interaction with RadixCache (prefix reuse across CP ranks is non-trivial).

---

## Bottom Line

The text is a technical talk intro explaining:

1. Sequence length scaling → KV cache and attention compute blow up
2. TP alone can't solve it, especially with GQA/MLA
3. SGLang's current architecture (ZMQ → Runtime → TP workers → RadixCache)
4. CP needs to be layered in to handle 128K+ token serving at production throughput

If you're working through SGLang internals, the key files to read are `python/sglang/srt/managers/schedule_batch.py` (BatchScheduler), `radix_cache.py`, and the attention backends in `srt/layers/attention/`.
