---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Activation Functions in GPT Explained
translated: false
type: note
---

### Andrej Karpathy's Explanation of Activation Functions in His "Let's Build GPT" Video

In his YouTube video ["Let's build GPT: from scratch, in code, spelled out."](https://www.youtube.com/watch?v=kCc8FmEb1nY) (note: the provided link points to the same video, with the timestamp at ~2:51:40), Andrej Karpathy discusses activation functions in the context of the Multi-Layer Perceptron (MLP) layer within GPT-2's Transformer architecture. He focuses on why certain activations are chosen for language models, emphasizing gradient flow, neuron health, and empirical performance. The discussion starts around the MLP's role (as the "map" operation after attention's "reduce"), where he explains GELU as the key activation used in GPT-2, contrasts it with alternatives like ReLU and tanh, and briefly touches on Swish for modern context.

Here's a breakdown of his explanations for **GELU** and **tanh** specifically, drawn directly from that section. (He doesn't dwell heavily on tanh alone but uses it as a foil to highlight GELU's advantages.)

#### GELU (Gaussian Error Linear Unit)
Karpathy describes GELU as the activation function powering the non-linearity in GPT-2's MLP (between two linear layers). He stresses its role in ensuring smooth, reliable training in large language models like GPT-2 and BERT.

- **Mathematical Definition**:
  - **Exact GELU**: \\( \text{GELU}(x) = x \cdot \Phi(x) \\), where \\( \Phi(x) \\) is the cumulative distribution function (CDF) of the standard normal distribution: \\( \Phi(x) = \int_{-\infty}^{x} \frac{1}{\sqrt{2\pi}} e^{-t^2/2} \, dt \\).
  - **Approximate GELU** (what GPT-2 actually uses, via PyTorch's `nn.GELU()`): \\( \text{GELU}_{\text{approx}}(x) = x \cdot \sigma(1.702 \cdot x) \\), where \\( \sigma(z) = \frac{1}{1 + e^{-z}} \\) is the sigmoid function.
    - He notes the approximation was a historical choice for faster computation in TensorFlow; today, the exact version works fine and is interchangeable.

- **Why GELU? (Key Advantages Karpathy Highlights)**:
  - **Non-Zero Gradients Everywhere**: Unlike ReLU (which kills gradients for negative inputs, leading to "dead neurons" that output zero and learn nothing), GELU provides a small positive gradient for *every* finite input. This keeps all neurons alive and trainable throughout the network.
  - **Smoother Optimization**: It creates a gentler "optimization landscape" by blending linear behavior for positive inputs with a probabilistic "gating" for negatives (inspired by stochastic regularization and adaptive dropout ideas). This leads to more stable training in deep models.
  - **Empirical Superiority**: Karpathy points out it's "empirically better" for language modeling—models like GPT-2 and BERT perform stronger with it. Output range is roughly \\( (-\infty, \infty) \\), but it smoothly transitions without hard cutoffs.
  - **No Vanishing Issues**: Gradients don't die off like in saturating functions, promoting better gradient flow in very deep Transformers.

He implements it simply in code as part of the MLP forward pass, showing how it processes each token's pooled attention output independently.

#### tanh (Hyperbolic Tangent)
Karpathy doesn't use tanh in the GPT-2 build but references it as an older, flawed alternative to illustrate why modern activations like GELU win out. He frames it as a classic example of what *not* to rely on in deep nets.

- **Mathematical Definition**:
  - \\( \tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}} \\), which squashes any input to the range (-1, 1).

- **Explanation and Drawbacks**:
  - **Saturating Behavior**: For large positive or negative |x|, tanh quickly flattens (saturates), pushing outputs toward ±1. This causes **vanishing gradients**—the derivative approaches zero in those regions, starving deeper layers of learning signals and slowing convergence.
  - **Early Saturation**: It "saturates early" in deep networks, making training inefficient compared to non-saturating options like GELU or ReLU.
  - **Historical Context**: Karpathy implies it's a relic from shallower nets (e.g., early RNNs), but it's unsuitable for Transformers due to these issues. No "dead neurons" like ReLU, but the vanishing problem is worse overall.
  - **Gradient Risk**: High risk of vanishing gradients for large |x|, with outputs bounded to (-1, 1).

#### Quick Comparison (as Karpathy Frames It)
Karpathy contrasts these in the video to justify GELU:

| Activation | Output Range | Key Strength | Main Weakness | Used in GPT-2? |
|------------|--------------|--------------|---------------|----------------|
| **GELU**   | \\( (-\infty, \infty) \\) | Always-positive gradients; smooth & alive neurons | Slightly more compute than ReLU | Yes (approximate form) |
| **tanh**   | (-1, 1)     | Bounded outputs (good for some normalization) | Vanishing gradients; early saturation | No |

He also nods to ReLU (\\( \max(0, x) \\), prone to dead neurons) as what GELU directly improves on, and Swish (\\( x \cdot \sigma(x) \\), used in later models like Llama 3) as a learnable cousin to GELU—but the core focus is GELU's practicality for GPT.

This segment (~5-10 minutes) ties into his hands-on code walkthrough, showing how these choices make the model train reliably on Shakespeare text. For the full nuance, jump to the timestamp in the video!
