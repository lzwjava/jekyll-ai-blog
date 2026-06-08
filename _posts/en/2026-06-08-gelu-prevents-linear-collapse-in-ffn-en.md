---
audio: false
generated: true
image: false
lang: en
layout: post
title: GELU Prevents Linear Collapse in FFN
translated: false
type: note
---

**Question:** Why is GELU necessary in the FFN layer of nanoGPT?

**Answer:**

Without GELU (or any non-linearity), your two linear transformations compose into a single linear transformation:

```python
x_out = W_proj(W_fc(x) + b_fc) + b_proj
      = (W_proj @ W_fc) @ x + ...
```

This is still just a linear function, so the entire FFN layer collapses to linear algebra. You lose all model capacity — the network can only learn linear relationships. **GELU breaks this linearity and enables the model to learn non-linear patterns.**

### Why GELU over ReLU?

GELU is defined as:

$$\text{GELU}(x) = x \cdot \Phi(x)$$

where $\Phi(x)$ is the cumulative distribution function of a standard normal distribution. In practice, it's often approximated as:

$$\text{GELU}(x) \approx 0.5 \cdot x \cdot (1 + \tanh(\sqrt{2/\pi}(x + 0.044715 \cdot x^3)))$$

The key insight: **GELU is smoother and differentiable everywhere**, unlike ReLU which has a hard cutoff at zero. This matters because:

1. **Adaptive gating effect**: GELU weights inputs by how "typical" they are under a Gaussian. High-magnitude inputs pass through mostly unchanged; low-magnitude inputs get suppressed but not zeroed.

2. **Gradient flow**: The smooth curve means better gradient propagation during backprop, especially in deep stacks.

3. **Empirical performance**: Transformers trained with GELU converge faster and reach better loss than ReLU. This was demonstrated empirically in the BERT paper (Devlin et al., 2018).

Here's the comparison in code:

```python
import torch
import torch.nn.functional as F

x = torch.linspace(-3, 3, 100)

relu = F.relu(x)
gelu = F.gelu(x)  # uses approximation
silu = F.silu(x)  # also smooth, used in LLaMA

# GELU is strictly smoother at the origin
# ReLU has a sharp corner, causing gradient issues
```

### In transformer FFNs specifically

The FFN expansion (1600 → 6400 → 1600) creates a bottleneck where GELU acts as both:

- **Non-linearity gate**: Decides which features matter
- **Adaptive regularizer**: Suppresses noise without killing information

Without it, the 4x expansion is wasted — you're just multiplying by dense matrices with no learned selectivity.

**Bottom line**: GELU is what makes the FFN actually learn. It's not ornamental.
