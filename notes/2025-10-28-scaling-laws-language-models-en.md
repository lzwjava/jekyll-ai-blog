---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Scaling Laws for Neural Language Models
translated: false
type: note
---

### Overview

The 2020 paper "Scaling Laws for Neural Language Models" by Jared Kaplan and colleagues at OpenAI (including Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Mann, Prafulla Dhariwal, Andrew Radford, and Ilya Sutskever) explores how the performance of large neural language models—measured by cross-entropy loss—scales with key training resources. Through extensive experiments on transformer-based models, they uncover predictable power-law relationships that hold across huge ranges of model sizes, datasets, and compute budgets (spanning over seven orders of magnitude). These "scaling laws" provide a framework for optimizing training efficiency and predicting performance without trial-and-error.

### Key Findings on Scaling Laws

The core insight is that loss \\( L \\) decreases as a power law with respect to three variables:

- **Model Size (\\( N \\), number of parameters)**: \\( L(N) \propto N^{-\alpha} \\), where \\( \alpha \approx 0.076 \\) (for language modeling). Larger models learn faster initially but train more slowly overall.
- **Dataset Size (\\( D \\), number of tokens)**: \\( L(D) \propto D^{-\beta} \\), with \\( \beta \approx 0.103 \\). More data consistently reduces loss, but gains diminish as \\( D \\) grows.
- **Compute (\\( C \\), floating-point operations)**: \\( L(C) \propto C^{-\gamma} \\), where \\( \gamma \approx 0.050 \\). This combines the effects of \\( N \\) and \\( D \\), as \\( C \approx 6ND \\) for typical training.

These laws are empirical but remarkably consistent across architectures (e.g., width vs. depth has little impact) and tasks. Other observations include:

- **Sample Efficiency**: Larger models are far more data-efficient—e.g., a 100x larger model needs only ~10x less data for the same loss.
- **Overfitting**: Predictable based on the \\( N/D \\) ratio; it kicks in when \\( N \\) exceeds \\( D \\) by a factor, following \\( L_{\text{test}} - L_{\text{train}} \propto (N/D)^\kappa \\).
- **Optimal Allocation**: For a fixed compute budget, the best strategy is to train *very large* models on a *modest* amount of data, stopping early (before full convergence) to avoid diminishing returns.

### Theoretical and Practical Implications

The paper suggests these laws stem from fundamental properties of neural networks, like irreducible loss floors from noise or irreducible perplexity. They challenge the "bigger data always better" intuition, instead favoring massive models to squeeze more performance from limited compute. This has profoundly influenced modern AI development, justifying investments in giants like GPT-3 by predicting that scaling up predictably yields breakthroughs.

In short, the paper argues for a "compute-optimal" path: prioritize model size, use just enough high-quality data, and train efficiently—paving the way for the scaling era in LLMs.

[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
