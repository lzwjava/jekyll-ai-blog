---
audio: false
generated: true
image: false
lang: en
layout: post
title: Per-Stage SLOs for LLM Serving
translated: false
type: note
---

Question: What does the paper at arxiv.org/abs/2504.08784 say?

Answer:

The paper introduces **SLOs-Serve**, an LLM serving system that optimizes for **per-application, per-stage SLOs** rather than the usual blanket TTFT/TPOT targets most serving stacks (vLLM, TGI, SGLang) use. SLOs-Serve is designed for serving multi-stage LLM requests with application- and stage-specific service level objectives, customizing token allocation to meet these SLO requirements.

**Core mechanism — resource planning as an optimization problem:**

SLOs-Serve uses a multi-SLO dynamic programming-based algorithm to continuously optimize token allocations under SLO constraints, exploring the full design space of chunked prefill and optional speculative decoding.

This is the part relevant to your inference-optimization interest. Instead of treating "how many tokens to chunk this prefill into" and "whether to use spec decoding for this request" as fixed scheduler policies, they formulate it as a **DP over token-budget allocation per iteration**, subject to per-stage latency constraints. Concretely, this means:

- A multi-stage pipeline (e.g., RAG retrieval → generation → tool call → final answer) has *different* latency budgets per stage. A naive scheduler treats every decode step the same; SLOs-Serve tracks remaining SLO budget per request per stage and re-solves the allocation each scheduling round.
- Chunked prefill size becomes a decision variable in the DP, not a fixed hyperparameter (vLLM's `--max-num-batched-tokens` style knobs are static; this is dynamic per-iteration).
- Speculative decoding draft-length is folded into the same optimization — i.e., "should this request use spec decode this round, and with what draft depth" becomes part of the same token-budget allocation rather than a separate orthogonal system.

**System-level capabilities built on top of the planner:**

Leveraging this resource planning algorithm, SLOs-Serve supports multi-SLOs and multi-replica serving with dynamic request routing while being resilient to bursty arrivals — so there's a routing layer across replicas that's SLO-aware (route requests to whichever replica can still meet its stage deadline), not just round-robin or least-loaded.

**Results:**

Evaluated across 6 LLM application scenarios — summarization, coding, chatbot, tool calling, and reasoning — SLOs-Serve improves per-GPU serving capacity by 2.2x on average versus prior state-of-the-art systems.

**Why this matters for you:** if you're building agent pipelines (multi-agent, tool-use, RAG) and self-hosting on your RTX 4070 or renting AMD MI300X capacity, the naive approach of running vLLM with one global SLO wastes GPU-hours — a tool-calling stage that needs a fast 50-token response gets scheduled the same as a long reasoning stage that can tolerate more latency. The DP-based per-stage allocation is the kind of thing worth stealing conceptually even if you don't run their exact system: for a custom agent server, you could implement a simplified version — track remaining latency budget per stage in your request metadata, and let your scheduler prioritize chunked prefill size based on that budget rather than FCFS. That's directly applicable to your "custom agent development and automation" work since multi-stage agent requests are exactly the workload this targets, not just single-turn chat.

One caveat: I only got the abstract from arxiv (the PDF fetch returned the same abstract page, not full text), so I don't have the exact DP formulation, complexity bounds, or their baseline comparisons (vLLM? SGLang? Sarathi?). If you want the actual math for the DP recurrence, I'd need to pull the PDF directly — worth doing if you're going to implement something similar.

References:

- [SLOs-Serve: Optimized Serving of Multi-SLO LLMs (arXiv:2504.08784)](https://arxiv.org/abs/2504.08784)
