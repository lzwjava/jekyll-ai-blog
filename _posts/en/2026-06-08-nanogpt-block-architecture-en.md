---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoGPT Block Architecture
translated: false
type: note
---

## Question

Explain the Block class from nanoGPT — how it combines layer norm, attention, and MLP.

## Answer

This is a **transformer decoder block** — the repeating unit that stacks to form the entire language model. Let me walk through the forward pass and the architectural choices.

### The Forward Pass

```python
def forward(self, x):
    x = x + self.attn(self.ln_1(x))           # Path 1: Attention with residual
    x = x + self.mlp(self.ln_2(x))            # Path 2: MLP with residual
    return x
```

**Step-by-step:**

1. **`self.ln_1(x)`** — Apply layer norm to input
2. **`self.attn(...)`** — Pass normalized activations through causal self-attention (attends to previous tokens only)
3. **`x + ...`** — Add residual connection: `x_out = x + Attn(LayerNorm(x))`
4. **`self.ln_2(x_out)`** — Apply layer norm again
5. **`self.mlp(...)`** — Pass through feed-forward network (dense → activation → dense)
6. **`x + ...`** — Add another residual: `x_final = x_out + MLP(LayerNorm(x_out))`

### Why Pre-Norm Architecture?

This uses **pre-norm** (normalize before the sublayer) not post-norm (normalize after). The difference matters:

```python
# Pre-norm (this code)
x = x + SubLayer(LayerNorm(x))

# Post-norm (older style)
x = LayerNorm(x + SubLayer(x))
```

**Pre-norm advantages:**

- **Better gradient flow** — Gradients pass directly through residual connections without being squeezed by layer norm
- **Trains faster** — Deeper models are more stable (nanoGPT uses this for good reason)
- **No warmup needed** — Post-norm requires learning rate warmup; pre-norm doesn't

### Residual Connections: The Identity Shortcut

The `x + ...` is critical. Without it:

```python
# Without residual
x = self.attn(self.ln_1(x))  # x could vanish or explode through many layers
x = self.mlp(self.ln_2(x))
```

**With residual:**

```python
x = x + self.attn(self.ln_1(x))
```

The network learns **additive updates** to x, not replacements. Mathematically:

```
x_l+1 = x_l + f_l(x_l)
```

This enables:

- **Deep networks** — Gradients flow directly: ∂L/∂x_l = ∂L/∂x_l+1 · (1 + ∂f/∂x_l)
- **Safe initialization** — f starts near zero (small weights), so x_l ≈ x_0 early in training
- **Information bypass** — Attention/MLP learn to modify, not rebuild x

### How Attention and MLP Interact

```
Block(x) where dim(x) = [batch, seq_len, n_embd]

→ Attn: "which past tokens are relevant?" (context aggregation)
→ MLP: "given attended context, what patterns emerge?" (feature transformation)
```

The MLP is position-wise (applied identically to each token):

```python
# MLP internals (roughly)
def forward(self, x):
    x = x @ W1 + b1      # [batch, seq, n_embd] → [batch, seq, 4*n_embd]
    x = gelu(x)          # Activation
    x = x @ W2 + b2      # [batch, seq, 4*n_embd] → [batch, seq, n_embd]
    return x
```

So each block does:

1. **Attention** — cross-token communication (mixing information across sequence)
2. **MLP** — per-token nonlinear transformation (feature refinement)

### Full Block Diagram

```
Input x
  ↓
[LayerNorm] → [CausalSelfAttention] → [+ residual] → x'
  ↓
[LayerNorm] → [MLP] → [+ residual] → Output
```

### Stacking Blocks

nanoGPT stacks N of these (typically 12 or 24). Each layer sees progressively higher-level features:

```python
x = embedding(input_ids)  # [batch, seq, n_embd]
for _ in range(num_layers):
    x = Block(config)(x)   # Repeated refinement
x = final_layer_norm(x)
logits = x @ token_embedding.T  # Predict next token
```

Early blocks learn low-level syntax (spaces, punctuation). Later blocks learn semantic relationships.

### Key Insight

The Block is **minimal but elegant**:

- No dropout here (nanoGPT is small, overfitting isn't the main issue)
- No learned scaling (layer norm handles variance)
- Pre-norm + residuals = training stability without tricks

This is why it works: **simple components + good residual structure = deep networks that train**.
