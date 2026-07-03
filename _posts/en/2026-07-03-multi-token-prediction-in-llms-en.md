---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Token Prediction in LLMs
translated: false
type: note
---

**Question:** What is MTP (Multi-Token Prediction) in LLMs?

**Answer:**

MTP means training the model to predict **multiple future tokens** at each position instead of just the next one. Standard next-token prediction (NTP) trains `P(t+1 | ≤t)`. MTP adds objectives for `t+2`, `t+3`, ... The two designs you should know: Meta's parallel-heads version (2024 paper) and DeepSeek-V3's sequential-module version, which is the one that actually shipped in a frontier model and carried into the V3.x/R1 lineage you're using.

### Why bother

1. **Denser training signal.** Each position now contributes D+1 loss terms instead of 1. Same data, more gradient — better sample efficiency, especially at scale (Meta found gains *grow* with model size; small models can actually get worse).
2. **Forces lookahead representations.** To predict t+2 well, the hidden state at t must encode a plan, not just a local continuation. This mitigates the myopia of pure teacher forcing.
3. **Free speculative decoding at inference.** The extra heads/modules draft future tokens; the main head verifies them. DeepSeek-V3 reports ~85–90% acceptance rate for the second token, giving ~1.8× decoding TPS.

### Meta's version (Gloeckle et al., 2024)

Shared transformer trunk, then `n` independent output heads, each one transformer layer, all sharing the unembedding matrix. Head `k` predicts token `t+k` from the same trunk hidden state. Fully parallel, no causal chain between the predicted tokens. Loss = sum of the n cross-entropies.

### DeepSeek-V3's version (the important one)

DeepSeek keeps the **complete causal chain** at each prediction depth. Instead of parallel heads, MTP depth `k` is a small sequential module:

```
h_k[i] = TransformerBlock_k( W_k · concat( RMSNorm(h_{k-1}[i]), RMSNorm(Emb(t[i+k])) ) )
logits  = SharedUnembed(h_k[i])   # predicts token t[i+k+1]
```

Key points:
- Module k receives the **previous depth's hidden state** AND the **embedding of the actual next token** (ground truth during training). So predicting t+2 is conditioned on knowing t+1 — causal, not marginal.
- Embedding matrix and output head are **shared** with the main model → cheap in params.
- V3 uses **D = 1** (one extra module, predicts one extra token).
- Loss: `L = L_main + λ · mean(L_mtp_k)`, with λ = 0.3 early, 0.1 later in training.
- The MTP module is **dropped at inference** for standard decoding, or **kept as a self-drafter** for speculative decoding.

### Minimal implementation (~50 lines, DeepSeek-style)

```python
import torch, torch.nn as nn, torch.nn.functional as F

class MTPModule(nn.Module):
    def __init__(self, d, block_cls):
        super().__init__()
        self.norm_h = nn.RMSNorm(d)
        self.norm_e = nn.RMSNorm(d)
        self.proj = nn.Linear(2 * d, d, bias=False)
        self.block = block_cls(d)          # one transformer block

    def forward(self, h_prev, tok_emb_next):
        # h_prev:       (B, T, d)  hidden states from previous depth
        # tok_emb_next: (B, T, d)  embeddings of the *next* ground-truth tokens
        x = self.proj(torch.cat([self.norm_h(h_prev), self.norm_e(tok_emb_next)], dim=-1))
        return self.block(x)               # causal attention inside

class GPTWithMTP(nn.Module):
    def __init__(self, vocab, d, trunk, block_cls, depth=1):
        super().__init__()
        self.emb = nn.Embedding(vocab, d)
        self.trunk = trunk                 # your main transformer stack
        self.head = nn.Linear(d, vocab, bias=False)   # shared unembed
        self.mtp = nn.ModuleList(MTPModule(d, block_cls) for _ in range(depth))

    def forward(self, idx, targets, lam=0.3):
        B, T = idx.shape
        e = self.emb(idx)
        h = self.trunk(e)                              # (B, T, d)
        loss = F.cross_entropy(self.head(h).flatten(0, 1), targets.flatten())

        h_k = h
        for k, mod in enumerate(self.mtp, start=1):
            # align: position i now predicts t[i+k+1]
            h_k = h_k[:, : T - k]
            e_next = self.emb(idx[:, k : T])           # ground-truth t[i+k]
            h_k = mod(h_k, e_next)
            tgt_k = targets[:, k : T]                  # shifted targets
            loss_k = F.cross_entropy(self.head(h_k).flatten(0, 1), tgt_k.flatten())
            loss = loss + lam * loss_k
        return loss
```

To bolt this onto your nanoGPT fork: the trunk is unchanged; you add the embedding-shifted concat, one extra block per depth, and the shifted CE loss. On your MI300X run, expect a small step-time hit (~10% for D=1) in exchange for better loss at the same token count — the tradeoff DeepSeek judged worth it at 671B/14.8T tokens.

### Inference: self-speculative decoding

At decode time, run the main model → get t+1. Feed h and t+1's embedding through the MTP module → draft t+2. Then verify t+2 with one main-model forward pass over both tokens; accept if the main model's argmax/sampled token agrees. Acceptance ~85–90% means you average ~1.8 tokens per main-model step. This is speculative decoding where the draft model costs almost nothing because it reuses the trunk's hidden states — compare against EAGLE/Medusa, which strap similar draft heads onto frozen models post-hoc. MTP is essentially "Medusa, but trained jointly from scratch, with the causal chain kept intact."

### Where it stands

MTP as a training objective is now standard in the DeepSeek lineage and increasingly copied elsewhere; as an inference trick it's converged with the speculative-decoding literature (Medusa, EAGLE-2/3). If you're studying DeepSeek's newer MoE models, the MTP module is one of the three signature pieces alongside MLA and the aux-loss-free MoE routing — worth reading Section 2.2 of the V3 technical report with the code above open next to it.

**References:**

- [Better & Faster Large Language Models via Multi-Token Prediction (Meta, 2024)](https://arxiv.org/abs/2404.19737)
- [DeepSeek-V3 Technical Report — §2.2 Multi-Token Prediction](https://arxiv.org/abs/2412.19437)
- [Medusa: Simple LLM Inference Acceleration with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774)
- [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077)
