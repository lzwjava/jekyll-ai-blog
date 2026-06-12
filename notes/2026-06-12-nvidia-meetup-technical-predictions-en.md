---
audio: false
generated: true
image: false
lang: en
layout: post
title: NVIDIA Meetup Technical Predictions
translated: false
type: note
---

**Question:** Based on the agenda of the NVIDIA Accelerated Computing Developer Meetup (Shenzhen, June 13, 2026, co-hosted with Google Cloud and Tencent), predict what each session will actually cover technically.

**Answer:**

Here's my session-by-session prediction, grounded in what's publicly known about each topic as of June 2026.

## 1. NVIDIA × Tencent: Hy3 Preview inference optimization

Context first: Hy3 preview launched April 23, 2026 — a fast/slow-thinking hybrid MoE with 295B total params, 21B activated, 256K max context. The headline they'll repeat: 40% overall inference efficiency gain from deep model-framework co-design, covering the full inference stack, kernel performance, and quantization algorithms.

Expect the talk to decompose that 40% into:

- **MoE-specific serving on Hopper/Blackwell**: expert-parallel (EP) layout, grouped GEMM for expert FFNs, all-to-all dispatch/combine optimization, probably TensorRT-LLM and/or SGLang integration (Hy3 officially supports vLLM and SGLang)
- **Quantization**: FP8 weights/KV-cache, possibly NVFP4 on Blackwell, and how they kept the fast/slow-thinking router accurate post-quantization
- **PD disaggregation + MTP (multi-token prediction) speculative decoding** — standard 2026 playbook for MoE serving
- **Production numbers**: 54% lower first-token latency, 47% lower end-to-end latency on CodeBuddy/WorkBuddy, driving agent workflows up to 495 steps — they'll show how kernel-level wins translate to agent-product wins, and likely the economics (¥1.2/M input tokens)

## 2. AI Coding with Google Cloud + Next 26 recap

Two sessions, same source material. Next '26 (April, Las Vegas) had 260+ announcements centered on the "agentic era": Gemini Enterprise Agent Platform and 8th-gen TPUs. The coding-focused content will almost certainly be:

- **Antigravity** as the AI coding star: Google is unifying its dev tools into a single multi-agent platform called Antigravity (with Antigravity CLI), with Gemini Code Assist and Gemini CLI sunsetting for individual tiers on June 18, 2026 — note that's 5 days after this meetup, so expect a heavy "migrate now" push. Antigravity 2.0 is a standalone desktop app for orchestrating agents, powered by Gemini 3.5 Flash.
- Live demo: spec → multi-agent plan → parallel code agents → review, plus MCP integration (BYO-MCP lets you connect Gemini Enterprise to custom tools)
- The Next 26 recap will cherry-pick: Gemini 3.1 Pro access, Agent Platform as end-to-end agent workspace, and notably Claude Opus 4.7 being added for open model choice, plus 8th-gen TPUs (dual-chip design for training vs inference) and Virgo Network, the new megascale data center fabric

## 3. SM120 inference optimization with AI agents in the workflow

SM120 = compute capability 12.0 = consumer/workstation Blackwell (RTX 5090, RTX PRO 6000/4000). This is the most relevant session for your RTX 4070 → Blackwell trajectory. The pain points are well-documented and will likely structure the talk:

- Native NVFP4 CUTLASS paths have been broken on SM120 — TMA warp-specialized grouped GEMM kernels failed at runtime, forcing fallback to Marlin W4A16 which dequantizes FP4 to FP16; community patches to FlashInfer's SM120 capability checks achieved the first correct native FP4 MoE output on desktop Blackwell. Expect NVIDIA to present official CUTLASS/FlashInfer fixes and tuned tile configs.
- FlashInfer is the primary kernel library for SGLang on SM120, with JIT-compiled SM120 kernels and dedicated MLA variants — likely a walkthrough of attention backend selection
- The "AI agents in the workflow" angle: using coding agents to do the optimization loop itself — profile with nsys/ncu, have an agent propose kernel tile configs, benchmark, iterate. This matches the 2026 trend of agent-driven kernel autotuning. Real-world numbers like 6.5x throughput gains on RTX PRO 4000 from config fixes alone (36 → 234 tok/s) show why this matters.

## 4. SGLang Context Parallel (CP) design and implementation

Probably the deepest technical talk. CP shards the *sequence dimension* across GPUs (vs TP sharding hidden/head dims), attacking two problems: O(N²) prefill attention and KV cache exceeding single-GPU HBM. Expect:

- **Prefill CP with zigzag ring attention**: long-context prefill (256K+) exhausts HBM via KV cache and bottlenecks TTFT on O(N²) attention; zigzag CP assigns each rank head + tail chunks so causal-attention load balances, and in PD-disaggregated deployments each rank transfers only 1/CP of the KV to the decode node, in parallel, with no gather step

The zigzag trick in ~10 lines — why head+tail chunks balance causal attention:

```python
# Naive split: rank 0 gets tokens [0:N/4], rank 3 gets [3N/4:N]
# → rank 3 attends to ~4x more keys than rank 0 (causal mask). Imbalanced.
# Zigzag: rank i gets chunk i AND chunk (2*CP - 1 - i)
def zigzag_shard(tokens, cp_size):
    chunks = split(tokens, 2 * cp_size)
    return [concat(chunks[i], chunks[2*cp_size - 1 - i]) for i in range(cp_size)]
# rank 0: chunks (0, 7), rank 3: chunks (3, 4) → every rank sees
# ~equal causal attention FLOPs. Ring-pass KV blocks between ranks.
```

- **Decode CP**: partitioning the context during decode across devices to avoid KV cache redundancy (with TP alone, each rank holds a full KV copy), inspired by the Helix Parallelism paper, with ring attention or reduce-scatter/all-gather communication and a context_parallel_size topology in the scheduler
- **Composability**: how CP stacks with TP/PP/EP — DeepSeek V3.2 already runs CP8+PP2+TP8 configs in SGLang, and they'll position CP against the recent PP work (chunked pipeline parallelism with async P2P hit 3.31× prefill throughput at PP4 TP8 vs TP8 on DeepSeek-V3.1, with 67.9% TTFT reduction) — expect a "when CP vs PP vs both" decision framework, plus DSA/sparse-attention interaction for DeepSeek-style models

## Meta-prediction

The connecting thread across all four talks: **agentic inference economics**. Agent workflows (495-step Hy3 runs, Antigravity multi-agent orchestration) generate long contexts and massive KV pressure — which is exactly what CP, SM120 kernel work, and MoE co-design solve. If you attend, the SGLang CP talk is the one to take notes on; it's directly upstream of your DeepSeek v4 MoE exploration, and the zigzag/ring-attention design maps cleanly onto what you'd implement in a nanoGPT-scale training CP too.

**References:**

- [腾讯混元Hy3 preview发布 — Tencent](https://www.tencent.com/zh-cn/articles/2202320.html)
- [实测混元Hy3 preview — 钛媒体](https://www.tmtpost.com/7964254.html)
- [Pipeline Parallelism in SGLang — LMSYS Blog](https://www.lmsys.org/blog/2026-01-15-chunked-pipeline/)
- [Prefill CP with Zigzag Ring Attention — sglang#22223](https://github.com/sgl-project/sglang/issues/22223)
- [Decode Context Parallel proposal — sglang#12196](https://github.com/sgl-project/sglang/issues/12196)
- [NVFP4 MoE on SM120 debug report — cutlass#3096](https://github.com/NVIDIA/cutlass/issues/3096)
- [Google Cloud Next 26 wrap-up](https://cloud.google.com/blog/topics/google-cloud-next/google-cloud-next-2026-wrap-up)
- [Gemini for Google Cloud release notes (Antigravity migration)](https://docs.cloud.google.com/gemini/docs/release-notes)
