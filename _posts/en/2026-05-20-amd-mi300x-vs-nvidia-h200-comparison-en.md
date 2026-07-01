---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD MI300X vs NVIDIA H200 Comparison
translated: false
type: note
---

**Question:** How does AMD MI300X compare to NVIDIA H200?

**Answer:**## Specs: MI300X vs H200

| Metric | AMD MI300X | NVIDIA H200 | Winner |
| --- | --- | --- | --- |
| Architecture | CDNA 3 | Hopper | — |
| VRAM | **192 GB HBM3** | 141 GB HBM3e | **AMD** |
| Memory BW | **5.3 TB/s** | 4.8 TB/s | **AMD** |
| FP32 TFLOPS | **163** | 67 | **AMD** |
| FP16 TFLOPS | **326** | 134 (989 w/ sparsity) | AMD raw / NVIDIA real |
| INT8 TOPS | ~2,600 | **2,680** | **NVIDIA** |
| TDP | 750W | 700W | NVIDIA |
| Price (cloud) | ~$2.50/hr | ~$2.25/hr | NVIDIA |

Raw specs favor AMD on paper heavily. Reality is more nuanced.

## Real-World Benchmark Numbers

### Inference (LLM throughput)

In multi-GPU vLLM benchmarks using Llama 3.1 8B, MI300X achieves ~18,752 tokens/second on a single GPU — roughly **74% of H200's throughput**. Scaling efficiency is 95% at 2 GPUs but drops to 81% at 4 GPUs.

At lower concurrencies (under ~250 concurrent queries), H200 delivers faster per-query output speeds and lower latency. But at **high concurrency**, MI300X flips it — higher peak system throughput and lower cost per token.

### Latency

H200 consistently delivers 37–75% lower latency than MI300X across tested configurations. On DeepSeek R1, H200 hit 6,311 tokens/s offline throughput vs MI300X's 4,574 tokens/s.

### Training

SemiAnalysis's 5-month deep dive: real-world MI300X training performance on public stable AMD software lags H100/H200 significantly. **Training performance per TCO is worse on MI300X** on stable releases — but this changes with custom AMD dev builds.

Clarifai's engineers found MI300X achieves only **37–66% of H100/H200 performance** due to software overhead — but can outperform H100 on memory-bound tasks, delivering up to 40% lower latency and doubling throughput for certain models.

## The Real Story: Software is the Bottleneck

This is the core thesis. MI300X hardware is competitive or better. ROCm is the tax you pay:

```
Hardware specs:     AMD wins or ties
Real training:      AMD ~65-75% of H200 (stable ROCm)
Real inference:     AMD ~74% throughput, 37-75% worse latency
Memory-bound tasks: AMD sometimes WINS (192GB is huge)
Cost per token:     AMD wins at high concurrency
```

Getting MI300X training performance within 75% of H100/H200 required significant effort from SemiAnalysis — including custom Dockerfiles built from source with direct AMD engineering support.

## Where MI300X Actually Wins

1. **192GB VRAM** — fit 70B models in BF16 on a single card. H200 can't do this (141GB).
2. **High-concurrency inference** — at large batch sizes, MI300X flips the cost equation
3. **Memory-bound workloads** — long context windows, large KV caches
4. **Availability** — H200s are scarce; MI300X stock actually exists (as you found)
5. **Cost** — cheaper per hour, and AMD Developer Cloud via DigitalOcean is accessible

## AMD's Trajectory (Important for Decision-Making)

The MI325X (available Q4 2024) upgrades to 256GB HBM3e + 6TB/s bandwidth. The MI350X/MI355X (CDNA 4, TSMC 3nm, shipping 2025) delivers ~4,600 TOPS FP8 — roughly **1.8× MI300X** in FP8 throughput, with near-parity to B200 on some FP8 training benchmarks.

ROCm is also improving fast. On Llama-2 70B LoRA FP8, MI355X slashed training time from ~28 minutes (MI300X) to just over 10 minutes — a 2.8× speedup, with results within ~10% of B200/GB200 submissions.

## Decision Matrix for You

| Use Case | Pick |
| --- | --- |
| LoRA fine-tuning (HF stack) | MI300X ✅ (works, cheaper) |
| nanoGPT-scale training | MI300X ✅ (PyTorch ROCm is fine) |
| Custom CUDA kernels | H200 (don't touch ROCm) |
| 70B model inference | **MI300X wins** (192GB fits it) |
| Low-latency serving | H200 |
| High-throughput batch inference | MI300X at scale |
| Availability right now | **MI300X wins** |

## Bottom Line

The "70%" figure from before still roughly holds for inference throughput vs H200 specifically (~74%). For training it can be worse (37–66%) or close to parity depending on ROCm version and workload. The 192GB VRAM advantage is real and matters for large model work. For your use case — LoRA fine-tuning, agent tooling, model training at nanoGPT scale — **MI300X via AMD Developer Cloud is a solid pragmatic choice**, especially given H200 scarcity.

**References:**

- [AMD MI300X vs NVIDIA H200 — Spheron Blog](https://www.spheron.network/blog/amd-mi300x-vs-nvidia-h200/)
- [MI300X vs H100 vs H200 Benchmark: Training — SemiAnalysis](https://newsletter.semianalysis.com/p/mi300x-vs-h100-vs-h200-benchmark-part-1-training)
- [Multi-GPU Benchmark: B200 vs H200 vs H100 vs MI300X — AIMultiple](https://research.aimultiple.com/multi-gpu/)
- [Independent GPU Performance Analysis — Artificial Analysis](https://artificialanalysis.ai/articles/independent-analysis-of-leading-gpus-amd-nvidia)
- [MI300X vs B200 — Clarifai](https://www.clarifai.com/blog/mi300x-vs-b200)
