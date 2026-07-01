---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang vs vLLM Differences
translated: false
type: note
---

**Question:** What are the differences between SGLang and vLLM?

**Answer:**

Both are high-performance LLM inference engines, but they have different design philosophies and optimization targets.

---

## Core Philosophy

| | **vLLM** | **SGLang** |
| --- | --- | --- |
| Origin | UC Berkeley, 2023 | Stanford, 2024 |
| Primary innovation | PagedAttention (KV cache mgmt) | RadixAttention (prefix reuse) |
| Design goal | Maximize throughput via memory efficiency | Maximize throughput via computation reuse |
| Primary abstraction | Serving engine | Structured generation language + engine |

---

## Key Technical Differences

### 1. KV Cache Management

**vLLM — PagedAttention:**

- Splits KV cache into fixed-size pages (like virtual memory)
- Eliminates KV cache fragmentation
- Allows sharing pages across parallel sequences (beam search, speculative decoding)

**SGLang — RadixAttention:**

- Organizes KV cache as a **radix tree** (trie over token sequences)
- Automatically reuses KV cache across requests that share a common prefix
- Critical win: multi-turn chat, RAG with shared system prompts, few-shot prompting — all get prefix reuse for free

```
Prefix: [system prompt tokens]
Request A: [system prompt] + [user query A]
Request B: [system prompt] + [user query B]
                ↑
        SGLang computes this once, reuses across A and B
```

### 2. Structured Output / Constrained Decoding

SGLang was originally built around **structured generation** — it has a native DSL:

```python
# SGLang native DSL (original API)
@sgl.function
def multi_turn_qa(s, question):
    s += sgl.system("You are helpful")
    s += sgl.user(question)
    s += sgl.assistant(sgl.gen("answer", max_tokens=256))
```

vLLM added structured output later via `guided_decoding` (outlines/lm-format-enforcer backend). SGLang's is tighter because the engine was designed around it from day one.

### 3. Continuous Batching & Scheduling

Both support continuous batching, but:

- vLLM uses **chunked prefill** + preemption with recompute or swap
- SGLang uses **chunk prefill with RadixAttention** — prefill chunks land in the radix tree, so later requests benefit immediately

### 4. Multi-modal & Architecture Support

As of mid-2025:

- **vLLM** has broader model support (more HuggingFace models work out-of-box)
- **SGLang** tends to be faster on supported models (LLaMA, Mistral, Qwen, DeepSeek) and has very strong **DeepSeek MLA (Multi-head Latent Attention)** support — relevant to you given your DeepSeek usage

### 5. MoE / DeepSeek Support

SGLang specifically optimized for **DeepSeek V3/R1** MoE models:

- Expert parallelism across GPUs
- MLA (latent KV compression) — DeepSeek's variant that compresses KV cache via low-rank projection
- FP8 quantization path tuned for AMD and NVIDIA

vLLM also supports DeepSeek but SGLang's team has been faster here.

---

## Benchmark Reality (approximate, varies by workload)

| Metric | vLLM | SGLang |
| --- | --- | --- |
| Throughput (shared prefix) | Baseline | +20–50% from RadixAttention |
| Throughput (no shared prefix) | ~similar | ~similar |
| TTFT (time-to-first-token) | Good | Often better with prefix reuse |
| Model coverage | Wider | Narrower but growing |
| Ease of deployment | Mature, stable | Slightly more experimental |

---

## When to Use Which

**Use SGLang when:**

- You have long shared prefixes (system prompts, RAG context, few-shot examples)
- Running DeepSeek V3/R1/MLA models
- Need tight structured output / constrained generation
- Chasing maximum throughput on supported architectures

**Use vLLM when:**

- You need maximum model compatibility
- Running diverse workloads without a dominant shared prefix
- You want the more battle-tested production path (more operators use it)
- Integrating with existing tooling (Ray Serve, KServe, etc.)

---

## Quick Start Comparison

```bash
# vLLM
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3-8B-Instruct \
  --tensor-parallel-size 1

# SGLang
pip install sglang[all]
python -m sglang.launch_server \
  --model-path meta-llama/Llama-3-8B-Instruct \
  --tp 1
```

Both expose an OpenAI-compatible `/v1/chat/completions` endpoint — drop-in swappable for most use cases.

---

**Bottom line for your workload:** Given you're running DeepSeek V3/V4 and care about throughput at scale, **SGLang is worth benchmarking seriously** — the RadixAttention wins are real when your prompts share structure (which they do in agent pipelines and multi-turn chat). vLLM is the safer production choice if you need broad compatibility or are serving a mix of models.

## References

- [SGLang Paper: Efficient Execution of Structured Language Model Programs](https://arxiv.org/abs/2312.07104)
- [vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention](https://arxiv.org/abs/2309.06180)
- [SGLang GitHub](https://github.com/sgl-project/sglang)
- [vLLM GitHub](https://github.com/vllm-project/vllm)
- [SGLang DeepSeek Support Notes](https://github.com/sgl-project/sglang/blob/main/docs/references/deepseek.md)
