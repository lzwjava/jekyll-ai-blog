---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Optimizing Multi-SLO LLM Serving
translated: false
type: note
---

### Overview
The paper "SLOs-Serve: Optimized Serving of Multi-SLO LLMs" introduces SLOs-Serve, a system designed to efficiently serve large language models (LLMs) in multi-stage applications where each stage (e.g., prefill for input processing, decode for token generation) and application (e.g., chatbots, coding assistants) has specific service level objectives (SLOs). These SLOs ensure low latency for user-facing aspects, like time-to-first-token (TTFT) for prefill and tokens-per-output-time (TPOT) for decode. Traditional serving systems like vLLM or Sarathi-Serve prioritize throughput but often violate these fine-grained SLOs under shared resources, especially during bursts or mixed workloads.

### Key Challenges and Contributions
The authors identify challenges in multi-SLO serving:
- **Multi-stage requests**: Applications like reasoning LLMs (tight SLOs during "thinking" stages) or tool-calling agents (loops with tight prefill/decode) require stage-specific guarantees.
- **Resource contention**: Shared GPUs lead to SLO violations in co-located or disaggregated setups.
- **Bursty traffic**: Sudden spikes overwhelm schedulers.

SLOs-Serve's contributions include:
- A dynamic programming (DP)-based scheduler that optimizes token allocations (prefill budget, batch sizes) to meet SLOs while maximizing throughput.
- Support for chunked prefill, SLO-adaptive speculative decoding (customizing speculation lengths per SLO tier), and soft admission control (guaranteeing SLOs for admitted requests, deferring others).
- A distributed architecture with multi-replica routing and burst resilience, built on vLLM for batching and Ray for orchestration.

| Application | Prefill SLO | Decode SLO | Example |
|-------------|-------------|------------|---------|
| Summarization | Tight (e.g., 3x slowdown max) | Loose (100ms TPOT) | Document processing |
| Coding | Loose | Tight (50ms TPOT) | Code generation |
| Chatbot | Loose | Loose | Interactive queries |
| Tool-calling | Tight (loops) | Tight (loops), loose (final) | Agentic workflows |
| Reasoning | Tight (thinking) | Tight (thinking), loose (response) | Chain-of-thought |

### System Design
- **Scheduler (Algorithm 1)**: Uses DP to admit requests and plan batches, modeling execution time via a Roofline-inspired predictor (R² > 0.8 accuracy). States track memory, prefill budget, and accepted requests; transitions prioritize early deadlines and SLO attainment.
- **Batch Formation**: Dynamic sizing (up to 512+ tokens) based on tightest TPOT, enabling larger batches for higher throughput without SLO violations.
- **Speculative Decoding**: Adapts speculation lengths (e.g., 1-10 tokens) per SLO tier to boost prefill budget, solving via enumeration for optimal prefill/decode balance.
- **Multi-Replica & Bursts**: Centralized controller routes requests proactively; unattainable requests go to a best-effort queue, preempted if needed.

The design explores trade-offs, like larger batches increasing throughput but risking latency (visualized in figures showing SLO-feasible regions).

### Evaluation
Tested on 6 scenarios (chatbot, coding, summarization, mixed, tool-calling, reasoning) using real traces (Azure LLM workloads) and datasets (ShareGPT, HumanEval, etc.). Models: OPT-7B/13B/30B, ToolLlama-7B. Hardware: 4×A100 GPUs (main), up to 8×H100.

- **Capacity Gains**: 2.2× average improvement over vLLM/Sarathi-Serve/DistServe (geo-mean across scenarios). E.g., 2.4× in reasoning, 2.1× in bursty coding.
- **Scaling**: Super-linear with replicas (up to 6.2× in tool-calling under bursts) via routing.
- **Ablations**: Speculation adds 1.66×, routing 1.19×, burst handling 1.34×.
- Overhead: <10ms per schedule invocation.

Figures show SLOs-Serve maintains p99 latencies near targets during spikes, while baselines degrade.

### Conclusions
SLOs-Serve advances LLM serving by guaranteeing multi-SLOs in diverse, bursty environments, unlocking 2x+ efficiency gains. Future work could extend to unknown decode lengths or more stages. The system demonstrates that SLO-customized scheduling is key for production-grade LLM deployments.

[SLOs-Serve: Optimized Serving of Multi-SLO LLMs](https://arxiv.org/abs/2504.08784)
