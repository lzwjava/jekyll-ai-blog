---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Maximal Update Parametrization for Neural Networks
translated: false
type: note
---

### What is μP (Maximal Update Parametrization)?

μP, short for Maximal Update Parametrization, is a neural network parametrization technique developed by Greg Yang, a mathematician and AI researcher now at xAI (previously at Microsoft Research). Introduced in his 2022 paper "Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer," it reparametrizes the weights of deep learning models to make them more scalable and efficient for training.

#### Purpose
The core goal of μP is to stabilize hyperparameter (HP) tuning across different model sizes. In traditional setups (like standard parametrization, or SP), hyperparameters such as learning rates need to be retuned every time you scale up a model—e.g., from millions to billions of parameters—because gradients and updates become unstable (often scaling quadratically with model width or depth). μP fixes this by transforming the parameters so that the "maximal update" (the largest possible gradient step) remains consistent regardless of scale. This enables **μTransfer**, a workflow where you tune HPs on a tiny "proxy" model and directly apply them to a massive target model without any further adjustments.

#### Key Benefits
- **Dramatic Cost Savings**: Tuning on small models is cheap. For example, transferring HPs from a 13M-parameter proxy outperformed published BERT-large (350M params) results, with total tuning cost equivalent to just one pretraining run of BERT-large. For GPT-3 (6.7B params), a 40M-proxy transfer beat baselines at only 7% of the full pretraining cost.
- **Scalability for Large Models**: Works well on architectures like Transformers and ResNets, making it ideal for training enormous NNs (e.g., those used at xAI). It ensures "scale-invariant optima," meaning the loss landscape doesn't warp unpredictably as models grow.
- **Ease of Use**: Available as a PyTorch library (`pip install mup`), and it's been integrated into production training pipelines for big AI models.

#### Quick Mathematical Intuition
In SP, the variance of weights grows unstably, leading to exploding/vanishing gradients. μP reparametrizes weights (e.g., for a linear layer, scaling by fan-in) to normalize the Fisher information matrix, ensuring gradient flows stay balanced. This keeps optimal HPs (like learning rates) roughly constant across scales, avoiding the need for per-size retuning.

μP builds on Yang's broader "Tensor Programs" framework for understanding infinite-width/depth limits in NNs, and it's still evolving—recent work (as of 2025) emphasizes its role in maximal feature learning beyond just HP transfer.

**References**
- [Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer](https://arxiv.org/abs/2203.03466)
- [The Practitioner's Guide to the Maximal Update Parameterization](https://www.cerebras.ai/blog/the-practitioners-guide-to-the-maximal-update-parameterization)
- [How To Scale (Blog on μP and Scaling)](https://howtoscalenn.github.io/)
- [Greg Yang's Professional Page](https://thegregyang.com/)
