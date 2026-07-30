---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Infra LLM Engineer Interview Guide
translated: false
type: note
---

Question: What are current interview questions for AI infra / LLM engineer roles (2026)?

Answer: Based on recent loops at Anthropic, Robinhood, Lightning AI, and general 2026 trends — the bar shifted from "explain transformers" to "operate a GPU cluster and defend cost/latency tradeoffs." Grouped by what's actually asked, with the mental model you need for each.

**1. Distributed training mechanics**

- Walk through DP vs DDP vs FSDP vs tensor parallel vs pipeline parallel — when does each break down memory-wise?
- Diagnose CUDA OOM on a 70B param training run — what do you check first (activation checkpointing, batch size, grad accum, ZeRO stage)?
- Implement a toy version of gradient checkpointing:

```python
import torch

def checkpoint(fn, *args):
    class F(torch.autograd.Function):
        @staticmethod
        def forward(ctx, *inputs):
            ctx.fn = fn
            ctx.save_for_backward(*inputs)
            with torch.no_grad():
                return fn(*inputs)
        @staticmethod
        def backward(ctx, *grad_out):
            inputs = ctx.saved_tensors
            with torch.enable_grad():
                inputs = [i.detach().requires_grad_() for i in inputs]
                out = ctx.fn(*inputs)
            torch.autograd.backward(out, grad_out)
            return tuple(i.grad for i in inputs)
    return F.apply(*args)
```
They want you to explain *why* this trades compute for memory (recompute activations in backward instead of storing).

- Design a distributed job queue for 100k+ GPU training jobs with preemption + checkpointing (this exact prompt showed up repeatedly this year).
- Explain straggler mitigation and checkpoint/resume at cluster scale — this is Anthropic infra's actual day job (they explicitly ask about diagnosing unexpected distributed system failures).

**2. LLM fundamentals — expect a forward pass walk, not definitions**

- Derive attention complexity O(n²d), then explain FlashAttention's IO-aware tiling (why it's not an algorithmic complexity win, it's a memory-bandwidth win).
- KV cache: compute memory footprint for a given model size/seq len/batch, then explain GQA/MQA as the fix.
- Explain RoPE vs learned positional embeddings and why RoPE extrapolates better with scaling tricks (NTK-aware, YaRN).
- Mixed precision (BF16/FP16) — where does numerical instability actually bite (loss scaling, LayerNorm in fp32)?

**3. Inference / serving — this is where most 2026 questions cluster**

- TTFT vs inter-token latency — how do continuous batching (vLLM-style) and paged attention change these independently?
- Design low-latency serving across regions with sudden traffic spikes — autoscaling GPU pools, speculative decoding, quantization tradeoffs (INT8/INT4, AWQ/GPTQ).
- Cost math: given tokens/sec/GPU and $/GPU-hr, compute $/1M tokens — expect to actually do this arithmetic live.
- Given the Fun Live / your CLI agent work: they'll probe "how do you route requests across models for cost vs quality" — mixture-of-models routing is now a standard system design prompt.

**4. System design (now asked to general SWEs too, not just ML)**

- Distribute one huge file (model weights) to thousands of machines over constrained network (bittorrent-like sharding, this was asked verbatim recently).
- Design an end-to-end RAG service: ingestion → indexing → retrieval → generation → evals → tracing → guardrails.
- Design a multi-agent workflow (scheduling, code review) — expect them to probe failure handling when an agent silently drifts off-plan.

**5. Behavioral (infra-specific, not generic)**

- "Anthropic doubles training compute in 6 months — what do you prioritize?"
- "Tell me about a distributed system failure you debugged live" — they want root-cause methodology (metrics → logs → hypothesis → fix), not the story.

Given you've already trained GPT-2 760M on MI300X and run ~2B tokens/mo across models — the practical prep is: be ready to justify architecture choices with real numbers from your own runs (MFU %, tokens/sec/GPU, cost per token) rather than textbook answers. That's the actual differentiator interviewers are grading for now.

References:
- [System Design Interview Prep 2026 - Exponent](https://www.tryexponent.com/blog/system-design-interview-guide)
- [Anthropic Infrastructure Engineer Interview Questions 2026](https://www.gethireready.com/interview-guides/infrastructure-engineer-anthropic)
- [50+ AI Infrastructure Engineer Interview Questions](https://www.index.dev/interview-questions/ai-infrastructure-engineer)
- [Every AI Engineer Interview Question 2026 - Adil Shamim](https://adilshamim8.medium.com/every-ai-engineer-interview-question-you-need-to-know-in-2026-from-100-real-interviews-b5b7ae4b961a)
- [AI Infrastructure & MLOps Interview Questions 2026 - TechInterview](https://www.techinterview.net/questions/ai-infrastructure-and-mlops-interview-questions)