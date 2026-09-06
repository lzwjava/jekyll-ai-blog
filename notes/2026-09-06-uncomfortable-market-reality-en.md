---
audio: false
generated: true
image: false
lang: en
layout: post
title: Uncomfortable Market Reality
translated: false
type: note
---

Honest take, grounded in what I've seen in the code and the broader industry landscape:

## The uncomfortable market reality

**The core premise is being undercut fast.** BloomBee's thesis is "inference is expensive, idle GPUs are abundant, P2P can bridge them." But the industry has moved in the opposite direction:

- **Centralized inference got absurdly cheap.** Aggressive batching (vLLM, SGLang, TensorRT-LLM), Groq/Cerebras LPUs, and DeepSeek-style pricing have pushed frontier-model tokens to near-zero cost. When a 405B token costs fractions of a cent on a datacenter API, the economic case for stitching together consumer GPUs over the internet is very hard.
- **Co-located GPUs beat networked GPUs, always.** A single A100 node with 80GB–192GB of VRAM holds most useful models (up to ~70B at FP16, larger quantized). The models that *don't* fit (405B, MoE giants) are exactly the ones whose per-layer activations are huge — the worst case for network-hop-heavy inference.

## Fundamental technical headwinds

1. **Autoregressive decoding is latency-bound, and the speed of light doesn't negotiate.** Every token must traverse the whole chain of peers. Even with lossless compression and spec decoding, you're serializing ~40–80 layer round-trips over consumer internet with 10–50ms RTT each. The README itself admits: *"Latency increases with the number of network hops."* Microbatch pipelining helps throughput but not single-stream latency — and chat users care about latency.

2. **Heterogeneity and churn.** Volunteer peers join/leave constantly. Routing, retries, and cache invalidation across unstable nodes add complexity that a homogenous datacenter simply doesn't have. The `speculative_pruner` machinery is clever, but it's optimizing a system that's still orders of magnitude off from centralized performance.

3. **Petals-shaped shadow.** This is essentially Petals lineage, and Petals — with more resources and attention — never escaped the research-hobbyist niche. That's a strong prior against the category, not against this specific implementation.

## Where it *does* have real value

- **Research.** The genuinely transferable contributions here — **branch pruning for speculative decoding** (drafting cost scales with tree size; pruning it is valuable everywhere, including datacenters), lossless activation compression, and cross-stage overlap attribution — would improve *centralized* pipelined inference too. That's arguably the project's best export.
- **Censorship-resistance / no-single-operator scenarios.** If "nobody can shut it down" matters more than latency, P2P is the only option.
- **Genuinely stranded compute.** Regional GPU gluts (e.g., gaming rigs in countries without cheap cloud access) are real — just niche.
- **Latency-tolerant workloads.** Batch offline processing, synthetic data generation, background evals — where tokens/hour matters more than time-to-first-token.

## Verdict

- **As a business / industry infrastructure: not promising.** You're competing against falling token prices, and physics is against you on latency. I'd bet against decentralized LLM inference achieving meaningful commercial adoption.
- **As a research project: solid and worthwhile.** It attacks real problems (bandwidth-bound pipelining, spec-decode tree cost) with concrete engineering, and several of its techniques will outlive the decentralized framing.
- **Strategic suggestion:** the highest-EV pivot is to treat the decentralized part as a *research vehicle* and publish the communication-optimization results — the pruner and compression work could matter to vLLM-class systems, where the actual money is.

If you're deciding whether to invest time here: contribute to the spec-decoding and compression pieces (portable ideas), don't bet on the P2P deployment story.
