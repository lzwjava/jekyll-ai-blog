---
audio: false
generated: true
image: false
lang: en
layout: post
title: nanoGPT Architecture Explained Step-by-Step
translated: false
type: note
---

**Question:** How does nanoGPT work? Walk through the full architecture: GPT Block, Causal Self-Attention, MLP, and how the layers stack into the neural network.

**Answer:**

Let me build this up from first principles, layer by layer, then show you the full architecture visually. I'll use Karpathy's nanoGPT as the reference implementation throughout — it's the cleanest GPT implementation in existence.

---

## The Big Picture

A GPT is just a **function**: tokens in → logits out. Everything else is engineering to make that function learn well.

```
input ids [B, T]
    → token embeddings + positional embeddings [B, T, C]
    → N × TransformerBlock [B, T, C]
    → LayerNorm
    → linear projection [B, T, vocab_size]
    → logits
```

Where `B`=batch, `T`=sequence length, `C`=embedding dim (n_embd).

---

## 1. Token + Positional Embedding

```python
self.transformer = nn.ModuleDict(dict(
    wte = nn.Embedding(vocab_size, n_embd),   # token embedding
    wpe = nn.Embedding(block_size, n_embd),   # positional embedding
    drop = nn.Dropout(dropout),
    h = nn.ModuleList([Block(config) for _ in range(n_layer)]),
    ln_f = nn.LayerNorm(n_embd),
))
```

Forward:

```python
tok_emb = self.transformer.wte(idx)           # [B, T, C]
pos_emb = self.transformer.wpe(pos)           # [1, T, C]
x = self.transformer.drop(tok_emb + pos_emb) # [B, T, C]
```

No sinusoidal magic here — just learned lookup tables for both token identity and position. Sum them directly.

---

## 2. The Block (TransformerBlock)

This is the core repeating unit. nanoGPT's `Block`:

```python
class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd)
        self.mlp = MLP(config)

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))  # attention sub-layer with residual
        x = x + self.mlp(self.ln_2(x))   # FFN sub-layer with residual
        return x
```

Key insight: **Pre-LN** (LayerNorm before the sub-layer, not after). Original "Attention is All You Need" used Post-LN. Pre-LN trains more stably. The `x + ...` is the **residual connection** — gradients flow straight through it, preventing vanishing gradients across N layers.

---

## 3. Causal Self-Attention

This is where the magic happens.

```python
class CausalSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        # Q, K, V projections in one matrix for efficiency
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd, bias=config.bias)
        # output projection
        self.c_proj = nn.Linear(config.n_embd, config.n_embd, bias=config.bias)
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        # causal mask
        self.register_buffer("bias", torch.tril(torch.ones(config.block_size, config.block_size))
                             .view(1, 1, config.block_size, config.block_size))

    def forward(self, x):
        B, T, C = x.size()
        head_size = C // self.n_head

        # Project to Q, K, V
        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)  # each [B, T, C]

        # Reshape for multi-head: [B, n_head, T, head_size]
        q = q.view(B, T, self.n_head, head_size).transpose(1, 2)
        k = k.view(B, T, self.n_head, head_size).transpose(1, 2)
        v = v.view(B, T, self.n_head, head_size).transpose(1, 2)

        # Attention scores: (B, nh, T, hs) × (B, nh, hs, T) → (B, nh, T, T)
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(head_size))

        # CAUSAL MASK: future tokens → -inf → softmax → 0
        att = att.masked_fill(self.bias[:,:,:T,:T] == 0, float('-inf'))
        att = F.softmax(att, dim=-1)
        att = self.attn_dropout(att)

        # Weighted sum of values
        y = att @ v  # [B, nh, T, hs]

        # Reassemble heads
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.resid_dropout(self.c_proj(y))
```

The math:

```
Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V
```

- `QKᵀ / √d_k` → [T, T] matrix of scores: how much does position i attend to position j?
- `masked_fill(..., -inf)` → forces upper triangle to 0 after softmax = **causal** (no peeking at future)
- `softmax` → converts scores to probabilities (rows sum to 1)
- `@ V` → weighted sum of value vectors

Each head operates on `C/n_head` dims independently, learning different attention patterns. Multi-head = run this in parallel N times, concatenate.

---

## 4. The MLP (FFN)

```python
class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.c_fc   = nn.Linear(config.n_embd, 4 * config.n_embd, bias=config.bias)
        self.gelu   = nn.GELU()
        self.c_proj = nn.Linear(4 * config.n_embd, config.n_embd, bias=config.bias)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        x = self.c_fc(x)    # [B, T, 4C]
        x = self.gelu(x)    # nonlinearity
        x = self.c_proj(x)  # [B, T, C]
        x = self.dropout(x)
        return x
```

Expand by 4×, apply GELU, project back. This is where the model does **per-token computation** after attention has mixed information across positions. Attention = communication. MLP = computation. That's the mental model.

GELU vs ReLU: GELU is smooth at 0, which helps with gradient flow. Defined as `x · Φ(x)` where Φ is the Gaussian CDF.

---

## 5. Output Head

```python
self.lm_head = nn.Linear(n_embd, vocab_size, bias=False)
```

And crucially, **weight tying**:

```python
self.transformer.wte.weight = self.lm_head.weight
```

The embedding matrix and the final projection share weights. This saves ~50M params in GPT-2 and makes sense semantically: the same vector space is used to encode input tokens and decode output logits.

---

## The Full Forward Pass

```python
def forward(self, idx, targets=None):
    B, T = idx.size()
    pos = torch.arange(0, T, dtype=torch.long, device=idx.device)

    # Embed
    tok_emb = self.transformer.wte(idx)
    pos_emb = self.transformer.wpe(pos)
    x = self.transformer.drop(tok_emb + pos_emb)

    # N transformer blocks
    for block in self.transformer.h:
        x = block(x)

    # Final layernorm
    x = self.transformer.ln_f(x)

    # Project to vocab
    if targets is not None:
        logits = self.lm_head(x)  # [B, T, vocab_size]
        loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
    else:
        logits = self.lm_head(x[:, [-1], :])  # inference: only last token
        loss = None

    return logits, loss
```

At inference you only need to run `lm_head` on the last token's hidden state — that's the next-token prediction.

---

Now let me visualize the whole stack:Click any box to drill deeper into that component.

---

## Parameter Count (GPT-2 small: 124M)

| Component | Params |
|---|---|
| `wte` (token emb) | `vocab_size × C = 50257 × 768 ≈ 38.6M` |
| `wpe` (pos emb) | `1024 × 768 ≈ 0.8M` |
| Per Block: attn `c_attn` | `C × 3C = 768 × 2304 ≈ 1.77M` |
| Per Block: attn `c_proj` | `C × C ≈ 0.59M` |
| Per Block: MLP `c_fc` | `C × 4C ≈ 2.36M` |
| Per Block: MLP `c_proj` | `4C × C ≈ 2.36M` |
| 12 blocks total | `≈ 85M` |
| `lm_head` | shared with `wte`, +0 |

Weight tying saves ~38.6M params.

---

## Residual Stream Mental Model

Think of `x` as a **residual stream** that flows through the network. Each block reads from it and writes incremental updates back:

```
x₀ = embed(tokens)
x₁ = x₀ + attn₁(ln(x₀))
x₂ = x₁ + mlp₁(ln(x₁))
x₃ = x₂ + attn₂(ln(x₂))
...
xₙ = logits
```

Nothing is destroyed — information accumulates. This is why residual networks train so much better than plain deep networks: gradients flow straight from loss back to the embedding layer with no multiplicative chain.

---

## One Line That Ties It Together

Karpathy's best insight about transformers: **"Attention is communication, MLP is computation."** Attention lets tokens gather information from other positions in the sequence. MLP processes that gathered information independently per token. Stack these N times and you get a model that can build up increasingly abstract representations across layers.

References:

- [nanoGPT source — Karpathy](https://github.com/karpathy/nanoGPT/blob/master/model.py)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Language Models are Unsupervised Multitask Learners (GPT-2)](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
