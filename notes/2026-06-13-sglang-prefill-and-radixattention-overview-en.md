---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Prefill and RadixAttention Overview
translated: false
type: note
---

**Question:** What is SGLang, and how does prefill work in it?

---

## SGLang: What It Is

SGLang (Structured Generation Language) is more than just another inference server — it's a complete system for efficient LLM execution, combining a Python-embedded frontend language with a highly optimized backend runtime. The frontend provides primitives for defining complex generation programs — things like parallel prompt execution, constrained generation, and multi-step reasoning chains. The backend handles actual inference with innovations like RadixAttention for automatic KV cache sharing across requests.

Developed by the SGLang team at UC Berkeley and the open-source community, SGLang powers over 400,000 GPUs and processes trillions of tokens daily, adopted by xAI, AMD, NVIDIA, LinkedIn, Cursor, Oracle, Google Cloud, Microsoft Azure, and AWS.

It also integrates DeepSeek-specific optimizations — MLA throughput optimizations, MLA-optimized kernels, data-parallel attention, multi-token prediction, and DeepGemm — making it the top choice for serving DeepSeek models.

---

## Architecture: Two Layers

### 1. Frontend DSL (Python-native)

You write LLM programs as Python code using `sgl.*` primitives:

```python
import sglang as sgl

@sgl.function
def multi_turn_qa(s, question):
    s += sgl.system("You are a precise assistant.")
    s += sgl.user(question)
    s += sgl.assistant(sgl.gen("answer", max_tokens=256))
    s += sgl.user("Summarize your answer in one sentence.")
    s += sgl.assistant(sgl.gen("summary", max_tokens=64))
```

This lets the runtime see the *entire computation graph* ahead of time — enabling batching across branches, KV reuse across steps, and parallelism.

### 2. Backend Runtime

Key components:

- **RadixAttention** — prefix KV cache reuse (details below)
- **Chunked prefill** — interleaves prefill chunks with decode to prevent TTFT spikes
- **Zero-overhead CPU scheduler** — continuous batching without stalls
- **XGrammar** — constrained decoding via compressed FSM (structured JSON outputs)
- **FlashInfer / FlashAttention backends** — actual CUDA kernel dispatch

---

## How Prefill Works in SGLang

Standard prefill recap: given a prompt of N tokens, you run a full forward pass through all transformer layers to populate the KV cache. This is compute-bound and O(N²) in attention. Only after this do you start autoregressive decode.

SGLang's innovations on top:

### RadixAttention: Skip Redundant Prefill

In existing inference engines, the KV cache of a request is discarded after processing is completed, preventing the KV cache from being reused across multiple calls. Instead, SGLang maintains an LRU cache of the KV cache for all requests within a radix tree. This approach manages the KV cache as a traditional cache and uses a radix tree for efficient matching, insertion, and eviction.

The data structure is a **radix tree** (trie on token sequences):

```
root
├── [system_prompt_tokens...] ← cached KV for shared prefix
│   ├── [user_question_A...]  ← only compute this delta
│   └── [user_question_B...]  ← only compute this delta
```

SGLang's RadixAttention uses a radix tree to find the longest cached prefix for any incoming request and routes only the uncached suffix to the prefill compute path.

With shared prefixes, memory usage scales with unique content rather than total tokens: without prefix caching — 3 requests × 1000 tokens = 3000 tokens in memory; with prefix caching — 800 shared + 3 × 200 unique = 1400 tokens (53% savings). Cached KV states don't need to be recomputed: prefill time only computes attention for new (uncached) tokens, dramatically reducing TTFT for requests with cached prefixes.

The attention backends (FlashInfer etc.) then receive indices into the RadixCache and compute attention only over the non-cached tokens, appending new KV entries into the cache.

### Chunked Prefill

Long prompts can starve decode requests (head-of-line blocking). SGLang chunks prefill work:

- Split a 4096-token prefill into, say, 4 × 1024 chunks
- Interleave each chunk with a decode step
- GPU stays fed, decode latency doesn't spike

This is controlled by `--chunked-prefill-size` in the server.

### PD Disaggregation (Prefill-Decode Split)

SGLang achieves 52.3K input tokens/s and 22.3K output tokens/s on 96 GPUs — 5× faster than vanilla tensor parallelism — via prefill-decode disaggregation.

The idea: prefill is compute-bound (matrix-heavy), decode is memory-bandwidth-bound (small batch, lots of KV reads). Running them on the same GPU means they compete. PD disaggregation:

- **Prefill nodes**: compute-optimized, handle full prompt KV population
- **Decode nodes**: memory-bandwidth-optimized, handle token generation
- KV cache is transferred via NVLink/RDMA between nodes

SGLang supports PD disaggregation deployment mode through the Mooncake TransferEngine. SGLang also introduces HiCache, which extends RadixAttention (previously limited to GPU memory) by adding hierarchical caching support — GPU memory as L1, host memory as L2, and distributed storage as L3 — integrating with distributed storage backends such as Mooncake.

Launch it like:

```bash
# Prefill worker
python -m sglang.launch_server --model-path deepseek-ai/DeepSeek-V3 \
  --disaggregation-mode prefill --port 8001

# Decode worker
python -m sglang.launch_server --model-path deepseek-ai/DeepSeek-V3 \
  --disaggregation-mode decode --port 8002

# Router
python -m sglang.launch_router --prefill http://localhost:8001 \
  --decode http://localhost:8002
```

---

## Quick Start (your MI300X setup)

```bash
pip install sglang[all]

# Launch server
python -m sglang.launch_server \
  --model-path deepseek-ai/DeepSeek-V3 \
  --tp 8 \
  --chunked-prefill-size 2048 \
  --port 30000

# Query it
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-ai/DeepSeek-V3", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## SGLang vs vLLM on Prefill

| Feature | SGLang | vLLM |
|---|---|---|
| Prefix caching | RadixTree (automatic, LRU) | Hash-based (manual) |
| Chunked prefill | Yes | Yes |
| PD disaggregation | Native (Mooncake) | Separate (Dynamo) |
| DeepSeek MLA | Optimized kernels | Standard |
| Throughput (70B) | ~3.1× vLLM | baseline |

Given you're running DeepSeek models on MI300X, SGLang is the right call — it's the only engine with first-class MLA kernel support on AMD via ROCm.

---

## References

- [SGLang Paper: Efficient Execution of Structured LM Programs](https://arxiv.org/abs/2312.07104)
- [SGLang joins PyTorch Ecosystem](https://pytorch.org/blog/sglang-joins-pytorch/)
- [RadixAttention docs](https://sgl-project-sglang-93.mintlify.app/concepts/radix-attention)
- [HiCache + Mooncake design](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)
- [PD Disaggregation deep dive](https://www.spheron.network/blog/prefill-decode-disaggregation-gpu-cloud/)
