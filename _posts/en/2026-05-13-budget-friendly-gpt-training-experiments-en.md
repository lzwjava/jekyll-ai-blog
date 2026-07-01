---
audio: false
generated: true
image: false
lang: en
layout: post
title: Budget-Friendly GPT Training Experiments
translated: false
type: note
---

**Question:** With a budget of 5,000 CNY (~$735 USD), using RunPod or DigitalOcean, how far can we get with nanoGPT training?

---

**Answer:**

## What Is nanoGPT?

nanoGPT is Andrej Karpathy's lightweight, educational implementation of GPT — the simplest, cleanest codebase for training or fine-tuning GPT-style models. It is **not** the same scale as GPT-3. It ranges from a tiny Shakespeare character-level model (~10M parameters) to a GPT-2 replica (~124M parameters). This is actually the right tool for your budget.

---

## GPU Pricing Reference (RunPod vs DigitalOcean)

RunPod's community cloud offers popular GPU configurations including the RTX 4090 at approximately **$0.39/hour**, the A100 80GB at **$1.89/hour**, and the H100 80GB at **$2.99/hour**.

DigitalOcean's GPU droplets are more expensive and less flexible for ML workloads — RunPod is the far better choice for nanoGPT training on a tight budget.

---

## What Can You Train With $735?

Here is a practical breakdown of the three levels of nanoGPT experiments, calculated against RunPod's RTX 4090 at ~$0.39/hr:

### Level 1 — Baby Shakespeare Model (Character-level, ~10M params)

**Cost: < $0.05 | Time: ~3–5 minutes**

The fastest way to get started is training a character-level GPT on the works of Shakespeare. On one A100 GPU this training run takes about **3 minutes** and achieves a best validation loss of 1.4697. On an RTX 4090 this is similarly fast, costing essentially nothing. You get a model that generates semi-coherent Shakespearean text.

This is free to run dozens of times. Great for learning and experimentation.

---

### Level 2 — GPT-2 Small (124M params) on OpenWebText / FineWeb

**Cost: ~$3–$5 per full run | Time: ~2–8 hours on 1x RTX 4090**

A community experiment showed single-GPU, from-scratch GPT-2-style training to a validation loss of 3.286 in about **115 minutes** on a single RTX 4090.

A baseline run on 2x RTX 4090 takes about **8.13 hours**, meaning a single 4090 run would take roughly 15–16 hours for the full default nanoGPT GPT-2 training.

At $0.39/hr × 16 hours = **~$6.24 per full run**. With your $735 budget, you could run this experiment over **100 times** — enough for serious hyperparameter tuning and research.

---

### Level 3 — GPT-2 Medium/Large (350M–774M params)

**Cost: ~$30–$80 per run | Time: several days on 1x RTX 4090**

For the full default nanoGPT config with 600,000 iterations on a single RTX 4090, total training time would be roughly **35 days**, compared to ~4 days using 8x A100 GPUs with distributed training.

At $0.39/hr × 35 days = **~$327 per run**. With $735 you could do about 2 full runs — possible but risky (spot instance interruptions, no safety margin).

---

## Budget Allocation Plan (~$735 total)

| Phase | Activity | Est. Cost |
| --- | --- | --- |
| Experiments | 50+ Shakespeare char-level runs | ~$5 |
| Core work | 80–100 GPT-2 124M runs (tuning) | ~$500 |
| Stretch | 1 GPT-2 Medium (350M) run | ~$100 |
| Buffer | Debugging, storage, data transfer | ~$130 |

---

## Key Practical Tips

**Use RunPod, not DigitalOcean.** RunPod's community cloud is purpose-built for ML workloads. DigitalOcean GPU droplets are pricier and less optimized for training jobs.

**Use spot/community instances.** RTX 4090 spot pricing ranges from as low as **$0.07/hr** on some providers, which could stretch your budget dramatically further — though spot instances can be interrupted.

**Use `torch.compile`.** With modern optimizations like FlexAttention and `torch.compile`, a GPT-2 124M model can be trained in about **115 minutes** on a single RTX 4090 — much faster than unoptimized defaults.

**Save checkpoints frequently** to avoid losing progress on long runs.

---

## Summary

With 5,000 CNY (~$735) and RunPod, you can realistically:

- ✅ Run the Shakespeare baby model **hundreds of times** (nearly free)
- ✅ Train GPT-2 124M from scratch **80–100 times** with room for serious experimentation
- ✅ Attempt a GPT-2 Medium (350M) run **1–2 times** as a stretch goal
- ❌ You cannot train anything near GPT-3 scale (175B parameters)

This is actually a **solid and meaningful** research budget for nanoGPT. You can learn a tremendous amount, tune hyperparameters, and produce a working custom language model.

---

**References:**

- [nanoGPT GitHub (Andrej Karpathy)](https://github.com/karpathy/nanoGPT)
- [nanoGPT Training Time on 1x 4090 — GitHub Issue #179](https://github.com/karpathy/nanoGPT/issues/179)
- [GPT-2 124M in 115 min on RTX 4090 — HuggingFace](https://huggingface.co/DevParker/NanoGPT-124m-In-A-Cave-With-A-Box-Of-Scraps/blob/main/README.md)
- [NanoGPT Speedrun on 2x RTX 4090 — Tyler Romero](https://www.tylerromero.com/posts/nanogpt-speedrun-worklog/)
- [RunPod Pricing Guide — Hivenet](https://compute.hivenet.com/post/runpod-pricing-complete-guide-to-gpu-cloud-costs)
- [RTX 4090 Cloud Pricing 2026 — GetDeploying](https://getdeploying.com/gpus/nvidia-rtx-4090)
