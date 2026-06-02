---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang on AMD Cloud for LLM Inference
translated: false
type: note
---

**Question:** What is SGLang, and why is it offered as an option on AMD Developer Cloud?

**Answer:**

SGLang (Structured Generation Language) is a **high-performance LLM inference serving framework** — think of it as a serious competitor to vLLM, but with a different architectural philosophy and some sharp technical advantages.

## What SGLang Is

SGLang is an efficient serving engine for large language models and vision-language models. Its core inference optimizations include prefill-decode disaggregation, large-scale expert parallelism, a zero-overhead scheduler, and speculative decoding. It's widely adopted across the industry to serve frontier models like Grok3 and DeepSeek V3/R1.

The project is led by Lianmin Zheng (Berkeley → xAI). SGLang is the high-performance serving infrastructure powering trillions of tokens daily, and it joined the PyTorch ecosystem in early 2025. It provided day-one support for DeepSeek V3/R1 models on both NVIDIA and AMD GPUs with DeepSeek-specific optimizations.

## Key Technical Features (vs. vLLM)

| Feature | SGLang | vLLM |
|---|---|---|
| **Scheduler** | Zero-overhead, RadixAttention for KV cache reuse | Good but more overhead |
| **PD Disaggregation** | First-class support | Added later |
| **MoE Expert Parallelism** | Large-scale EP at 96+ GPUs | Catching up |
| **Speculative decoding** | Yes | Yes |
| **Structured output** | Native (it's in the name) | Via guided decoding |

**RadixAttention** is SGLang's key differentiator — it does automatic KV cache reuse across requests sharing a common prefix (system prompts, few-shot examples). This is massive for throughput in production workloads where many requests share the same long prefix.

## Why AMD Developer Cloud Specifically Uses It

ROCm 7 introduces a robust approach to distributed inference, leveraging the open-source ecosystem including frameworks like SGLang, vLLM, and llm-d. AMD is going all-in on open-source inference stacks to challenge NVIDIA's CUDA moat. SGLang runs natively on ROCm (AMD's CUDA equivalent).

AMD has integrated DeepSeek-V3 on AMD Instinct GPUs, optimized for performance powered by SGLang. The MI300X (192GB HBM3) is particularly well-suited for large MoE models like DeepSeek-R1 (671B params), and SGLang's large-scale expert parallelism maps well onto that hardware.

## Quick Start (on AMD Developer Cloud or any ROCm box)

```bash
# Pull SGLang with ROCm support
docker pull lmsysorg/sglang:latest-rocm

# Serve DeepSeek-R1 on MI300X
docker run --device=/dev/kfd --device=/dev/dri \
  --group-add video --shm-size 128g \
  lmsysorg/sglang:latest-rocm \
  python -m sglang.launch_server \
    --model deepseek-ai/DeepSeek-R1 \
    --tp 8 \
    --port 30000
```

```python
# Client-side — OpenAI-compatible
import openai
client = openai.Client(base_url="http://localhost:30000/v1", api_key="none")

resp = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[{"role": "user", "content": "Explain KV cache reuse"}]
)
```

## TL;DR for Your Work

If you're running inference on AMD Developer Cloud (MI300X), SGLang is the **recommended serving backend** — better than vLLM for:

- Long shared-prefix workloads (agents, RAG)
- DeepSeek-class MoE models (large expert parallelism)
- High-throughput batch workloads with speculative decoding

It's the xAI/Grok production stack, open-sourced. Treat it as the inference engine of the frontier labs that isn't NVIDIA-locked.

**References:**

- [SGLang GitHub](https://github.com/sgl-project/sglang)
- [AMD ROCm 7 + SGLang announcement](https://www.amd.com/en/blogs/2025/enabling-the-future-of-ai-introducing-amd-rocm-7-and-the-amd-developer-cloud.html)
- [AMD Advancing AI 2025 — Lianmin Zheng SGLang talk](https://www.amd.com/en/corporate/events/advancing-ai/2025/advancing-ai-2025.html)
- [DeepSeek-V3 on AMD with SGLang](https://amd.com/en/developer/resources/technical-articles/amd-instinct-gpus-power-deepseek-v3-revolutionizing-ai-development-with-sglang.html)
