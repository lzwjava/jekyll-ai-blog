---
audio: false
generated: true
image: false
lang: en
layout: post
title: Xiaomi MiMo V2.5 Production Engineering Breakthrough
translated: false
type: note
---

**Question:** What does the Xiaomi MiMo V2.5 inference blog post say?

**Answer:**

Published today (May 30, 2026), this is a dense production engineering writeup from Xiaomi's MiMo team. Here's the full breakdown:

---

## TL;DR

MiMo-V2.5 uses **Hybrid Sliding Window Attention (SWA) + sparse MoE + multimodal encoders**. The post documents how they actually realized the theoretical 7× KVCache compression of Hybrid SWA in production — which didn't come for free; it required a full-stack overhaul.

---

## Architecture Baseline

- **MiMo-V2.5-Pro**: 70 layers — 10 Full Attention + 60 SWA (window=128)
- SWA layers = 6/7 of all layers → ~7× compute and KVCache reduction vs full attention
- KVCache efficiency ranks **2nd** among models surveyed (behind DeepSeek-V4-Pro and V4-Flash)

---

## 1. KVCache System Refactor (biggest section)

**Dual-Pool Design:** Full Attention and SWA KV use separate pools. SWA pool is strictly O(W), not O(N). This is where the 7× storage savings actually materializes.

**Layerwise Prefetch:** SWA's tiny KV footprint enables near-perfect overlap of H2D KVCache prefetch with compute — cache load cost approaches zero.

**SWA-Aware Prefix Cache Tree:** The classic RadixAttention assumption ("equal tokens → equal KV") breaks under SWA because SWA KV can be partially evicted mid-sequence. Their fix: add "window-safe length" matching — only count a cache hit if the tail W tokens still have valid SWA pool slots. Each tree node carries dual indices (Full Attention segment + SWA segment). Raw hit rate slightly drops but effective hit rate improves dramatically due to far more data fitting in the same memory budget.

**Distributed cache consistency fixes** across L1/L2/L3 tiers (device, host, GCache). Four specific failure modes addressed: device-complete/host-deficient, host-complete/device-deficient, L3 prefix eviction of high-frequency sequences, and medium/short sequence SWA retention.

**GCache (in-house L3 cache):** Built by Xiaomi's storage team. Key properties:
- Decentralized metadata via consistent hashing (Master only does heartbeats/discovery, not IO path)
- Memory+disk co-location on GPU machines → zero additional storage cost
- RDMA: 170 GB/s single-process read at 280μs; 350 GB/s under GDR
- Single-replica with Raft HA and proactive fault migration

**Result: 93% average server-side KVCache hit rate; 95%+ for heavy users.**

---

## 2. Scheduling (LLM-Router)

Custom stateless router using Redis for centralized state (replaces SGLang's early router which had no shared state).

**Affinity scheduling formula:**
```python
score(worker) = matchWeight × prefix_match_percentage − normalized_load
```
→ +25% L2 cache hit rate, +30% per-node input throughput

**TTFT optimization:** Priority queue sorted by uncached token count (cache-friendly requests run first) + starvation penalty. Result: **P90 TTFT reduced 30%** for long requests, no regression for short.

---

## 3. Prefill Optimizations

- **EP size halved** after SWA KVCache fix (smaller working set → fit more in memory → smaller expert parallelism needed) → **+40% end-to-end prefill performance**
- **3-tier length bucketing** (0–64K / 64K–256K / 256K–1M) to avoid DP-Attention synchronization skew from mixing short and long requests in the same EP group
- **MoE load balance** naturally good (avg factor ~0.85) — no explicit balancing needed yet
- **NUMA conflict fix**: `numa_balancing` kernel param conflicted with SGLang's NUMA config → disabled it → **+10% end-to-end perf**

---

## 4. Decode Optimizations

- SWA decode KVCache → **~5× effective capacity** increase
- PD-disaggregated KVCache preallocation moved to CPU until decode starts (eliminate GPU memory waste)
- CUDA Graph memory tuning
- **MTP (Multi-Token Prediction, 3 layers) fix:** Previously prefill didn't build MTP KVCache, so early decode tokens (0–128) had near-zero acceptance rate. Fixed with prefill MTP support + HiCache L2/L3 adaptations. Result: **0–128 tokens: 2.3× speedup; 128–256 tokens: 1.5× speedup** — huge for agentic short-output scenarios

---

## 5. Multimodal (EPD Disaggregation)

Based on SGLang v0.5.7 EPD design. **Encoder throughput doubled** (15→30 QPS) with no latency regression. Key tricks:
- Async multimodal embedding replication overlapped with prefill
- TP=1 Encoder with data parallelism (TP>1 hurts small encoders)
- Cross-request batching (batch images/audio from multiple requests into one forward)
- GPU-side image preprocessing (vs CPU bottleneck)
- Parallel video decoding: 1-hour video decode **156s → 23s**
- Consistent hashing for Encoder routing → **+30% multimodal cache hit rate**
- Shared-memory intra-node embedding cache sharing

---

## Why This Matters for You

If you're building inference infra or studying production LLM systems:

1. **Hybrid SWA is architecturally elegant but operationally hard** — the prefix cache tree semantics break in subtle ways (the "window-safe length" insight is non-obvious and important)
2. The **dual-pool KVCache + layerwise prefetch** pattern is likely to become standard
3. **MTP with prefill warmup** is a concrete trick for agentic short-output latency
4. The **NUMA balancing kernel conflict** is a gotcha worth knowing for multi-GPU deployments on Ubuntu
5. GCache's co-deployment-on-GPU-machines approach for zero-cost L3 storage is clever infra design

The paper essentially documents what it takes to ship a Hybrid SWA model at production quality — something vLLM/SGLang didn't fully support when they launched.
