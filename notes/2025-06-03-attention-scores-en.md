---
audio: false
generated: true
lang: en
layout: post
title: Stabilizing Attention Scores in Transformers
translated: false
type: note
---

Dividing by the square root of the key dimension, \\(\sqrt{d_k}\\), in the scaled dot-product attention mechanism (as in the formula \\(\text{Scaled Scores} = \frac{Q K^T}{\sqrt{d_k}}\\)) is a deliberate choice to stabilize gradients and prevent large values, particularly in the context of transformers. Here's why \\(\sqrt{d_k}\\) is used instead of just \\(d_k\\):

1. **Variance of Dot Product**:
   - The dot product \\( Q K^T \\) computes the similarity between query (\\( Q \\)) and key (\\( K \\)) vectors, where each vector has dimension \\( d_k \\). If the elements of \\( Q \\) and \\( K \\) are assumed to be independent and have a mean of 0 and variance of 1 (common after initialization or normalization), the dot product \\( Q_i \cdot K_j \\) (for a single pair of query and key vectors) has a variance of \\( d_k \\). This is because the variance of the sum of \\( d_k \\) independent products of two standard normal variables scales linearly with \\( d_k \\).
   - Without scaling, the magnitude of \\( Q K^T \\) grows with \\( d_k \\), leading to very large values for large \\( d_k \\) (common in transformers, where \\( d_k \\) might be 64, 128, or larger). Large values in the attention scores can cause issues when passed through the softmax function.

2. **Softmax Stability**:
   - The attention scores \\( \frac{Q K^T}{\sqrt{d_k}} \\) are fed into a softmax to compute attention weights. If the scores are too large (as they would be without scaling or with insufficient scaling), the softmax function can produce very sharp distributions, where one element dominates (approaching 1) and others are near 0. This leads to vanishing gradients for most elements, making it hard for the model to learn effectively.
   - Dividing by \\(\sqrt{d_k}\\) ensures that the variance of the scaled scores is approximately 1, keeping the scores in a range where the softmax function behaves well, producing more balanced attention weights and stable gradients.

3. **Why Not \\( d_k \\)?**:
   - Dividing by \\( d_k \\) instead of \\(\sqrt{d_k}\\) would over-scale the dot product, reducing the variance of the scores to \\( \frac{1}{d_k} \\). For large \\( d_k \\), this would make the scores very small, causing the softmax to produce nearly uniform distributions (since small inputs to softmax result in outputs close to \\( \frac{1}{n} \\)). This would dilute the attention mechanism's ability to focus on relevant keys, as the differences between scores would be diminished.
   - Over-scaling with \\( d_k \\) could also lead to numerical instability in some cases, as very small values might be harder to handle precisely in floating-point arithmetic.

4. **Why \\(\sqrt{d_k}\\)?**:
   - Dividing by \\(\sqrt{d_k}\\) normalizes the variance of the dot product to approximately 1, as \\( \text{Var}\left(\frac{Q K^T}{\sqrt{d_k}}\right) = \frac{\text{Var}(Q K^T)}{d_k} = \frac{d_k}{d_k} = 1 \\). This keeps the scores in a reasonable range, ensuring that the softmax produces meaningful attention weights without being overly sharp or overly uniform.
   - The square root arises naturally from the mathematical property of the dot product's variance. It strikes a balance between preventing exploding values (which would happen without scaling) and avoiding over-suppression of the scores (which would happen with \\( d_k \\)).

5. **Empirical Effectiveness**:
   - The choice of \\(\sqrt{d_k}\\) was introduced in the original Transformer paper ("Attention is All You Need" by Vaswani et al., 2017) and has been empirically validated across many transformer-based models. It works well in practice for a wide range of \\( d_k \\) values, ensuring stable training and good performance.

In summary, dividing by \\(\sqrt{d_k}\\) is a mathematically motivated choice that stabilizes the variance of the attention scores, ensures the softmax operates in a well-behaved regime, and avoids the issues of either exploding or vanishing gradients. Dividing by \\( d_k \\) would overly reduce the scores, leading to less discriminative attention weights and potentially harming model performance.
