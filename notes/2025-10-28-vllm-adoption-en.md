---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: vLLM Adoption by AI Providers
translated: false
type: note
---

### Usage of vLLM by AI Providers

vLLM is an open-source inference engine commonly recommended for serving open-weight models efficiently. However, its adoption in production services varies. Below is a breakdown based on available information:

| Provider/Model | Uses vLLM in Production? | Details |
|---------------|---------------------------|---------|
| **Claude (Anthropic)** | No | Anthropic relies on proprietary infrastructure for serving Claude models. vLLM offers compatibility for local or third-party deployments mimicking Anthropic's API, but there's no evidence of internal use. |
| **OpenAI (GPT models)** | No | OpenAI uses custom, in-house serving systems optimized for scale. vLLM supports OpenAI-compatible APIs for local inference, but OpenAI does not base its production on vLLM. |
| **Minimax AI** | No | MiniMax open-sources models like MiniMax-M1/M2 and recommends vLLM for user deployments due to its performance. No confirmation of vLLM in their core production API; they may use forks or custom setups. |
| **Kimi (Moonshot AI)** | No | Moonshot recommends vLLM for self-hosting Kimi-K2, and their Checkpoint-Engine tool integrates with it for weight updates. However, their production inference likely uses proprietary optimizations alongside engines like SGLang or TensorRT-LLM. |
| **DeepSeek AI** | Yes | DeepSeek has open-sourced a custom inference engine built directly on vLLM, incorporating optimizations from their research. This is used for models like DeepSeek-V3 and R1, with contributions back to the vLLM project. |

### References

- [DeepSeek Open-Sources Custom Inference Engine Built on vLLM](https://www.ainews.com/p/deepseek-open-sources-custom-inference-engine-built-on-vllm)
- [The path to open-sourcing the DeepSeek inference engine](https://news.ycombinator.com/item?id=43682088)
- [MiniMax-M1 Hybrid Architecture Meets vLLM](https://blog.vllm.ai/2025/06/30/minimax-m1.html)
- [Kimi K2: Open Agentic Intelligence](https://moonshotai.github.io/Kimi-K2/)
- [OpenAI-Compatible Server - vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)
- [Support Anthropic API `/v1/messages` endpoint · Issue #21313 · vllm-project/vllm](https://github.com/vllm-project/vllm/issues/21313)
