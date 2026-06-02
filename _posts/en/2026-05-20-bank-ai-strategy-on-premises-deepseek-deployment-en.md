---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Bank AI Strategy: On-Premises DeepSeek Deployment"
translated: false
type: note
---

**Question:** In a big bank context, should I be serving DeepSeek V4 models (Flash and Pro) internally — making them work on-prem — rather than calling DeepSeek's external API?

**Answer:**

Yes, that is exactly the right framing. Here's the full picture.

---

## DeepSeek V4 — What Was Just Released

On April 24, 2026, DeepSeek released DeepSeek V4 and V4-Pro. V4-Pro has 1.6T total / 49B active parameters; V4-Flash has 284B total / 13B active parameters. Both support a 1M token context window. Both are licensed under the MIT License with weights published on Hugging Face.

Key architectural innovations:

- A Hybrid Attention Architecture combining Compressed Sparse Attention (CSA) and Heavily Compressed Attention (HCA); in the 1M-token setting, V4-Pro requires only 27% of single-token inference FLOPs and just 10% of the KV cache compared to V3.2.
- Both models support three reasoning effort modes (Thinking / Non-Thinking) and are integrated with agents like Claude Code and OpenCode.

---

## Why You Should Self-Host in a Big Bank (Not Call DeepSeek's API)

This is the critical point. DeepSeek's hosted API involves Chinese data residency. For teams in regulated industries or with US/EU compliance requirements, self-hosting the open weights is the clean path — it sidesteps data sovereignty concerns entirely and gives you full control over inference behavior.

Banks have:

- **Data residency requirements** — customer data, trade data, internal comms cannot leave approved jurisdictions
- **Third-party vendor risk policies** — routing production traffic to a Chinese-hosted API won't pass InfoSec review
- **Model auditability requirements** — you need to know exactly which weights you're running, not a "preview" that can silently change

MIT license + open weights = you can download, run, and lock the weights in your own infra. This is the entire value proposition for a bank.

---

## Hardware Reality

For most teams running V4-Flash, two H200 SXM in a single pod is the sweet spot — 282 GB of HBM3e fits the model plus comfortable KV for 256K context. If you need full 1M context or high QPS, scale to 8× H200. For V4-Pro, the minimum single-node config is 8× H200 (1,128GB); full 1M context on V4-Pro requires a two-node H200 cluster.

**Practical tiers:**

| Model | Weights Size | Minimum Self-Host | Context |
|---|---|---|---|
| V4-Flash | ~160 GB (FP8) | 2× H100/H200 | 1M tokens |
| V4-Pro | ~865 GB | 8× H200 (single-node) | up to 800K |
| V4-Pro (full 1M) | ~865 GB | 2-node H200 cluster | 1M tokens |

For most self-hosting scenarios, V4-Flash is the practical choice — you get 85–95% of V4-Pro's quality at a fraction of the infrastructure cost. V4-Pro self-hosting makes sense for organizations with existing GPU clusters that need the absolute best open-weight performance and can't send data to external APIs.

---

## The Serving Stack

The recommended path for internal deployment:

```bash
# Pull weights
huggingface-cli download deepseek-ai/DeepSeek-V4-Flash --local-dir ./ds-v4-flash

# Serve with vLLM (OpenAI-compatible endpoint)
pip install vllm
vllm serve ./ds-v4-flash \
  --model deepseek-ai/DeepSeek-V4-Flash \
  --tensor-parallel-size 2 \       # 2x H100/H200
  --max-model-len 131072 \          # 128K to start, scale to 1M with more GPUs
  --dtype bfloat16 \
  --api-key your-internal-key
```

The API is OpenAI ChatCompletions compatible, making integration straightforward for teams already using OpenAI's SDK format. Developers just need to update their model parameter to `deepseek-v4-pro` or `deepseek-v4-flash`.

Your internal apps hit `http://internal-llm-gateway/v1/chat/completions` with `model: deepseek-v4-flash` — zero code changes from existing OpenAI-compatible integrations.

For production-grade serving with auth, rate limiting, and audit logging (what banks actually need):

```
[Internal clients]
    → [Kong/Nginx API Gateway with auth + audit log]
    → [vLLM cluster serving V4-Flash / V4-Pro]
    → [GPU nodes, air-gapped network segment]
```

---

## Flash vs Pro Routing Strategy

The optimal strategy for most teams: route 70–80% of traffic to V4-Flash and escalate to V4-Pro for complex tasks.

For your context as an AI engineer at a bank:

- **V4-Flash** → code generation, test case generation, RAG over internal docs, routine automation (iclaw-style use cases)
- **V4-Pro** → complex agentic workflows, long-context document analysis (full codebase review, regulatory documents), hard reasoning tasks

---

## What This Means for Your Role

This is a high-value AI engineering project: standing up internal DeepSeek V4 serving infrastructure is exactly the kind of work that sits at the intersection of LLM systems, compliance engineering, and AI platform building. The argument to management writes itself:

1. MIT license — no licensing cost
2. On-prem — no data leaves the bank
3. 1M token context — entire codebases or regulatory docs in one call
4. OpenAI-compatible API — drop-in for existing tooling

The gap between "we can't use external LLMs due to data policy" and "we have frontier-grade models running internally" is exactly what you'd be closing.

---

**References:**

- [DeepSeek V4 Preview Release — API Docs](https://api-docs.deepseek.com/news/news260424)
- [DeepSeek-V4-Flash on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)
- [DeepSeek-V4-Pro on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)
- [RunPod: Running V4 in the wild](https://www.runpod.io/blog/deepseek-v4-in-the-wild-and-how-to-run-it-on-runpod)
- [DeepSeek V4 Flash Deep Dive — Codersera](https://codersera.com/blog/deepseek-v4-flash-deep-dive/)
- [V4 Pro vs Flash Comparison — Lushbinary](https://lushbinary.com/blog/deepseek-v4-pro-vs-flash-benchmarks-pricing-comparison/)
