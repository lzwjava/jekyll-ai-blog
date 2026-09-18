---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ternary Bonsai 27B Cost Breakdown
translated: false
type: note
---

**Question:** Estimate the full cost of training a model like Ternary Bonsai 2 27B.

**Answer:**

There are two separate cost buckets: **base model pre-training** (Alibaba's cost) and **Prism ML's ternary quantization work**. Here's a detailed breakdown of both.

---

## Part 1 — Pre-Training Qwen3.8-27B (Alibaba's Bill)

**Step 1: Estimate total FLOPs**

Using the standard formula `FLOPs ≈ 6 × N × D`:

| Scenario | Tokens (D) | FLOPs |
| --- | --- | --- |
| Chinchilla-optimal (20×N) | ~540B | ~8.7 × 10²³ |
| Moderate over-train | ~5T | ~8.1 × 10²⁴ |
| LLaMA 3-style (aggressive) | ~15T | ~2.4 × 10²⁵ |

Qwen3.8-27B likely falls in the **5–15T token range** given modern practices, so call it **~10²⁴–10²⁵ FLOPs**.

**Step 2: Convert to GPU-hours**

An H100 SXM at ~40% MFU (typical for large distributed training) delivers effectively ~800 TFLOP/s of usable throughput.

| Token budget | GPU-hours (512× H100) | Wall-clock time |
| --- | --- | --- |
| 5T tokens | ~500,000 GPU-hrs | ~40 days |
| 10T tokens | ~1,000,000 GPU-hrs | ~80 days |
| 15T tokens | ~1,500,000 GPU-hrs | ~120 days |

**Step 3: Dollar cost**

H100 cloud rental in 2026 ranges from ~$1.38/hr (cheap spot) up to $7.50+/hr (AWS on-demand), with the market average across 42 providers sitting at $3.61/hr on-demand.

| Scenario | GPU-hours | @ $2.50/hr (reserved) | @ $3.61/hr (avg) | @ $7.50/hr (AWS) |
| --- | --- | --- | --- | --- |
| 5T tokens | 500K | **$1.25M** | **$1.8M** | **$3.75M** |
| 10T tokens | 1M | **$2.5M** | **$3.6M** | **$7.5M** |
| 15T tokens | 1.5M | **$3.75M** | **$5.4M** | **$11.25M** |

**Realistic estimate for Qwen3.8-27B pre-training: ~$2M–$6M USD**, not counting overhead, failed runs, ablation experiments, and post-training (SFT, RLHF), which can easily add another 30–50%.

---

## Part 2 — Prism ML's Ternary Quantization

This is much cheaper — it's a post-training process, not a from-scratch pre-train:

| Task | Est. GPU-hours | Cost @ $3/hr |
| --- | --- | --- |
| Calibration dataset runs | ~50–200 H100-hrs | ~$150–$600 |
| Hadamard rotation fitting + PTQ passes | ~100–500 H100-hrs | ~$300–$1,500 |
| Evaluation across 14 benchmarks (EvalScope + vLLM) | ~200–1,000 H100-hrs | ~$600–$3,000 |
| Engineering iteration / ablations | ~1,000–5,000 H100-hrs | ~$3,000–$15,000 |
| **Total estimate** | | **~$5,000–$20,000** |

This is a rough order-of-magnitude estimate. Prism ML has not published their exact compute cost.

---

## Summary

| Cost Component | Who Pays | Low Estimate | High Estimate |
| --- | --- | --- | --- |
| Base pre-training (Qwen3.8-27B) | Alibaba | ~$2M | ~$10M+ |
| Post-training / RLHF / SFT | Alibaba | ~$200K | ~$1M |
| Ternary quantization (Bonsai) | Prism ML | ~$5K | ~$20K |
| **Total to reproduce from scratch** | Both | **~$2.2M** | **~$11M+** |

The key insight is that Prism ML's work is **relatively cheap** — perhaps $5K–$20K — but it stands entirely on top of Alibaba's multi-million dollar pre-training investment. This is the economic model behind almost all open-weight quantization: someone else pays for the hard part, and researchers add value through compression techniques at a tiny fraction of the original cost.

For comparison, an 8-GPU H100 server costs around $216,000 to buy outright, meaning owning enough hardware to run pre-training at meaningful scale would require tens of millions in capital expenditure alone, before power, cooling, and staffing.

---

**References:**

- [H100 Price Per Hour 2026 — Spheron](https://www.spheron.network/blog/h100-price-per-hour-2026/)
- [H100 Rental Prices Compared — IntuitionLabs](https://intuitionlabs.ai/articles/h100-rental-prices-cloud-comparison)
- [Cost to Train 70B LLM From Scratch 2026 — Spheron](https://www.spheron.network/blog/cost-to-train-70b-parameter-llm-from-scratch-2026/)
- [Chinchilla Scaling Laws — Hoffmann et al.](https://arxiv.org/abs/2203.15556)
