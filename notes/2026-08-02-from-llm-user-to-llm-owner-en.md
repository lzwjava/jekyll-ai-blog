---
audio: false
generated: true
image: false
lang: en
layout: post
title: From LLM User to LLM Owner
translated: false
type: note
---

Question: What's the best way to build genuine first-principles understanding of LLMs — architecture, training, and inference — beyond just using them?

Answer: You already have scaling-law/roofline notes, so skip the "what is attention" tutorials. The gap between using LLMs and *owning* them is usually one of three things: (1) never hand-derived the backward pass, (2) never reasoned about FLOPs/memory-bandwidth per layer, (3) never implemented KV-cache + sampling yourself. Do these three and the "essence" clicks.

**1. Forward pass — know every shape, no autograd**

```python
import numpy as np

def gpt_forward(x, Wte, Wpe, blocks, Wlm):
    # x: (B, T) token ids
    B, T = x.shape
    tok_emb = Wte[x]                      # (B, T, C)
    pos_emb = Wpe[np.arange(T)]           # (T, C)
    h = tok_emb + pos_emb                 # (B, T, C)
    for blk in blocks:
        h = block_forward(h, blk)         # (B, T, C)
    logits = h @ Wlm.T                    # (B, T, V)
    return logits

def attn(x, Wq, Wk, Wv, Wo, n_head):
    B, T, C = x.shape
    hd = C // n_head
    q = (x @ Wq).reshape(B, T, n_head, hd).transpose(0,2,1,3)  # (B,nh,T,hd)
    k = (x @ Wk).reshape(B, T, n_head, hd).transpose(0,2,1,3)
    v = (x @ Wv).reshape(B, T, n_head, hd).transpose(0,2,1,3)
    att = q @ k.transpose(0,1,3,2) / np.sqrt(hd)     # (B,nh,T,T)
    mask = np.triu(np.ones((T,T)), k=1).astype(bool)
    att[..., mask] = -np.inf
    att = np.exp(att - att.max(-1, keepdims=True))
    att /= att.sum(-1, keepdims=True)
    out = att @ v                                     # (B,nh,T,hd)
    out = out.transpose(0,2,1,3).reshape(B, T, C)
    return out @ Wo
```

The essence is here: attention is just a content-addressable weighted average — softmax(QKᵀ/√d)V. Everything else (RoPE, GQA, MLA, sliding-window) is a modification to how Q/K/V are produced or masked, not a new mechanism.

**2. Backward pass — derive one linear layer + softmax by hand**

This is the part people skip because autograd hides it. Do it once:

```python
# y = softmax(x @ W), loss = -log(y[target])
# dL/dz (pre-softmax logits) = y - onehot(target)   <- the entire magic of cross-entropy+softmax
dz = y.copy()
dz[range(B), target] -= 1
dW = x.T @ dz / B
dx = dz @ W.T
```

Every gradient in a transformer reduces to chain-ruling through matmuls and softmax exactly like this. If you've derived `dz = y - onehot(target)` yourself, the loss curve you watch during GPT-2 training stops being a black box.

**3. Inference — prefill/decode split + KV cache is the whole story**

```python
class KVCache:
    def __init__(self, n_layer, n_head, hd, max_T):
        self.k = np.zeros((n_layer, n_head, max_T, hd))
        self.v = np.zeros((n_layer, n_head, max_T, hd))
        self.pos = 0

def decode_step(token, cache, blocks, Wte, Wpe, Wlm):
    h = Wte[token] + Wpe[cache.pos]        # (1, C) — single new token
    for i, blk in enumerate(blocks):
        q, k, v = project(h, blk)          # (1, hd) each
        cache.k[i, :, cache.pos] = k
        cache.v[i, :, cache.pos] = v
        att = softmax(q @ cache.k[i, :, :cache.pos+1].T / sqrt(hd))
        h = att @ cache.v[i, :, :cache.pos+1] @ blk.Wo
    cache.pos += 1
    return h @ Wlm.T                       # logits for next token
```

Prefill is compute-bound (large matmul, full sequence at once). Decode is memory-bandwidth-bound (you reload the entire model's weights from HBM to generate *one* token) — this is exactly the roofline distinction you already have notes on, and it's why batching + speculative decoding + quantization all target the decode phase specifically.

**Where the real depth is now (post-fundamentals):**
- FlashAttention: the memory-bound nature of attention on GPU, IO-awareness instead of FLOP-awareness is documented with code in the curated inference paper list.
- MLA/GQA: compressing the KV cache is the dominant lever for long-context serving cost — DeepSeek-V2's multi-head latent attention and related economical-inference work is the current state of the art here.
- Since you've already trained GPT-2 760M: the next rung is re-deriving Chinchilla yourself on your own loss curves (fit `L(N,D) = E + A/N^α + B/D^β` against your actual runs) rather than trusting the paper's constants — your MI300X runs are the perfect dataset for this.

For an end-to-end version that goes model → pretrain → SFT → reward → DPO/PPO/GRPO with real (not toy) code, this repo is the most complete public writeup with actual training-shaped code rather than a single-file demo: it's structured stage-by-stage (Data, Pretrain, SFT, Reward, DPO, PPO, GRPO, Evaluate, Chat) with theory and real code per stage.

References:
- [train-llm-from-scratch (full pipeline, real code)](https://github.com/FareedKhan-dev/train-llm-from-scratch)
- [Awesome-LLM-Inference (FlashAttention, PagedAttention, quantization, papers+code)](https://github.com/xlite-dev/Awesome-LLM-Inference)
- [LLM Inference Unveiled: Survey + Roofline Model](https://arxiv.org/pdf/2402.16363)
- [Your own notes: Transformer Fundamentals (scaling laws, roofline)](https://phonism.github.io/LLMNotes/en/transformer-part1-fundamentals/)
- [Karpathy: Let's reproduce GPT-2 (build_nanogpt)](https://github.com/karpathy/build-nanogpt)