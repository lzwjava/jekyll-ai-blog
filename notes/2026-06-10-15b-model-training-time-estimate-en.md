---
audio: false
generated: true
image: false
lang: en
layout: post
title: 1.5B Model Training Time Estimate
translated: false
type: note
---

Question: For training a 1.5B model on nanochat, how many tokens should we prepare and how much time will it take?

Answer:

Training a 1.5B parameter model requires planning both **total token budget** and **wall-clock time**, depending on your goals (research-quality vs production-quality). Here’s a structured estimate:

---

## 1. Token budget

A good rule of thumb for transformer LLMs:

* **Small research runs:** 50–100× model parameters in tokens
* **Medium/final-quality runs:** 200–300× model parameters in tokens
* **High-quality/foundation-scale:** 500×+ model parameters in tokens

### Calculation for 1.5B:

* Model params: 1.5B ≈ 1.5×10⁹
* Medium-quality target (200×):
  ( 1.5 × 10^9 × 200 = 3 × 10^{11} ) tokens → **300B tokens**
* Lower research target (100×): 150B tokens
* Aggressive large run (300×): 450B tokens

**Recommendation for MI300X:** start with **200–250B tokens**; enough to see meaningful training without overcommitting.

---

## 2. Training time estimation

Use your current MI300X throughput as reference:

* Your 760M model: ~101.5k tok/sec

* Step scaling roughly linear with model size in FLOPs:

  | Model | Estimated tok/sec |
  | ----- | ----------------- |
  | 760M  | 101.5k            |
  | 1.5B  | ~50–60k           |

* Token throughput is halved because compute roughly doubles.

### Wall-clock time:

* **Target:** 200B tokens
* Throughput: 55k tok/sec → 198M tok/hour ≈ 0.198B tok/hour
* Time ≈ ( 200 / 0.198 ) ≈ 1010 hours ≈ **42 days** (single MI300X, continuous)

> Note: gradient accumulation, eval steps, logging, and pauses can add 10–20% overhead. Realistic total: **~45–50 days**.

* **Smaller exploratory run:** 50B tokens → ~11 days

---

## 3. Practical adjustments

* **Sequence length:** 2048 is fine; 4096 doubles memory and halves batch, slowing throughput.
* **Batch size:** keep max that fits memory; larger batch improves MFU.
* **FP8 + FA2:** keep enabled for best throughput.
* **Checkpointing:** frequent saves recommended (every 5–10B tokens) to avoid losing long runs.

---

## 4. Summary Table

| Model | Target Tokens | Estimated Tok/sec | Time (hours) | Notes            |
| ----- | ------------- | ----------------- | ------------ | ---------------- |
| 1.5B  | 50B           | 55k               | 250          | exploratory      |
| 1.5B  | 200B          | 55k               | 1010 (~42d)  | research-quality |
| 1.5B  | 300B          | 55k               | 1515 (~63d)  | higher quality   |

> Real throughput will fluctuate depending on exact batch/seq/config.

---

If you want, I can draft a **ready-to-run nanochat config for 1.5B** optimized for MI300X, including batch, grad accumulation, sequence length, and checkpoint schedule to finish 200B tokens efficiently.
