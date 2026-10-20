---
audio: false
generated: true
image: false
lang: en
layout: post
title: Unpopular Truths About vLLM and SGLang
translated: false
type: note
---

**Question:** What are the unpopular/honest truths about vLLM and SGLang?

**Answer:**

Here's an honest, community-sourced breakdown of the uncomfortable realities about both frameworks.

---

## ⚔️ The Benchmark War Is Mostly Theater

Both teams have publicly fought over benchmark numbers — vLLM published impressive results claiming advantage over SGLang, SGLang replied "very aggressively" with completely different numbers, then vLLM answered again with yet another update. The conclusion from neutral observers: the performance gap isn't meaningful enough to matter, especially for longer sequences.

vLLM and SGLang have leapfrogged each other for two years — whichever leads this month tends to trade places by the next minor release. A benchmark is only usable when it's version-matched, flag-matched, and run against your actual request distribution.

Headline numbers are inherently misleading: the famous ~29% SGLang throughput advantage on 8B-class models compresses sharply as model size and concurrency change — at 70B scale, it narrows to single digits.

---

## 🔴 vLLM's Unpopular Truths

**1. Kubernetes autoscaling is fundamentally broken by default**

CPU utilization on a vLLM pod stays low even at maximum throughput — the work is on the GPU, and GPU memory stays constant because vLLM pre-allocates it for the KV cache. The two metrics Kubernetes uses to make scaling decisions are both flat regardless of load. A vLLM deployment under heavy traffic looks idle to the Kubernetes scheduler while requests queue up inside the engine and latency degrades.

**2. PagedAttention doesn't solve everything**

After hours of continuous requests, memory fragmentation can cause OOM errors even when theoretical memory should be sufficient. The fix is usually restarting the server — not ideal for production. A single 128K context request can destabilize a server handling shorter requests.

**3. Multiple high-severity security CVEs**

At least six high-severity CVEs since 2025 enable remote code execution, SSRF, and DoS through the public API, including CVE-2025–30165 (CVSS 8.0) enabling RCE via unsafe pickle deserialization in vLLM's multi-node ZeroMQ communication.

**4. Production builds ship bugs**

All big cloud inference providers use custom versions of either vLLM or SGLang with their own bugfixes added, since out of the box there are bugs.

**5. Hardware support is narrower than marketed**

Native Windows support only landed in 2026 and requires CUDA 13.0 and an RTX 6000 Ada or newer. For consumer hardware with 8–12 GB VRAM, vLLM's native quantization targets server GPUs — its edge only shows up at concurrency you're unlikely to reach alone.

---

## 🔴 SGLang's Unpopular Truths

**1. RadixAttention is only magic when prefixes are shared**

Without high prefix-cache hit rates, SGLang is roughly a slower vLLM with extra knobs. Workloads with highly diverse and non-overlapping prompts — where the prefix cache hit rate drops below ~20% — see RadixAttention add overhead with no benefit.

In one controlled benchmark at 64 concurrent unique-prompt requests, vLLM's median time-to-first-token was 849ms vs. SGLang's 3,045ms — more than three times slower to first token when prefix reuse doesn't apply.

**2. SGLang uses more VRAM, not less**

SGLang's KV cache grows dynamically as the prefix tree expands — budget ~15% more VRAM than an equivalent vLLM deployment.

**3. One model per instance — no multi-tenancy**

Running several models means paying for separate SGLang instances and their own slices of GPU memory. There's no lightweight or stripped-down mode for simpler deployments.

**4. Hardware coverage trails vLLM**

ROCm (AMD) support is only partial, Apple Silicon is absent, and as of mid-2026 it remains CUDA-only in most configurations. vLLM supports over 200 model architectures plus TPU, Trainium, and Gaudi; SGLang's list is narrower.

---

## 🔴 Shared Problem: They Change Your Model's Outputs

This one is rarely discussed:

Holding model weights, decoding parameters, and hardware constant, the choice of inference backend alone can induce substantial variation in benchmark outcomes, shifting reported performance by up to **16 percentage points**. This creates a dangerous "deployment gap" between research validation and production reality, where backend-induced discrepancies can undermine not only performance claims but also safety guarantees.

---

## 🟡 Bottom Line

The honest answer is that neither wins outright. SGLang's RadixAttention lead is real on shared-prefix traffic (RAG, agents, chat history) and shrinks toward zero when every prompt is unique. Under real saturation load, vLLM has measured faster time-to-first-token on unique-prompt traffic. Run both against your **actual production workload** before committing.

---

**References:**

- [10 Best vLLM Alternatives for Production 2026](https://www.premai.io/blog/10-best-vllm-alternatives-for-llm-inference-in-production-2026/)
- [vLLM in Production: Security Hardening Guide](https://medium.com/@michael.hannecke/vllm-in-production-a-security-hardening-guide-for-enterprise-deployments-56a9c2c213dd)
- [The Silent Hyperparameter — Inference Backend Reproducibility](https://arxiv.org/pdf/2605.19537)
- [vLLM vs SGLang: What Published Data Actually Shows](https://markaicode.com/benchmarks/sglang-production-benchmark-latency/)
- [SGLang vs vLLM Fighting Over Meaningless Numbers (The Weekly Kaitchup)](https://kaitchup.substack.com/p/the-weekly-kaitchup-89)
- [vLLM vs Ollama vs SGLang vs TensorRT-LLM](https://theaiengineer.substack.com/p/vllm-vs-ollama-vs-sglang-vs-tensorrt)
- [vLLM Kubernetes: 7 Proven Production Patterns](https://thegoodshell.com/vllm-kubernetes/)
- [What Is SGLang? 2026 Guide](https://www.digitalocean.com/resources/articles/what-is-sglang)
