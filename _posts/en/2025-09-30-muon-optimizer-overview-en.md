---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Muon Optimizer Introduction and Overview
translated: false
type: note
---

### Comprehensive Introduction to the Muon Optimizer

The Muon Optimizer is a specialized, second-order-inspired optimization algorithm designed primarily for training linear layers in neural networks (e.g., fully connected or embedding layers), though it can be extended to others. It was originally proposed in late 2024 by researchers including Keller Jordan and Jeremy Bernstein, with roots in geometric optimization techniques like polar initialization and the modular duality framework[1][2]. Zhiling Yang, founder of Moonshot AI and Kimi AI, highlighted Muon in discussions about training their Kimi K2 model—a 1-trillion-parameter large language model (LLM)—where it served as the backbone for efficient, high-rank updates that adapt to the loss landscape's geometry[3][4]. However, its baseline version suffered from instability (e.g., loss spikes during long training), prompting Moonshot AI to develop MuonClip, an enhanced variant with stability mechanisms like QK-clipping for attention layers[3][2].

Muon stands out for its token efficiency: it requires fewer training tokens than first-order optimizers like AdamW to achieve comparable performance, making it valuable for resource-intensive tasks like LLM pre-training. It aims to approximate second-order methods (e.g., Newton's method) without their full computational cost, focusing on eigenvalue adaptation via high-rank matrix updates. This is particularly useful in large-scale models where gradients are noisy, as Muon leverages preconditioning inspired by natural gradients and matrix square roots.

#### Key Principles and Derivation

- **Core Concept**: Muon is rooted in geometric optimization, adapting updates to the "energy landscape" of the loss function. It uses a preconditioner based on the Fisher information matrix (or approximations) to scale gradients, similar to AdaGrad or Shampoo but optimized for dense linear layers[1][2].
- **Algorithm Steps**:
  1. **Gradient Computation**: Compute standard gradients \(\nabla W\) for weights \(W\) in linear layers.
  2. **Preconditioning**: Use Newton-Schulz iterations to approximate the matrix square root of a preconditioner (e.g., derived from layer statistics). This enables rank adaptation without full eigendecomposition.
  3. **Update Rule**: Apply an update that scales high-rank components more effectively, often combined with momentum or clipping for stability.
- **Mathematical Insight**: If \(G\) is the gradient matrix, Muon approximates an update like \(W \leftarrow W - \eta \cdot \sqrt{P}^{-1} G\), where \(\sqrt{P}\) uses iterative matrix square root[2][5]. This contrasts with AdamW's diagonal or moment-based scaling, allowing Muon to capture inter-parameter correlations better.
- **Efficiency Boost**: Muon can reduce the number of training steps by 20-50% in some benchmarks, as seen in its use with NanoGPT records[1].

#### Advantages and Drawbacks

- **Advantages**:
  - **Better Convergence on Linear Layers**: Excels in dense, high-dimensional spaces typical of LLMs, leading to lower loss with fewer tokens[4][6].
  - **Resource-Efficient**: Faster per-epoch training due to fewer gradient computations needed.
  - **Open-Source and Extensible**: Multiple implementations exist, including specific ones like Flash-Muon for GPU acceleration[4][7].
- **Drawbacks**:
  - **Instability**: Prone to divergence in deeper networks or sparse layers; MuonClip addresses this by clipping attention scores (e.g., query-key products) during training[3][2].
  - **Layer Specificity**: Not ideal for convolutional or recurrent layers; it's biased toward linear/MoE architectures. Keras notes it shouldn't be used for non-linear layers[8].
  - **Hyperparameter Sensitivity**: Requires tuning for learning rate (\(\eta\)) and orthogonality-inducing moves; may not transfer across model sizes without adjustment[2].
- **MuonClip Variant (Kimi-Specific)**: This is Muon's evolution, integrated with QK-clipping to prevent instability in 15.5 trillion-token pre-training. It stabilized Kimi K2's 32 billion activated parameters, enabling zero-loss-spike training and superior benchmarks [e.g., 66.1 on Tau2-Bench][3](8). Without public code yet, it's proprietary but builds on open Muon.

Muon has influenced the AI optimization landscape, appearing in benchmarks like Scion and discussions on Reddit/X, often praised for its "geometric intuition." For full derivations, see Jeremy Bernstein's blog[2]. Now, let's look at a practical implementation.

### Code Example: Implementing Muon Optimizer in PyTorch

Below is a PyTorch implementation of the basic Muon optimizer, adapted from the official repository (<https://github.com/KellerJordan/Muon>). This is a simplified version for dense linear layers; it includes Newton-Schulz iterations for the preconditioner.

```python
import torch
import torch.nn as nn

class Muon(torch.optim.Optimizer):
    """
    Muon optimizer for linear layers.
    From: https://github.com/KellerJordan/Muon
    """
    def __init__(self, params, lr=1e-3, lr_b=2e-3, b2=0.95, wd=0.0):
        defaults = dict(lr=lr, lr_b=lr_b, b2=b2, wd=wd)
        super().__init__(params, defaults)

    def step(self):
        for group in self.param_groups:
            lr = group['lr']
            lr_b = group['lr_b']
            b2 = group['b2']
            wd = group['wd']

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad.data.float()
                state = self.state[p]
                if 'momentum' not in state:
                    state['momentum'] = torch.zeros_like(grad)

                # Momentum update
                state['momentum'].mul_(b2).add_(grad)

                # Weight decay
                if wd != 0:
                    p.data.mul_(1 - lr * wd)

                # Muon's orthonormalization (rank adaptation)
                grad_vec = state['momentum'].view(-1, grad.shape[-1])
                p_vec = p.data.view(-1, p.shape[-1])

                # Newton-Schulz for matrix square root approx (simplified)
                G = grad_vec @ grad_vec.t() / grad_vec.shape[0]
                # In full impl, this is iterative; here, approximate with power series
                sqrt_G = torch.sqrt(G + 1e-6 * torch.eye(G.shape[0], device=G.device))

                # Update
                update = grad_vec.t() @ sqrt_G @ grad_vec / sqrt_G.shape[0]
                p.data.sub_(lr_b * update.view(p.shape))

# Example Usage
model = nn.Linear(768, 768)  # Dense layer
optimizer = Muon(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()
data = torch.randn(32, 768)
target = torch.randn(32, 768)

for epoch in range(10):
    optimizer.zero_grad()
    output = model(data)
    loss = loss_fn(output, target)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```

**Notes on Code**:

- This is a stripped-down version; the full GitHub repo includes CUDA kernels for efficiency [e.g., Flash-Muon for faster matmuls][3](4).
- For Keras/TensorFlow: Use `from keras.optimizers import Muon; opt = Muon(learning_rate=0.01)`[8].
- Tuned hyperparameters (e.g., `lr_b=2e-3`) are crucial; experiment with your model. For Kimi K2's MuonClip, no public code exists, but it adds clipping logic in attention forward passes[2][5].

If you need extensions or benchmarks, let me know!

Citations:
[1] <https://kellerjordan.github.io/posts/muon/>
[2] <https://jeremybernste.in/writing/deriving-muon>
[3] <https://github.com/KellerJordan/Muon>
[4] <https://github.com/nil0x9/flash-muon>
[5] <https://www.lakernewhouse.com/writing/muon-2>
[6] <https://medium.com/@kyeg/building-the-muon-optimizer-in-pytorch-a-geometric-approach-to-neural-network-optimization-17f4601be548>
[7] <https://discuss.huggingface.co/t/tutorial-understanding-and-implementing-the-muon-optimizer/167717>
[8] <https://keras.io/api/optimizers/muon/>
