---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding the nanoGPT Architecture
translated: false
type: note
---

You're asking exactly the right questions to understand how nanoGPT works under the hood. These components fit together in a specific way to predict the next token in a sequence. Let me walk you through the architecture and how it all connects.

## The Complete Picture: From Text to Next Token Prediction

Here's how all the components you mentioned come together to form a complete GPT model:

```
Input Tokens (IDs) 
    ↓
Token Embeddings + Positional Embeddings
    ↓
[Transformer Block × n_layers]
    ├── LayerNorm
    ├── Multi-Head Self-Attention (K, Q, V)
    │   └── Causal Masking (look only at previous tokens)
    ├── Residual Connection (+)
    ├── LayerNorm
    ├── MLP/FeedForward (GELU activation)
    └── Residual Connection (+)
    ↓
Final LayerNorm
    ↓
Linear Layer (lm_head) → Logits for next token
```

## Component Breakdown

### 1. Embeddings: The Starting Point

The model uses **two embedding tables**:
- **Token Embeddings** (`wte`): Maps each token ID (0 to vocab_size-1) to a dense vector of size `n_embd`
- **Positional Embeddings** (`wpe`): Maps each position (0 to block_size-1) to a vector of size `n_embd`

These are **summed together** element-wise: `x = token_embeddings + positional_embeddings`. This gives each token a representation that includes both what it is and where it appears in the sequence.

### 2. The K, Q, V Mechanism in Self-Attention

This is where the magic happens. Inside each attention head, the input `x` gets projected into three matrices:

```python
key = nn.Linear(n_embd, head_size, bias=False)
query = nn.Linear(n_embd, head_size, bias=False)
value = nn.Linear(n_embd, head_size, bias=False)

k = key(x)    # (B, T, head_size)
q = query(x)  # (B, T, head_size)
v = value(x)  # (B, T, head_size)
```

The attention weights are computed as:
```python
wei = q @ k.transpose(-2, -1) / sqrt(head_size)  # Scaled dot-product
```

Then a **causal mask** is applied using a lower triangular matrix to prevent looking at future tokens:
```python
tril = torch.tril(torch.ones(T, T))
wei = wei.masked_fill(tril == 0, float('-inf'))
wei = F.softmax(wei, dim=-1)  # Normalize across rows
out = wei @ v  # Weighted aggregation
```

The **multi-head** version runs this in parallel with multiple heads, then concatenates the results and projects them back.

### 3. MLP/FeedForward Layer

This is a simple but crucial two-layer network applied to each token independently:
```python
class FeedForward(nn.Module):
    def __init__(self, n_embd, dropout):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),  # Expand 4x
            nn.GELU(),                       # Non-linearity
            nn.Linear(4 * n_embd, n_embd),  # Project back
            nn.Dropout(dropout)
        )
```

The hidden dimension is typically **4 times** the embedding dimension (`4 * n_embd`).

### 4. The Transformer Block Structure

Each block follows a specific pattern with residual connections:
```python
def forward(self, x):
    # Self-attention with pre-normalization
    x = x + self.attn(self.ln_1(x))
    # Feed-forward with pre-normalization
    x = x + self.mlp(self.ln_2(x))
    return x
```

## How "Next Token" Prediction Works

This is where many people get confused. The key insight is that **the model predicts all positions simultaneously during training**.

### During Training:
Given input sequence `[a, b, c]`, the model:
1. Processes all tokens in parallel
2. Due to **causal masking**, position 1 sees only token 1, position 2 sees tokens 1-2, position 3 sees tokens 1-3
3. The `lm_head` (a linear layer) is applied to **every position** to predict the next token at that position
4. Targets `y` are the original sequence shifted by one: `[b, c, d]`
5. Loss is computed across all positions simultaneously

This is why training is efficient - the model learns from every position in one forward pass, not one token at a time.

### During Generation/Inference:
When generating new text, the model is called repeatedly:
```python
for _ in range(max_new_tokens):
    # Crop to last block_size tokens
    x_cond = x[:, -block_size:]
    # Forward pass to get logits
    logits = model(x_cond)
    # Take logits of the last position only
    logits_last = logits[:, -1, :]
    # Convert to probabilities, sample
    probs = F.softmax(logits_last, dim=-1)
    next_token = torch.multinomial(probs, num_samples=1)
    # Append to sequence
    x = torch.cat([x, next_token], dim=1)
```

**Important**: The linear layer (`lm_head`) doesn't "know" about context. All the contextual information from previous tokens is already encoded in the last token's embedding after passing through all transformer blocks.

## How Layers Are Built

The layers are constructed hierarchically:

1. **Bottom layer**: Individual components (`CausalSelfAttention`, `MLP`, `LayerNorm`)
2. **Middle layer**: `Block` combining attention + MLP with residuals
3. **Top layer**: `GPT` class that stacks multiple `Block` instances

The model configuration controls everything:
```python
class GPTConfig:
    block_size = 1024    # Max sequence length
    vocab_size = 50257   # GPT-2 vocabulary size
    n_layer = 12         # Number of transformer blocks
    n_head = 12          # Number of attention heads
    n_embd = 768         # Embedding dimension
```

Weight initialization is carefully handled with scaled initialization for deep networks, and the token embeddings are tied with the output projection (`lm_head`) for parameter efficiency.

This architecture, while deceptively simple in its components, creates the powerful autoregressive behavior that makes GPT models work.