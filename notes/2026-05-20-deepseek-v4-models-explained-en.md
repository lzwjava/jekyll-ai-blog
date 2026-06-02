---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek V4 Models Explained
translated: false
type: note
---

**Question:** Why are DeepSeek V4 Pro and V4 Flash so good? Why do they rank at the top on OpenRouter? How cheap are they and what's the community feedback?

---

**Answer:**

DeepSeek dropped V4 Pro and V4 Flash on April 24, 2026. Here's the full breakdown — architecture, benchmarks, pricing math, and honest community feedback.

---

## Architecture: Why It's Fast and Cheap

Three key innovations explain the cost/performance:

### 1. MoE with aggressive sparsity
V4 Pro has 1.6T total parameters but only 49B active per token. V4 Flash has 284B total with 13B active. Inference costs are a fraction of what a dense model requires.

### 2. KV cache compression
The model uses a combination of Compressed Sparse Attention and Hybrid Compression Attention that reduces KV cache memory to just 10% of what V3.2 required. This makes the 1M token context window actually viable for production use.

### 3. Manifold-Constrained Hyper-Connections (mHC) for stable training
Standard residual connections pass a single vector forward. Hyper-Connections widen this into multiple parallel streams — theoretically improving expressivity. Unconstrained Hyper-Connections caused catastrophic training divergence in DeepSeek's 27B experiments, with signal amplification exceeding 3,000x. The mHC framework solves this by constraining the residual connection mixing matrices to the Birkhoff Polytope using the Sinkhorn-Knopp algorithm — dropping signal amplification to 1.6x, enabling stable training at 1.6T parameters.

They also use the Muon optimizer for pre-training — chosen for faster convergence and greater stability compared to standard AdamW, and notably, trained V4 on Huawei Ascend 950PR chips, not NVIDIA hardware — a significant geopolitical and supply-chain signal.

---

## Pricing: The Actual Math

| Model | Input $/M | Output $/M |
|---|---|---|
| DeepSeek V4 Pro | $1.74 | $3.48 |
| DeepSeek V4 Flash | $0.14 | $0.28 |
| Claude Opus 4.6 | ~$15 | ~$25 |
| GPT-5.5 | $5 | $30 |

That is a 7x price gap at near-identical coding benchmark performance vs Claude Opus 4.6. V4-Flash costs 89x less than Claude Opus 4.6 per output token.

At scale: at 100M output tokens per month, you'd pay $348 for V4-Pro versus $2,500 for Claude Opus 4.6.

V4 Flash even has a free tier on OpenRouter — $0/M input, $0/M output, with a 1M token context and 384K max output.

---

## Benchmark Reality Check

### Where V4 Pro genuinely leads (coding):
On SWE-bench Verified it scores 80.6% versus V4-Pro's 80.6% — within 0.2 points of Claude. On Terminal-Bench 2.0, V4-Pro leads Claude (67.9% vs 65.4%). On LiveCodeBench it hits 93.5% vs Claude's 88.8%.

### Where V4 Flash holds up:
V4-Flash is a genuinely serious model, not a stripped-down fallback. On SWE-bench Verified it scores 79.0% versus V4-Pro's 80.6% — a 1.6-point gap. On LiveCodeBench it hits 91.6% versus 93.5%. For most developer coding tasks, these are functionally equivalent results.

### Where it still trails:
HLE (Humanity's Last Exam) at 37.7% puts V4-Pro below Claude (40.0%), GPT-5.4 (39.8%), and well below Gemini-3.1-Pro (44.4%). SimpleQA-Verified at 57.9% versus Gemini's 75.6% reveals a meaningful factual knowledge retrieval gap.

---

## Community Feedback

Mixed but directionally positive:

Reddit reactions: "DS-V4 nice, but it's mid, not SOTA." For coding specifically, it's competitive with or ahead of frontier models. For reasoning, it trails.

In a 38-task benchmark vs Claude and GPT, DeepSeek V4 Pro received the only financial research 10/10 — it produced the strongest answer to an NVDA game theory task. Its relative weakness is presentation format more than analysis quality — strong markdown research, but Claude more readily produces dashboard-ready charts and metric cards.

For tasks requiring 30+ sequential tool calls or sustained complex planning, V4 Pro shows more drift than Claude Opus 4.7. For shorter agentic loops — the kind you'd use for standard agentic coding workflows — the performance difference is much smaller and often immaterial.

The broader trend: Qwen 3.6 Plus from Alibaba is competing at a similar level in coding-specific benchmarks. GLM 5.1 made similar noise earlier in 2026. The gap between open-weight and closed-model performance is compressing at a rate that seemed implausible two years ago.

---

## Practical Routing Strategy (for your agent/CLI workloads)

Given your usage profile (~1.5B tokens/year, CLI agents, OpenRouter):

```python
# Model routing heuristic for cost-optimized agentic stacks
def route_model(task):
    if task.type in ["code_generation", "code_review", "agentic_coding"]:
        if task.complexity == "high" or task.tool_calls > 30:
            return "deepseek/deepseek-v4-pro"   # $3.48/M out, frontier coding
        else:
            return "deepseek/deepseek-v4-flash"  # $0.28/M out, ~same SWE-bench
    elif task.type in ["factual_recall", "complex_reasoning", "writing"]:
        return "anthropic/claude-opus-4-6"       # leads on HLE, SimpleQA
    else:
        return "deepseek/deepseek-v4-flash:free" # zero cost, 1M ctx
```

The API maintains compatibility with both OpenAI ChatCompletions and Anthropic API formats, so swapping into your existing OpenRouter setup is zero friction.

**Bottom line**: For your use case (code-heavy, agent-heavy, high token volume), V4 Flash is probably the most interesting model right now — 79% SWE-bench at effectively free on OpenRouter, 1M context, and production-grade throughput. Pro makes sense when you need the extra reasoning depth and can absorb ~$3.50/M output.

---

**References:**

- [DeepSeek V4 Pro — OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-pro)
- [DeepSeek V4 Flash — OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-flash)
- [DeepSeek V4-Pro Review: Benchmarks, Pricing & Architecture](https://www.buildfastwithai.com/blogs/deepseek-v4-pro-review-2026)
- [DeepSeek V4 vs Claude vs GPT-5.4: 38-Task Benchmark](https://fundaai.substack.com/p/deepdeepseek-v4-vs-claude-vs-gpt)
- [DeepSeek V4 Coding Benchmarks — BSWEN](https://docs.bswen.com/blog/2026-04-26-deepseek-v4-vs-claude-opus-gpt-coding-benchmarks-2026/)
- [DeepSeek V4: Open-Source Frontier Model Review — MindStudio](https://www.mindstudio.ai/blog/deepseek-v4-open-source-frontier-model-review)
- [DeepSeek V4 — DataCamp](https://www.datacamp.com/blog/deepseek-v4)
