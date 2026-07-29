---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash-Attention Benchmarks Results
translated: false
type: note
---

Here are the full benchmark results with flash-attention:

---

## ⚡ Flash-Attention Benchmarks (Qwen3-0.6B, RTX 4070)

| Workload | Throughput |
|----------|-----------|
| **Prefill** — 8 seqs × 1024 tok | **19,548 tok/s** |
| **Decode** — 8 seqs × 512 tok | **1,389 tok/s** |
| **Decode** — 16 seqs × 256 tok | **2,307 tok/s** |
| **Mixed** — 16 seqs (variable) | **1,660 tok/s** |
| **2 seqs × 256 tok** (apples-to-apples) | **357 tok/s** |
| **64 seqs × 512 tok** (max throughput) | **646 tok/s** |

### vs. Before (PyTorch SDPA)

| Metric | Before (SDPA) | Now (FlashAttn) | Speedup |
|--------|---------------|-----------------|---------|
| Prefill | 506 tok/s | **19,548 tok/s** | **~38×** |
| Decode (2 seqs) | ~4–30 tok/s | **357 tok/s** | **~12–89×** |

Flash-attention eliminates the per-sequence causal mask loop and `transpose` overhead, using fused kernels that are dramatically faster — especially for prefill where large matmuls benefit most from the memory-efficient flash algorithm.