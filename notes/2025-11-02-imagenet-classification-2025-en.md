---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: ImageNet Classification Advances in 2025
translated: false
type: note
---

The State-of-the-Art (SOTA) on ImageNet (specifically the ImageNet-1K validation set for image classification) has continued to advance steadily since the dramatic improvements post-2012. As of November 2025, the leading models achieve top-1 accuracies around 91%, corresponding to a top-1 error rate of ~9%. Top-5 accuracies are even higher, typically exceeding 99%, for a top-5 error rate below 1%.

### Key SOTA Models (Top-5 from Papers With Code Leaderboard)

Here's a snapshot of the current top performers (fine-tuned on ImageNet-1K), based on top-1 accuracy. Top-5 accuracies aren't always explicitly re-reported for these very high-performing models (as they saturate near-perfect levels), but cross-referencing with similar recent architectures suggests top-5 errors under 1% for all:

| Rank | Model | Top-1 Accuracy | Est. Top-5 Accuracy | Parameters | Notes |
| ------ | -------- | ---------------- | --------------------- | ------------ | ------- |
| 1 | CoCa (finetuned) | 91.0% (9.0% error) | ~99.5% (<0.5% error) | 2.1B | Multimodal image-text model; excels in zero-shot (86.3% top-1) and frozen-encoder settings (90.6% top-1). |
| 2 | Model Soups (BASIC-L) | 90.98% (9.02% error) | ~99.4% (<0.6% error) | ~1B | Ensemble averaging of fine-tuned models for improved robustness. |
| 3 | Model Soups (ViT-G/14) | 90.94% (9.06% error) | ~99.4% (<0.6% error) | 1.8B | ViT-based; strong generalization to out-of-distribution data. |
| 4 | DaViT-Giant | 90.4% (9.6% error) | ~99.3% (<0.7% error) | 1.4B | Dual-attention ViT; trained on 1.5B image-text pairs. |
| 5 | ConvNeXt V2-Huge | 88.9% (11.1% error) | ~99.0% (~1.0% error) | 660M | CNN revival with masked autoencoder pretraining; efficient for edge devices. |

### Clarification on the "<3% Today"

- This refers to the **top-5 error rate**, not top-1. Pre-2012 baselines (e.g., SVMs) hovered around 25% top-5 error. By 2017 (SENet), it dropped to ~2.3%. Modern SOTA models have pushed it below 1%, making top-5 predictions essentially reliable for most real-world use cases.
- Top-1 error remains higher (~9%) because it demands the *exact* top prediction match, which is stricter and more sensitive to edge cases like ambiguous images.

Progress has slowed in recent years due to dataset saturation—gains now come from massive pretraining (e.g., on ImageNet-21K or web-scale data) and techniques like model ensembling or distillation. Human expert performance is estimated at ~5% top-1 error (or 2-12% top-5, varying by study), so AI has surpassed humans on this benchmark.

[ImageNet Benchmark (Papers With Code)](https://paperswithcode.com/sota/image-classification-on-imagenet)
[Image Classification: State-of-the-Art Models in 2025 (HiringNet)](https://hiringnet.com/image-classification-state-of-the-art-models-in-2025)
[CoCa: Contrastive Captioners are Image-Text Foundation Models (arXiv)](https://arxiv.org/abs/2205.01917)
