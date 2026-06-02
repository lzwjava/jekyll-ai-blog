---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: NanoGPT Model Architecture Summary
translated: false
type: note
---

### NanoGPT Model Architecture Overview

NanoGPT implements a GPT-2-like decoder-only transformer model in PyTorch. The architecture is defined in the `model.py` file, with a configurable `GPTConfig` that sets hyperparameters. The default configuration (e.g., for the "gpt2" variant) uses:

- **Number of transformer blocks**: 12 (`n_layer = 12`)
- **Embedding dimension (layer size)**: 768 (`n_embd = 768`)
- **Number of attention heads**: 12 (`n_head = 12`)
- **MLP intermediate size**: 3072 (`n_embd * 4`, as the expansion factor is 4)

Each transformer block (class `Block`) is a standard decoder block with residual connections and layer normalization. It includes:

- **LayerNorm 1** (`ln1`): Applied before the self-attention.
- **Multi-Head Self-Attention** (`attn`): Causal (masked) attention to prevent looking ahead.
- Residual addition after attention.
- **LayerNorm 2** (`ln2`): Applied before the MLP.
- **MLP** (`mlp`): A simple feed-forward network.
- Residual addition after MLP.

The overall model (class `GPT`) stacks these 12 blocks after token and position embeddings, followed by a final LayerNorm (`ln_f`) and a linear projection to the vocabulary size.

#### MLP Structure

The MLP (class `MLP` within `Block`) is a two-layer feed-forward network:

- First linear layer (`c_fc`): Projects from `n_embd` (768) to intermediate size (3072).
- GELU activation: Applied element-wise after the first projection.
- Second linear layer (`c_proj`): Projects back from 3072 to `n_embd` (768).

This follows the "fc -> gelu -> projection" pattern you mentioned.

#### Forward Pass Flow

The forward passes are residual-style, with pre-norm (LayerNorm before sub-layers). Here's a high-level breakdown:

1. **Major Forward (GPT.forward)**:
   - Token embeddings: Input tokens (shape `[B, T]`) → embeddings (shape `[B, T, n_embd]`).
   - Positional embeddings: Added to token embeddings.
   - Pass through the stack of `n_layer` (12) transformer blocks: `x = block(x)` for each.
   - Final LayerNorm: `x = self.ln_f(x)`.
   - Linear projection: `logits = self.lm_head(x)` → output shape `[B, T, vocab_size]`.

   Snippet (simplified):

   ```python
   def forward(self, idx, targets=None):
       # ... embedding + positional
       for block in self.blocks:
           x = block(x)
       x = self.ln_head(x)
       logits = self.head(x)
       # ... loss if targets
       return logits
   ```

2. **Forward in Transformer Block (Block.forward)**:
   - Apply `ln1` to input `x`.
   - Self-attention: `x = x + attn(ln1(x))` (residual).
   - Apply `ln2` to the result.
   - MLP: `x = x + mlp(ln2(x))` (residual).

   Snippet (simplified):

   ```python
   def forward(self, x):
       x = x + self.attn(self.ln1(x))
       x = x + self.mlp(self.ln2(x))
       return x
   ```

3. **Forward in Self-Attention (MultiheadAttention.forward)**:
   - LayerNorm input → compute Q, K, V projections (linear layers `c_attn`).
   - Split into heads, apply causal mask, scaled dot-product attention.
   - Concat heads, project back with `c_proj`.
   - Residual add (but in block, it's added outside).

   Key: Causal mask ensures future tokens are ignored. Output shape preserved as `[B, T, n_embd]`.

   Snippet (core attention computation, simplified):

   ```python
   def forward(self, x):
       B, T, C = x.shape
       qkv = self.c_attn(x).split(self.n_embd, dim=2)  # Q,K,V
       # ... reshape to heads, mask, attn = q @ k.transpose / sqrt
       # attn = attn.masked_fill(mask == 0, -1e9)
       # y = attn @ v
       # ... concat and project
       return self.c_proj(y.reshape(B, T, C))
   ```

4. **Forward in MLP (MLP.forward)**:
   - First projection: `x = self.c_fc(x)` → to intermediate size.
   - GELU: `x = F.gelu(x)`.
   - Second projection: `x = self.c_proj(x)` → back to `n_embd`.

   Snippet:

   ```python
   def forward(self, x):
       x = self.c_fc(x)
       x = F.gelu(x)
       x = self.c_proj(x)
       return x
   ```

This setup mirrors GPT-2's architecture closely, with ~124M parameters in the default config. For exact code, check the repo.

[model.py source](https://github.com/karpathy/nanoGPT/blob/master/model.py)
