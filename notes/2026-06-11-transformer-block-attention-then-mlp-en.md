---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Transformer Block: Attention then MLP"
translated: false
type: note
---

**Question:** In nanoGPT's 12-layer (or 20-layer) stack, what's inside each block? Does FFN wrap the MLP, and is attention inside the MLP?

**Answer:**

Close, but the nesting is wrong in two ways. Let's fix the mental model:

**1. MLP and FFN are the same thing.** Two names for one module. "Feed-Forward Network" is the paper terminology (Attention Is All You Need), "MLP" is what Karpathy calls it in nanoGPT code. There's no wrapping relationship — they're synonyms.

**2. Attention is NOT inside the MLP.** Attention and MLP are *siblings* inside the block, applied sequentially. The block contains exactly two sub-layers:

```
Block = LayerNorm → Attention → residual add
      → LayerNorm → MLP(FFN) → residual add
```

Here's the actual nanoGPT code ([model.py](https://github.com/karpathy/nanoGPT/blob/master/model.py)):

```python
class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln_1 = LayerNorm(config.n_embd, bias=config.bias)
        self.attn = CausalSelfAttention(config)   # sub-layer 1
        self.ln_2 = LayerNorm(config.n_embd, bias=config.bias)
        self.mlp = MLP(config)                    # sub-layer 2 (this IS the FFN)

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))   # attention first
        x = x + self.mlp(self.ln_2(x))    # then MLP/FFN
        return x
```

And the MLP itself — no attention inside, just two linear layers with GELU in between:

```python
class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.c_fc   = nn.Linear(config.n_embd, 4 * config.n_embd)  # expand 4x
        self.gelu   = nn.GELU()
        self.c_proj = nn.Linear(4 * config.n_embd, config.n_embd)  # project back

    def forward(self, x):
        return self.c_proj(self.gelu(self.c_fc(x)))
```

So for GPT-2 124M (`n_layer=12, n_embd=768`), each token vector flows through:

```
x ∈ R^768
  → ln_1 → attention (tokens talk to each other)  → + x
  → ln_2 → 768 → 3072 → GELU → 3072 → 768          → + x
```

× 12 blocks, then final LayerNorm → lm_head.

Two details worth internalizing:

- **Pre-norm**: nanoGPT (following GPT-2) puts LayerNorm *before* each sub-layer, not after as in the original 2017 Transformer. Pre-norm keeps the residual stream clean and trains much more stably at depth — this is why you can stack 12, 20, 48 layers without warmup tricks.
- **Division of labor**: attention is the only place tokens mix with each other (communication); the MLP processes each token position independently (computation). Karpathy's framing: "attention is communicate, MLP is compute."

A useful intuition for the residual stream: think of `x` as a shared 768-dim "bus" flowing top to bottom, and each attention/MLP sub-layer reads from it, computes something, and *adds* its contribution back. Nothing wraps anything — it's 24 sequential read-compute-add operations (12 attention + 12 MLP) on the same stream.

Parameter check for one GPT-2 block: attention ≈ 4 × 768² ≈ 2.36M, MLP ≈ 8 × 768² ≈ 4.72M — the MLP holds ~2/3 of each block's parameters. In your 760M run, same ratio (until you go MoE, where the FFN is exactly the part that gets replicated into experts — that's the DeepSeek v4 connection).

**References:**

- [nanoGPT model.py](https://github.com/karpathy/nanoGPT/blob/master/model.py)
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [GPT-2 paper (Language Models are Unsupervised Multitask Learners)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
