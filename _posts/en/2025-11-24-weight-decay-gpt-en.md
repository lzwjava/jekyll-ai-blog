---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Weight Decay in GPT Training Explained
translated: false
type: note
---

### Overview of Weight Decay in Karpathy's Video
In his YouTube video *"Let's Reproduce GPT-2 (124M)"* (a 3+ hour deep dive into replicating OpenAI's GPT-2 training from scratch using PyTorch), Andrej Karpathy discusses weight decay as a key optimization technique during the hyperparameters section, around the 2:51:40 mark (roughly 10700 seconds). This comes after covering data loading and model architecture, as part of setting up the training loop to match GPT-3-style practices. The focus is on using AdamW (a variant of the Adam optimizer) to ensure stable, scalable training for large language models.

Karpathy emphasizes weight decay's role in regularization to prevent overfitting, especially when training on massive text datasets. He sets it to **0.1** (10x the typical AdamW default of 0.01) to align with GPT-3's regime, calling it a "pull of gravity" on the weights that keeps them from exploding or dominating.

### Key Explanation and Analogy
Karpathy describes weight decay as a **gentle, constant downward force**—like gravity—applied to the model's parameters during optimization. This prevents any single weight from growing too large and overfitting to noise in the data. Instead, it encourages the model to **distribute learning across multiple weights**, promoting more robust, shared representations (e.g., features aren't handled by one oversized weight but spread out for better generalization).

He contrasts this with vanilla Adam, noting that AdamW "decouples" weight decay from the adaptive learning rate updates, making it more effective. Without proper decay, large models like GPT-2 can become unstable, leading to poor convergence or exploding gradients.

### Mathematical Formulation
Karpathy briefly derives the update rule for AdamW, highlighting how weight decay is added as a separate shrinkage term:

\\[
\theta_{t+1} = \theta_t - \eta \left( \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda \theta_t \right)
\\]

- \\(\theta_t\\): Parameters (weights) at step \\(t\\)
- \\(\eta\\): Learning rate
- \\(\hat{m}_t, \hat{v}_t\\): Bias-corrected first and second moments (Adam's adaptive terms)
- \\(\lambda\\): Weight decay rate (0.1 in this setup)
- \\(\epsilon\\): Small stability constant

The key addition is \\(+\lambda \theta_t\\), which scales the weights by \\((1 - \eta \lambda)\\) each step, acting like L2 regularization but applied *after* the gradient step. This is crucial for large-scale training, as it stabilizes without interfering with gradient clipping or scheduling.

### Implementation Details
In the code walkthrough, Karpathy shows how to configure the optimizer in `configure_optimizers()`:

```python
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=learning_rate,  # e.g., 6e-4 with warmup
    weight_decay=0.1,  # Higher for GPT-like stability
    fused=True  # Kernel fusion for ~3ms speedup per step
)
```

He stresses **parameter grouping** to apply decay selectively (only where it helps):

| Parameter Group | Examples | Apply Weight Decay? | Why? |
|-----------------|----------|----------------------|------|
| **Decayed** | Embedding matrices, linear/attention weights (2D tensors) | Yes | These drive matrix multiplications; decay prevents overfitting in core computations |
| **No Decay** | Biases, LayerNorm scales/biases (1D tensors) | No | Not involved in inner products; decay here hurts performance without benefits |

This split (e.g., ~50 decayed vs. ~98 non-decayed parameters) is printed at setup for debugging. Karpathy notes it's empirical—drawn from GPT-3 paper insights—and pairs it with cosine learning rate decay and gradient clipping (norm=1.0) for full stability.

### Practical Impact and Tips
- **Why 0.1?** For massive models/datasets, stronger decay enforces sparser, more efficient weights without underfitting.
- **Performance Boost**: Fused AdamW shaves computation time, vital for long runs (e.g., days on multi-GPU setups).
- **Broader Context**: This setup helps the replicated GPT-2 achieve near-OpenAI perplexity scores, underscoring weight decay's "outsized impact" on generalization.

Karpathy's style is hands-on: he codes live, tests values, and ties it back to why it matters for real-world LLM training. If you're implementing this, start with his nanoGPT repo for the full script.

[Let's Reproduce GPT-2 (124M) - YouTube](https://www.youtube.com/watch?v=l8pRSuU81PU)
